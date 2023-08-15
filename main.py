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


def get_commit_id(owner, repo_name, access_token, web_site='github'):
    # using an access token
    auth = Auth.Token(access_token)

    # First create a Github instance:

    # Public Web Github
    if web_site.lower().strip() == 'gitee':
        base_url = "https://gitee.com/api/v5"
    else:
        base_url = "https://api.github.com"

    g = Github(auth=auth, base_url=base_url)

    # 获取仓库
    repo = g.get_repo(f"{owner}/{repo_name}")

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

def github2gitee(github_access_token, gitee_access_token, 
                 github_owner, gitee_owner,
                 github_repo_name, gitee_repo_name):
    # 判断是否最新，若非最新，则更新 gitee 仓库
    gitee_commit_id = get_commit_id(gitee_owner, gitee_repo_name, gitee_access_token, web_site='gitee')
    github_commit_id = get_commit_id(github_owner, github_repo_name, github_access_token)

    if github_commit_id != gitee_commit_id:
        print(f"仓库 {github_owner}/{github_repo_name} 最新 commit id 为 {github_commit_id}, 更新中")
        # 同步
        github_repo_url = f"git@github.com:{github_owner}/{github_repo_name}.git"
        gitee_repo_url = f"git@gitee.com:{gitee_owner}/{gitee_repo_name}.git"
        sync_repo(github_repo_url, gitee_repo_url)
        gitee_commit_id = get_commit_id(gitee_owner, gitee_repo_name, gitee_access_token, web_site='gitee')
    
    if gitee_commit_id == github_commit_id:
        print(f"仓库 {gitee_owner}/{gitee_repo_name} 已更新到最新。 \ncommit id: {github_commit_id}")
    else:
        print("更新失败，请人工检查。\ncommit id: {github_commit_id}")

def run():
    # load config

    # 定义要获取提交历史的仓库信息
    for repo_name in config.REPO_LIST:
        print(f"开始扫描仓库 : {config.GITEE_OWNER}/{repo_name}")
        github2gitee(config.GITHUB_TOKEN, config.GITEE_TOKEN,
                     config.GITHUB_OWNER, config.GITEE_OWNER,
                     repo_name, repo_name)
        

if __name__ == "__main__":
    import sys
    import config
    argvs = dict(enumerate(sys.argv))
    github_token = argvs.get(1, None)
    gitee_token = argvs.get(2, None)
    if not github_token:
        config.GITHUB_TOKEN = github_token
    if not gitee_token:
        config.GITEE_TOKEN = gitee_token
    if not config.GITHUB_TOKEN or not config.GITEE_TOKEN:
        raise ValueError("GITHUB_TOKEN or GITHUB_TOKEN is empty")
    run()