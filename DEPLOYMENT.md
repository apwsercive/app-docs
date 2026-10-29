# 当前部署记录

- GitHub 仓库：https://github.com/apwsercive/app-docs
- 文档中心：https://apwsercive.github.io/app-docs/
- 发布分支：`main`
- Pages 来源：GitHub Actions
- 首次成功运行：https://github.com/apwsercive/app-docs/actions/runs/40843761980
- 工作流提交：`e2d5402711d22511523a783f5ef6c5350ec71a71`
- 状态：已上线的协议草稿，尚未确认运营主体、联系邮箱和生效日期。

## 发布地址

| 语言 | 隐私协议 | 服务条款 |
| --- | --- | --- |
| 简体中文 | https://apwsercive.github.io/app-docs/kongming/zh-Hans/privacy/ | https://apwsercive.github.io/app-docs/kongming/zh-Hans/terms/ |
| English | https://apwsercive.github.io/app-docs/kongming/en/privacy/ | https://apwsercive.github.io/app-docs/kongming/en/terms/ |

## 本地仓库与维护

目标本地目录：`~/Desktop/app-docs`。远程仓库：`https://github.com/apwsercive/app-docs.git`，分支 `main`。

原先通过浏览器部署的 `source.zip` 已由本次迁移改为普通源码目录；工作流直接执行 `check.py`、`build.py` 并部署 `dist/`，不再解包或自动向仓库推送。Markdown 文档位于 `content/<app>/<locale>/<article>.md`，提交到 `main` 后自动发布。认证与首次推送结果以本次交付说明为准。

此前浏览器登录账号与 GitHub 连接器账号不同；连接器对本仓库仅有读权限。日常终端／Sourcetree 推送需使用有此仓库写权限的 GitHub 身份。

## 已完成验证

- GitHub Actions 的 `build`、`deploy` 均成功，包括链接与新增 App／语言／文档检查。
- 四份协议的匿名 HTTP 请求均返回 200；核对了页面 `lang`、草稿 noindex 标识、对应文档的语言切换和仓库子路径。
- 线上 CSS 返回 200；在浏览器中确认首页渲染和语言选择入口，保存了页面预览。
- 没有修改 App 的协议入口，没有执行 iOS 构建、启动模拟器或做法律审查。
