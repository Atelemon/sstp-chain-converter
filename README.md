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


## VPNGate 自动获取与汇聚

新增 `update_vpngate.py` 和 `.github/workflows/refresh-vpngate.yml`。每 6 小时及手动触发时，尝试北京时间与 UTC 当前秒级时间戳作为 token；若都不可用，再尝试仓库 Actions Secret `VPNGATE_TOKEN` 中配置的原始 token。**时间戳格式只是推测，尚未证实上游接受动态 token。** 所有 token 尝试都需返回可解析的 SSTP 列表，否则不更新任何结果。

第一次使用请到 Settings → Secrets and variables → Actions → New repository secret，创建 `VPNGATE_TOKEN`，值为自行掌握的有效 token（不要提交到代码或 Issue）。如果确认服务端不支持当前时间 token，可以把工作流 `VPNGATE_TIME_TOKENS` 设为 `false`，只用固定 token。可以在 Actions → Refresh VPNGate SSTP nodes → Run workflow 手动运行并检查日志；未验证接口成功前不要假定自动更新正常。

`nodes-manual.txt` 保存手工节点，`nodes-auto.txt` 保存上游拉取节点，`nodes.txt` 为两者按 SSTP 地址去重后的固定输出。原来的 Issue 流程现只覆盖手动集合并触发重新合并，不再直接冲掉自动数据。原有 `nodes.txt` 已预先复制到 `nodes-manual.txt`。

仅接受地区备注或 IP 地址地理位置识别为 US/JP/KR/RU/TW/HK/SG/GB/DE/CA/AU 的节点；无法判断地区则跳过。这是地址的地理信息，不是对 SSTP 实际出口、住宅属性、节点可用性或 IP 信誉的验证。当前没有接入 AbuseIPDB/Scamalytics。GitHub 仓库及 TXT 是公开的，请不要向这些文件提交私人账号凭据。
