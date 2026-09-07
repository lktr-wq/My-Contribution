# 2026-09-07 新候选筛选：两条路线暂不推进

## 对齐的目标与边界

遵循用户最新决定：封存 DeviceReduce 残余块向量化实验，不再分析失败原因；快速筛选新的、有明显收益空间且不直接重复上游工作的候选。本轮不修改 CCCL、不公开 issue/PR、不改系统或代理配置、不下载依赖。

## 候选一：DeviceSegmentedSort 短段分桶

固定源码的 sm86+ I32 keys-only 策略，medium 为 16×7=112 项，large 为 256×23=5888 项；超过 500 段启用分桶路径。112→113 是值得复现的算法切换边界，但容量倍率不是耗时或可获得的加速倍率。

2026-09-07 核对原始来源：

- [性能 epic #10577](https://github.com/NVIDIA/cccl/issues/10577)：上游已明确指出粗粒度分桶和填充浪费。
- [细粒度分桶 #6792](https://github.com/NVIDIA/cccl/issues/6792)：开放，页面显示分配给 gonidelis；讨论 kernel 级与 runtime 级细粒度选择。
- [工作负载征集 #10661](https://github.com/NVIDIA/cccl/issues/10661)：维护者明确正在重做该模块。
- [开放 PR #11030](https://github.com/NVIDIA/cccl/pull/11030)：GitHub REST 实时读取标题及正文，正在添加 runtime-width group merge-sort primitive，含不同线程组宽度、有效项限制和冗余 merge pass 提前终止。

决定：**因方向明显重叠而暂不投入**，未编译或测量分段排序。PR #11030 是相关底层实现，不等于已修复 112→113 的全部端到端问题，更不等于已经合并。不得把已知上游问题称为本项目的新发现。

检索边界：GitHub REST 查询 `repo:NVIDIA/cccl is:pr segmented sort` 返回 207 项，读取最近更新的前 30 项并进一步打开 #11030。不是穷尽所有 PR 的证明；发现重叠已足以作本轮停止决策。网页元数据可能有缓存，以 PR REST 读取的开放状态为本次依据。

## 候选二：DeviceSelect::Flagged 的标记分布

问题：同样保留一半数据，交替、前半段集中、随机打乱三种标记分布，是否导致明显的耗时差距？这是普通输入分布敏感性筛选，不是优化 A/B，也不是 bug 复现。

范围：

- 原版 CUB；I32 输入、U8 flags、I64 计数；out-of-place，输入和 flags 在重复执行中不变。
- N=1,048,576 和 4,194,304，精确保留 N/2；随机分布从同一 50% flags 集合打乱，seed=6721。
- Case 0/1/2 分别为小规模交替/集中/随机，Case 3/4/5 为大规模对应分布。
- 输入值为 `i-N/2`，唯一且含正负数，CPU 逐项构造稳定筛选期望结果。
- 每个配置计时前后核对全部有效输出、计数和输出前后未使用区哨兵。18 个配置、36 次完整检查全部通过。哨兵不能代替 Compute Sanitizer；本轮未运行 sanitizer、SASS 或 profiler。
- 自建诊断 harness，参考官方 Flagged benchmark 的 GPU/no_batch 测量方式；不是原样官方 benchmark，也不声称跑过官方完整测试套件。

源码依据：`cub/cub/agent/agent_select_if.cuh` 的 `Scatter` 根据 tile 选中数切换 direct/two-phase scatter；同样总体保留比例仍可能有不同 tile 局部分布。这里只据此提出可证伪的筛选问题，未证明任何特定瓶颈。

## 预先设定的继续门槛

三轮全部同方向、每轮中位耗时差距至少 20%；同一对配置接受样本的平均 SM 频率差不超过 2%；正确性检查通过；每配置被丢弃尝试比例不超过 1%。这只是是否值得继续调查的门槛，不是已经获得的优化收益。

三轮顺序为 `[0,1,2,3,4,5]`、反序、`[2,0,1,4,5,3]`。每配置 20 次 warmup、1000 个接受样本，NVBench 原有 75% 低频阈值不变。15 秒/配置、100 秒/进程上限，无自动复跑。

## 结果

相对同规模交替分布，三轮配对 delta 的中位数（正数表示较慢）：

| 输入规模 | 集中分布 | 随机分布 | 继续门槛 |
|---|---:|---:|---|
| 1,048,576 | 0.000% | -0.472% | 未通过 |
| 4,194,304 | +1.943% | +2.069% | 未通过 |

- 共 18,000 接受样本、0 个低频丢弃、0 个超时边界配置。
- 第一轮小规模两组配对平均 SM 频率差约 12.24% / 11.67%，不满足可比性门槛；其余配对差绝对值小于 0.46%。
- 各配置相对标准差约 7.64%～27.70%，测量噪声偏高。表中小差异不是可靠的优化机会或性能回归结论。
- 编译 12.21 秒、链接 0.87 秒；三个测量进程合计约 8.19 秒（含其 CPU 检查等开销），不是整个调查的墙钟耗时。

决定：**本机本轮没有找到明显、值得继续投入的标记分布异常，暂不推进此候选**。这不证明所有数据类型、保留比例、分布和架构均不存在优化空间。不为解释小差异继续复测、profiling 或修改策略。

## 环境、复现与证据

- WSL CCCL-Ubuntu，RTX 4060 Laptop，CUDA 13.3 / sm89。
- CCCL HEAD `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`，实验前后工作树干净。
- Windows 插电、100% 电量、Turbo；各轮前后验证 Turbo GUID。
- 使用已有 NVBench 库和既有编译参数；未触发 CMake 重配置或下载。
- 源码：`evidence/phase2/select_distribution.cu`。
- 驱动：`evidence/phase2/run_select_distribution.py`；复用既有审计及环境帮助代码。
- 完整参数、源码/二进制/NVBench 哈希、原始 JSON、markdown、stdout/stderr：`evidence/raw/phase2/2026-09-07-select-distribution/`。生成的 build 目录不纳入 Git。

PowerShell 复现（必须指定一个不存在的新输出目录；脚本不覆盖旧证据）：

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/run_select_distribution.py' '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/select-distribution-recheck'
```

上游排重仅做初筛：`repo:NVIDIA/cccl is:pr in:title select` 最近 30 项，以及 `repo:NVIDIA/cccl "select" "distribution" in:title,body is:issue` 的两项结果；未发现直接同题并不等于不存在。本候选因效果门槛失败，未扩展排重。

## 下个小阶段

维持“先短测，明显差距才深入”的筛选方式，转查 DeviceScan 的规模/类型与调度切换；先检查上游是否已覆盖，再决定最小基线矩阵。它目前只是待筛方向，未发现问题、未实现优化。本轮不延长实验寻找正结果。
