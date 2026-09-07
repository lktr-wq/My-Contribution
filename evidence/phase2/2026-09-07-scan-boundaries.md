# DeviceScan 小规模边界筛选：未形成可推进候选

## 本轮目标与决定

继续寻找新候选，不恢复旧 DeviceReduce 或 DeviceSelect 路线。只检查原版 I32 ExclusiveSum 在工作块数量变化处是否存在三轮均明显变慢的现象；不修改 CCCL、不做优化 A/B、不公开发布、不下载依赖或改变系统配置。

结论：**没有达到预先设定的继续门槛，而且小任务计时噪声很高。本轮停止，不对这些差异继续深入分析。** 这不是“不存在优化空间”的证明，也不是性能回归报告。

## 路径依据与上游初筛

固定版本 `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`：

- `cub/cub/device/dispatch/tuning/tuning_scan.cuh`：sm86+ I32 默认 lookback，128 threads × 15 items/thread，tile=1920；固定延迟参数 350/450。
- `cub/cub/device/dispatch/dispatch_scan.cuh`：扫描块数 `ceil(N/1920)`，初始化块数 `ceil(scan_tiles/128)`。
- 实际日志确认 sm89、lookback、128×15。1920→1921 时 scan grid 1→2；245760→245761 时 scan grid 128→129、init grid 1→2。
- 46080→46081 对应 scan grid 24→25；GPU 有 24 SM，但这**不等于**单个 SM 只能驻留一个块，也不保证构成新的调度波次。日志给出理论每 SM 8 块 occupancy；没有据此断言负载不均。
- 本轮未检查 SASS 或采集 profiler counters；无优化实现，日志仅确认实际启动路径。

2026-09-07 使用 GitHub REST 初筛 `repo:NVIDIA/cccl is:pr scan in:title`，145 项中读取最近更新的 40 项；另查 `repo:NVIDIA/cccl scan "single tile" in:title,body`，返回 5 项。非穷尽排重。

亲自读取 [开放草稿 PR #9840](https://github.com/NVIDIA/cccl/pull/9840)：它增加 opt-in 的 BlockScan reduce-then-scan 算法，当前主要针对 BlockTopK 的 block 级延迟，不是本轮三个 DeviceScan 边界的已验证端到端修复。本轮未复制、编译或测试该 PR，作者 B200 数据也不作为本机证据。

## 实验范围和预设门槛

- 自建 baseline harness；原版 DeviceScan::ExclusiveSum，I32 输入/输出、I64 N，独立输入输出。
- N 为 1920、46080、245760 三个中心，各取 N-1/N/N+1，共 9 个配置。
- 输入 `1+i%17`，CPU I64 累加构造每项 exclusive-sum 期望值；所有中间结果均落在 I32 范围。
- 每配置计时前后检查全部输出以及输出两端哨兵。不是 sanitizer 验证；未证明所有输入/临时存储读写均无越界。
- 进程开始做约 500 ms 非计时运行缓解升频阶段；每配置另有 20 次 NVBench warmup。它不保证测量稳定，仍核对实际频率。
- 3 种执行顺序，1000 接受样本/配置，15 秒/配置与 100 秒/测量进程上限。保留默认 75% 低频拒绝阈值，不自动复跑。
- 继续条件：中心 N+1 对 N 三轮都至少慢 20%；各对平均 SM 频率差不超过 2%；检查通过；丢弃尝试不超过 1%。这是候选筛选门槛，不是统计显著性检验或优化收益门槛。

## 实测结果

| 边界 | 第一轮 delta | 第二轮 delta | 第三轮 delta | 配对 delta 中位数 |
|---|---:|---:|---:|---:|
| 1920→1921 | +8.54% | 0.00% | 0.00% | 0.00% |
| 46080→46081 | +18.78% | +5.02% | +5.96% | +5.96% |
| 245760→245761 | -5.00% | +10.53% | +5.26% | +5.26% |

全部门槛未通过。正号表示更慢；表格只是描述性统计，不是可靠的性能差异结论。

- 三轮共 27,000 个接受样本；丢弃 2 次低频尝试，未出现配置超时边界。
- 27 个计时配置的前后共 54 次完整输出/哨兵检查通过；路径日志另含 4 配置的前后检查。
- 九组中心配对的平均 SM 频率差绝对值最大约 0.173%，频率门槛通过。
- 各配置 GPU 耗时中位数约 14.34～21.50 us；样本相对标准差约 **54.4%～108.2%**，明显偏高。频率可比不能消除其他运行波动，本轮未确定噪声来源。
- 编译 11.41 s、链接 0.87 s、路径日志运行 0.97 s；三轮测量进程共约 10.45 s（含 CPU 检查、非计时预热等）。不是整轮调查的墙钟时间。

带日志的 `--profile` 运行包含打印开销，**其所有时间均排除**，仅用来确认 kernel 配置。该运行也包含非计时预热的重复日志，因此日志较大；原始输出保持完整、不做裁剪。

## 环境与证据

CCCL-Ubuntu / lktr；RTX 4060 Laptop；CUDA 13.3；sm89。开始时插电、100% 电量、Turbo；每轮前后验证 Turbo。初始瞬时 GPU 使用率曾为 40%，后续读数为 8%，未发现 wallpaper 进程或超过所查阈值的 GPU engine 项；这不证明没有其他 GPU 活动。未关闭任何用户进程。

CCCL 实验前后工作树干净。二进制、源码、驱动脚本、NVBench 动态库 SHA256 和完整命令记录在 manifest；build 产物不进 Git。Agent 2 的两个已有修改文件未触碰。

- `evidence/phase2/scan_boundaries.cu`
- `evidence/phase2/run_scan_boundaries.py`
- `evidence/raw/phase2/2026-09-07-scan-boundaries/manifest.json`
- 同目录的 path / round1～round3 日志与原始 NVBench JSON。

复现需指定不存在的新输出目录：

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/run_scan_boundaries.py' '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/scan-boundaries-recheck'
```

## 下一阶段边界

不继续这三个小规模边界，不为小差异调参数。后续优先考虑耗时更长的大规模吞吐候选，先做小矩阵确认测量是否足够稳定，再决定是否深入；不通过人为批量计时掩盖端到端成本，也不假定任务变大就一定消除噪声。目前没有新的已验证性能问题或优化收益。
