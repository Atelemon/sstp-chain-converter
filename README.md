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


## VPNGate 自动抓取（未检测节点独立发布）

未经检测的 VPNGate SSTP 节点**绝不自动加入** `nodes.txt`。两个 Raw 地址完全分开：

- 原有手动节点（由网页和 Issue 更新）：https://raw.githubusercontent.com/Atelemon/sstp-chain-converter/main/nodes.txt
- 自动抓取的未检测节点：https://raw.githubusercontent.com/Atelemon/sstp-chain-converter/main/nodes-auto.txt

`nodes-manual.txt` 用于保存手动提交的原始集合，`nodes.txt` 与其内容保持一致；`nodes-auto.txt` 仅存放自动抓取结果。两个 GitHub Actions 工作流不再互相合并，定时刷新只会提交 `nodes-auto.txt`。

`update_vpngate.py` 配合 `.github/workflows/refresh-vpngate.yml` 每 6 小时及手动触发时获取一次上游 SSTP 订阅，先尝试北京时间、UTC 当前秒级时间戳 token；无效时退回到 Actions Secret `VPNGATE_TOKEN` 配置的固定 token。时间格式只是推测，并未证实上游接受动态 token。只有返回可解析的 SSTP 记录、且存在能识别地区的节点时才更新 `nodes-auto.txt`，失败时保留既有文件。

在 Settings → Secrets and variables → Actions 中可创建 `VPNGATE_TOKEN` Secret 保存有效 token。若确认动态 token 不被服务端接受，可把自动工作流中的 `VPNGATE_TIME_TOKENS` 设为 `false`。

自动节点仅按照订阅备注或 IP 地理信息分区；**未经连通性、出口住宅属性、信誉/纯净度或安全性验证**，不可当作已检测节点使用。允许的地区为 US/JP/KR/RU/TW/HK/SG/GB/DE/CA/AU，其他地区或无法判定地区的节点会跳过。公开仓库、Issue、TXT 及 Git 历史可能暴露节点凭据，请勿放入私人账号密码。
