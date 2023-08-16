import os
# github 个人令牌
GITHUB_TOKEN = os.environ.get("github_token", "")
GITHUB_PRIVATE_KEY = os.environ.get("github_private_key", "")

# gitee 个人令牌
GITEE_TOKEN = os.environ.get("gitee_token", "")
GITEE_PRIVATE_KEY = os.environ.get("gitee_private_key", "")

# 需要同步的仓库名单，为空是默认获取全部仓库
REPO_LIST = [
]

# 不同步的仓库名单，名单中的仓库不会被同步
# 特别的，如果仓库名称在 gitee 中不存在，也不会同步
# 以及仓库名称中带有 "-", "." 字符，也不会同步
EXCLUDED_REPO_LIST = [
]
