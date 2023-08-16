import os

def get_all_env_variables():
    """
    获取并打印所有环境变量

    :return: None
    """
    # 使用os.environ获取所有的环境变量
    env_variables = os.environ

    # 遍历所有环境变量并打印
    for key, value in env_variables.items():
        print(f"{key}: {value}")

# get_all_env_variables()

