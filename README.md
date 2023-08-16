# github2gitee

## 项目说明
将 gitee 作为 github 的备份仓库，当 github 仓库发生变更时，会自动同步到 gitee 上去

## 功能
1. **自动更新**： 当 github 的仓库发生变更时，自动同步代码变更以及commit历史记录到 gitee 对应的仓库
2. **一次配置，适配所有仓库**：不需要针对每个仓库进行单独的设置，也不需要在每个 github 仓库上增加 github action
3. **支持私有仓库**： 同时支持同步 github 公有仓库和私有仓库
4. **灵活选择同步仓库**：支持仓库的黑白名单配置，默认同步所有 github 仓库， 可以只同步指定仓库，也可以屏蔽特定仓库

## 准备：
1. 需要一个云主机，同时在云主机上设置 github 和 gitee 的仓库的密钥
2. 创建 github 和 gitee 的个人令牌
3. 在 gitee 上将想要同步的仓库先同步一次

## 实现：
1. 默认拉去 github 所有的仓库，然后排出屏蔽的仓库，同时排除 gitee 上不存在的仓库，作为需要同步的仓库列表
2. 分别拉去 github 和 gitee 上最新的 commitid，如果不相同，则同步

## 运行
1. 确保本地能同时从 github ，gitee 上拉取和提交代码
2. 下载仓库代码，安装依赖
3. 配置 config.py
4. 运行 main.py（python3）
5. 在 crontab 中增加定时任务

## 没有云主机怎么办？

如果没有云主机，可以参考项目中的 github action，用 schedule 进行定时触发，此时需要将 github 和 gitee 的私钥都放到 action 的 secret 中。 

使用 github action 需要的变量：

```secret
GITEE_PRIVATE_KEY: gitee 的私钥，用于提交代码
GIT_PRIVATE_KEY： github 的私钥，用于拉取代码
GITEE_TOKEN： gitee 的个人令牌，用于获取仓库列表，查询 commit id 等
GIT_TOKEN： github 的个人令牌，用于获取仓库列表，查询 commit id 等
```

Github Action 同步结果：

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202308161306768.png)