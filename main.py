# -*- coding:utf-8 -*-
"""
- requirements
GitPython
PyGithub
"""
import git
from github import Github
# Authentication is defined via github.Auth
from github import Auth


def get_git_client(access_token, web_site="github"):
    # using an access token
    auth = Auth.Token(access_token)

    # First create a Github instance:

    # Public Web Github
    if web_site.lower().strip() == 'gitee':
        base_url = "https://gitee.com/api/v5"
    else:
        base_url = "https://api.github.com"

    g = Github(auth=auth, base_url=base_url)
    return g
   

def get_commit_id(git_client, owner, repo_name):

    # 获取仓库
    repo = git_client.get_repo(f"{owner}/{repo_name}")

    # 获取仓库的历史提交记录
    commits = repo.get_commits()

    # 获取最近的 commit id
    commit_id = commits[0].raw_data['sha']
    return commit_id

def sync_repo(src_url, dest_url):
    """ 同步
    """
    # github_repo = f"git@github.com:{github_owner}/{github_repo_name}.git"
    # gitee_repo = f"git@gitee.com:{gitee_owner}/{gitee_repo_name}.git"
    repo_name = src_url.split("/")[-1].split(".")[0]
    import tempfile

    with tempfile.TemporaryDirectory() as local_path:
        print(f"下载仓库到临时目录： {local_path} ...")
        git.Repo.clone_from(src_url, local_path)
        print("下载完成")
        repo = git.Repo(local_path)
        origin = repo.remotes.origin
        origin.set_url(dest_url)
        print(f"推送到目标仓库")
        repo.git.push("--all")
        repo.git.push("--tags")
        print("推送完成")

def github2gitee(github_client, gitee_client,
                 github_owner, gitee_owner,
                 github_repo_name, gitee_repo_name):
    # 判断是否最新，若非最新，则更新 gitee 仓库
    github_commit_id = get_commit_id(github_client, github_owner, github_repo_name)

    gitee_commit_id = get_commit_id(gitee_client, gitee_owner, gitee_repo_name)

    if github_commit_id != gitee_commit_id:
        print(f"仓库 {github_owner}/{github_repo_name} 最新 commit id 为 {github_commit_id}, 更新中")
        # 同步
        github_repo_url = f"git@github.com:{github_owner}/{github_repo_name}.git"
        gitee_repo_url = f"git@gitee.com:{gitee_owner}/{gitee_repo_name}.git"
        sync_repo(github_repo_url, gitee_repo_url)
        gitee_commit_id = get_commit_id(gitee_client, gitee_owner, gitee_repo_name)
    
    if gitee_commit_id == github_commit_id:
        print(f"仓库 {gitee_owner}/{gitee_repo_name} 已更新到最新。 \ncommit id: {github_commit_id}")
    else:
        print("更新失败，请人工检查。\ncommit id: {github_commit_id}")


def get_repo_names(git_client):
    """ 获取指定用户的仓库列表
    """
    user = git_client.get_user()
    repos = user.get_repos()
    return [i.name for i in repos]

def run():
    # load config

    # 定义要获取提交历史的仓库信息
    cnt = 1
    github_client = get_git_client(config.GITHUB_TOKEN, 'github')
    github_owner = github_client.get_user().login

    gitee_client = get_git_client(config.GITEE_TOKEN, 'gitee')
    gitee_owner = gitee_client.get_user().login

    gitee_repo_names = get_repo_names(github_client)

    if config.REPO_LIST:
        all_repo_names = config.REPO_LIST
    else:
        all_repo_names = get_repo_names(github_client)

    scan_repo_names = [i for i in all_repo_names if i not in config.EXCLUDED_REPO_LIST and i in gitee_repo_names]

    for repo_name in scan_repo_names:
        if cnt > 1:
            print("")
        print(f"{cnt}/{len(scan_repo_names)} 开始扫描仓库 : {github_owner}/{repo_name}")
        github2gitee(github_client, gitee_client,
                     github_owner, gitee_owner,
                     repo_name, repo_name)
        cnt += 1   


if __name__ == "__main__":
    import config
    if not config.GITHUB_TOKEN or not config.GITEE_TOKEN:
        raise ValueError("GITHUB_TOKEN or GITHUB_TOKEN is empty")
    run()
