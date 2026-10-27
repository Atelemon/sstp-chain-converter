# SSTP 转换和 TXT 集合

网站：https://atelemon.github.io/sstp-chain-converter/
固定 TXT：https://raw.githubusercontent.com/Atelemon/sstp-chain-converter/main/nodes.txt

## 使用
1. 在网页粘贴原始 SSTP 节点，填写入口并转换。
2. 点击提交更新集合，核对 GitHub Issue 正文。
3. 用 Atelemon 账户提交该 Issue，标题保持更新节点集合。
4. 等待仓库 Actions 中 Update public node collection 完成。
5. edgetunnel 读取固定 Raw TXT 地址；在 Clash 中更新 edgetunnel 生成的订阅。

## 机制
Issue 正文必须是一个 text 代码块，内容为转换结果。只接受仓库所有者本人创建或编辑的更新请求，不接受其他账户请求。Actions 使用自动生成的 GITHUB_TOKEN 写入 nodes.txt，不要求网页输入个人 Token。
本次功能部署不会把旧节点填入空的 nodes.txt。第一次实际集合发布需要你提交节点。
Actions 的自动提交不会触发普通 Pages 分支构建，因此更新后的集合以 Raw 地址为准，不使用 Pages 的 nodes.txt 地址。
提交不是即时保存，需要等待任务完成和 Raw 缓存刷新。重复节点名称按要求保留，不测试连通性。
公开的 Issue、nodes.txt 和 Git 历史会包含提交的节点凭据。不要提交私人账号密码或 GitHub Token。
如果仓库禁用 Actions 或受组织权限限制，任务可能失败。查看 Actions 任务日志，不要随意扩大权限。
