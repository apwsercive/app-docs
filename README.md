# 多 App 文档中心（GitHub Pages）

独立的静态文档站源码，使用 Python 3.9+；Markdown 解析器已固定版本随站点放在 `vendor/`，无需额外安装或联网构建。第三方许可证见 [THIRD_PARTY.md](THIRD_PARTY.md)。中英文协议按孔明工具当前代码整理，尚待确认运营主体、公开联系邮箱、主要发行地区和生效日期。当前内容标注草稿，不应作为正式上架协议。

此目录可直接复制为独立 GitHub 仓库的根目录，建议仓库名 `app-docs`。不要把 iOS 工程或其他 App 的私有源码上传到公开协议仓库。原 `sites/kongming-legal/` 草稿保持原样。

## 地址设计

稳定路径是 `/{app-id}/{locale}/{document-id}/`。App ID、语言标记和文档 ID 不随显示名称翻译或改名。

| 内容 | 路径 |
| --- | --- |
| 文档中心 | `/` |
| 中文应用列表 | `/zh-Hans/` |
| English app list | `/en/` |
| 孔明工具语言选择 | `/kongming/` |
| 中文隐私协议 | `/kongming/zh-Hans/privacy/` |
| 中文服务条款 | `/kongming/zh-Hans/terms/` |
| English Privacy Policy | `/kongming/en/privacy/` |
| English Terms of Service | `/kongming/en/terms/` |

项目型 Pages 的完整地址为 `https://<owner>.github.io/<repo>/kongming/zh-Hans/privacy/`；用户／组织主页型仓库 `<owner>.github.io` 则没有 `/<repo>` 前缀。语言由明确链接选择，不使用强制自动跳转；切换语言保留当前 App 与文档，无翻译时不展示该语言的文档链接。

## 本地构建与检查

```sh
cd ~/Desktop/app-docs
python3 check.py
python3 build.py
python3 -m http.server 8000 --directory dist
```

浏览 `http://localhost:8000/`。重新构建前删除仅用于生成的 `dist/`：`python3 -c "import shutil; shutil.rmtree('dist', ignore_errors=True)"`。构建器要求输出目录为空，以免残留已移除的 App、语言或旧页面。

子路径构建：`python3 build.py --base-path /app-docs`。此时必须从相应子路径提供文件，不能把 `dist` 直接当作域名根目录浏览。

## 首次发布

1. 确认 `site.json` 的 `publisher.name` 和 `publisher.email`；这些信息会公开展示。当前没有拿 GitHub 个人资料替代运营主体确认。
2. 审阅四份 `content/kongming/{zh-Hans,en}/{privacy,terms}.md`，确认产品描述、会员权益、发行地区相关要求；设置真实的 `effective` 生效日期、`updated` 更新日期，并将 `status` 改为 `published`。不要仅为让流水线通过而改状态。
3. 将本目录内容（包含 `.github/` 和 `.gitignore`，不含 `dist/`）放到目标文档仓库根目录，默认分支为 `main`；其他默认分支需同步修改 workflow。
4. 仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**，再推送 `main` 或手动运行工作流。
5. 工作流先执行链接与扩展性检查，读取 Pages 实际 `base_path`，仅上传 `dist/`。默认允许部署明确标注草稿、禁止搜索引擎索引的预览页面；预览不能作为正式上架协议。正式发布时，在仓库 Settings → Secrets and variables → Actions → Variables 设置 `DOCS_RELEASE=true`，启用严格发布检查；未完成署名、生效日期和草稿确认时，正式构建会明确失败。即使没有启用此变量，标为 `published` 的文档也必须补齐署名、邮箱和生效日期。
6. 检查 Actions 成功、部署 URL 可匿名访问、四个协议 URL 返回成功且页面语言正确，再填写 App Store Connect 与 App 内入口。此次未更改 App 中的 `PolicyView`。

免费方案通常选择公开文档仓库；私有仓库能否启用 Pages 取决于 GitHub 套餐。仓库可见性与网站访问权限需要分别确认。

## 新 App、语言与文档

- 新 App：在 `site.json.apps` 增加稳定 ID、各语言显示名，在 `content/<app-id>/<locale>/` 添加 Markdown。`documents` 可省略，或用来指定已有文档的显示顺序。不要直接套用孔明工具的数据处理承诺，每个 App 独立核实。
- 新语言：在 `site.json.locales` 添加 BCP 47 语言标记、语言自称、`dir` 和全部导航文案；在 App 的 `names` 添加翻译，在对应语言目录添加文档。生成器支持 `rtl` 和 CSS 逻辑方向。
- 新文档：例如 `support.md`、`faq.md`、`licenses.md`；直接放入 `content/<app-id>/<locale>/`，构建时自动发现并列入目录，不需登记文档列表。
- 兼容旧 JSON 格式，但同一路径不可同时保留同名 `.md` 和 `.json`，避免误读旧文案。
- 仅有真实翻译的页面会出现在切换链接中；不静默回退到其他语言。运行 `python3 check.py` 验证新内容。

## 用 Markdown 写文章

例如新增 `content/kongming/zh-Hans/guide.md`：

```md
# 使用指南

这里直接写正文，支持 **粗体**、*斜体*、链接、引用、列表和代码块。

## 如何保存

- 打开工具。
- 完成处理后点击分享。

[隐私协议](privacy.md)
```

只有一个 `# 标题` 就能生成草稿页面，地址为 `/kongming/zh-Hans/guide/`。没有填写日期时显示“待确认”，不会凭空生成生效日期。暂不扩展表格、脚注等非 CommonMark 语法；原生 HTML 按文本显示，不执行脚本。图片及其他静态资源不在此次自动收集范围。

正式协议可以在文件最前面加一段简单的元数据（只接受以下平铺字段，不是完整 YAML）：

```md
---
version: "1.0"
updated: 2026-10-29
effective:
status: draft
---

# 隐私协议

## 本机处理 {#on-device}

协议正文……
```

`effective` 留空表示尚未生效，`status` 支持 `draft` / `published`。正式发布仍要求完整的主体、邮箱和日期。标题也可以使用元数据 `title:`；如同时写 `# 标题`，两处需一致。

`##` 自动生成章节目录；`{#on-device}` 是可选的稳定章节 ID。迁移的四份协议保留了原有 ID，请勿随意改动。文章之间可直接写 `[服务条款](terms.md)`，跨语言可以写 `[English](../en/privacy.md#location)`，构建时会转换为正确的线上网址（含仓库子路径）。

本地添加 Markdown 后仍需发布到 GitHub，才会更新网站。当前线上源码包与更新方式见 [DEPLOYMENT.md](DEPLOYMENT.md)。把单个 MD 上传到仓库根目录不会变成 App 文章；它必须位于上述 `content/` 结构中。

日常维护直接在本地仓库编辑 `content/` 中的 Markdown，或在 GitHub 中编辑同路径文件。新增 MD 自动进入文章目录；新 App 和语言只需先在 `site.json` 中登记。

```sh
cd ~/Desktop/app-docs
python3 check.py
git add content site.json
git commit -m "更新文档"
git push origin main
```

推送到 `main` 后，GitHub Actions 自动检查、构建和部署。若多人或多台设备维护，开始编辑前先运行 `git pull --ff-only`；出现冲突时先处理冲突。`dist/`、`source.zip` 和缓存不会提交。`package.py` 只是可选的离线打包工具，正常发布不再使用 ZIP。

## 协议维护

当前文案覆盖本机处理、存储／备份、权限、定位与 Apple 地名查询、可见水印、系统分享、Apple 购买、反馈邮件、删除请求、GitHub Pages 访问数据，以及订阅取消／恢复／退款、结果准确性和法定消费者权利。未假设特定法院或司法辖区；主要发行地区确认后应核对相应条款。

`version` 用于标识正文修订，`updated` 和 `effective` 分开维护；中英文表达应同步审阅。重大更新前用 Git tag 保存旧版源码和生效记录（例如 `kongming-legal-v1.0`），日常地址始终提供当前有效文档。当前不提供旧版本的独立公开 URL。

页面采用系统字体、蓝色文本链接、单列正文、章节目录、可见焦点、跳转正文、亮暗色和打印样式；没有动画、外部字体、广告、分析脚本、表单或追踪 Cookie。GitHub 托管仍记录访客 IP 等基础访问数据，不能把“无分析脚本”表述为“网站不收集任何数据”。

## 核对来源

- [GitHub Pages 及访客 IP 日志](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub 隐私声明](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)
- [Apple 审核指南，隐私与购买要求](https://developer.apple.com/app-store/review/guidelines/)
- [Apple 自动续订订阅](https://developer.apple.com/app-store/subscriptions/)

这是一份依据当前代码的文档草稿及发布实现，不代表已完成特定地区法律审核或 App Store 审核。
