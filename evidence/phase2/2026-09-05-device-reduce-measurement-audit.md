# DeviceReduce 测量可信度审计（2026-09-05）

## 结果与范围

没有发现已确证的 CUB 缺陷，也没有实施优化。已修订旧报告对 `SAME` 的过度解读，并完成有界预热对照。小规模结果仍不适合声称几个百分点的优化；大规模可进入源码引导的探索，但正式结论仍需修改前后交错对照与正确性验证。

- CCCL：`/home/lktr/src/cccl`，HEAD `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`，源码未修改。
- NVBench：`410dcdd21c9b48191ecb3d3d77060b1bf4ac6244`，实际依赖源码工作树无修改。
- RTX 4060 Laptop，WSL2 `CCCL-Ubuntu`，使用既有 `cub.bench.reduce.sum.base`，无下载或重建。
- 脚本：[audit_reduce_measurements.py](audit_reduce_measurements.py)，仅 Python 标准库。
- 新证据：`evidence/raw/phase2/2026-09-05-warmup-audit/`。manifest 保存二进制 SHA256、两个 HEAD、完整命令、库路径、GPU 前后快照、逐轮电源模式、退出码与指标。每轮保存 JSON、Markdown、stdout、stderr。

## 实际源码核查

以下路径相对 `build/cub-benchmark/_deps/nvbench-src/`：

- `python/scripts/nvbench_compare.py`：用均值差与较小的相对样本标准差决定 `SAME`，不是统计显著性检验。相同代码两轮都存在的稳定瓶颈也不会由此排除。
- `nvbench/detail/measure_cold.cu`：先检查停止准则，再检查 walltime 超时；被判定 throttle 的单次测量不加入结果，已经接受的其他测量保留。
- `nvbench/detail/measure_timeout_warnings.cuh`：警告取决于 max-noise、min-time、最少样本等条件，没有无条件的通用超时警告。
- `nvbench/detail/entropy_criterion.cxx`：参数为 max-angle、min-r2，不保证低相对标准差。满足最少样本后，因时间上限结束也可能没有超时警告。
- `nvbench/detail/sample_count_criterion.cxx`：目标是接受的样本数量，不等于“已收敛”。
- `nvbench/detail/measure_cold_launch_timer_core.cuh`：CUDA event 计时之前清理 L2 并同步，然后安排 blocking kernel、频率测量和 event。cold GPU Time 不能简单称为包含全部主机调用开销的端到端时间。

## 旧两轮 JSON 审计

检查配置键唯一、未跳过、所需指标存在且有限、时间与样本量为正。原文件未修改。

| 指标 | Run 1 | Run 2 |
|---|---:|---:|
| 配置数 | 80 | 80 |
| GPU 相对标准差 > 5% | 78 | 79 |
| GPU 相对标准差 > 20% | 66 | 61 |
| cold walltime >= 15 秒 | 5 | 4 |
| 接受样本数范围 | 328–1390 | 370–1336 |

标准差描述单次采样分布，不是优化幅度误差条，不能直接反推均值或中位数的检出阈值。

达到时间边界的配置均为 Elements=2^28（以下前者为 T，后者为 OffsetT）：

- Run 1：I64/I32、I64/I64、I128/I32、I128/I64、C32/I64。
- Run 2：I128/I32、I128/I64、F64/I32、C32/I32。

JSON 不保存实际停止原因，因此只标记“达到时间边界、收敛未获确认”，不将它们全部断言为超时终止：停止准则也可能恰在该轮满足。

原始文件 SHA256：

- Run 1：`a00a9f4004290c45c705b9f4f4ca3545b806d907383de1e5c6465901c33d3c88`
- Run 2：`daced3ddc95a3dbeb07ad227f0f20510b0de59160d7909f0f2fba60eb8ea8420`

## 短复测：增加预热能否改善波动

开始检查发现 Windows 为 Silent；用户确认插电并切回增强后，验证为 Turbo。六轮前后均检查同一 Turbo GUID，未自动改变电源、代理或驱动。没有连续频率/温度时间线，不能声称整段硬件状态被锁定。

- T=I32、OffsetT=I32，Elements=2^16 与 2^24。
- 使用 sample-count，每配置 1000 个接受样本，timeout=15 秒。
- A=1 次预热，B=20 次预热；独立进程顺序 A、B、B、A、A、B，各三轮。进程内仍先小规模再大规模，未打乱规模顺序。
- 保存所有轮次，不剔除慢轮；遇 deadlock、非零退出、样本未达目标或电源模式变化则停止。
- 固定样本量用于本次诊断可比性，不能与旧 entropy 轮混合后宣称性能改善。

六个 benchmark 进程分别约 1.42、1.22、1.22、1.32、1.22、1.22 秒；12/12 配置均收满 1000 样本，无时间边界配置，退出码均为 0。stdout/stderr/Markdown 未检出 deadlock。Run 1 小规模出现一次 throttle 警告（1571.58 MHz，默认频率约 70%），对应 trial 被丢弃；保留该轮并标注，不当成纯净测量。

| Elements | 预热次数 | 三轮 GPU median（微秒） | median 跨轮跨度 | 单轮相对标准差范围 |
|---|---:|---|---:|---:|
| 2^16 | 1 | 15.648 / 15.520 / 16.384 | 5.52% | 62.81–95.66% |
| 2^16 | 20 | 16.384 / 15.392 / 16.384 | 6.05% | 60.29–75.68% |
| 2^24 | 1 | 372.736 / 372.544 / 372.736 | 0.052% | 3.91–7.46% |
| 2^24 | 20 | 373.760 / 372.736 / 373.760 | 0.274% | 2.88–3.83% |

跨度定义为 `(max(三轮 median)-min(三轮 median))/median(三轮 median)`，不是置信区间或未来误差上限。小规模单轮 IQR/median 为 34.02–59.88%，不能仅归为偶发极端长尾。大规模六轮 median 范围为 372.544–373.760 微秒。

20 次预热未表现出小规模波动的稳定改善；不据此断言所有预热方法都无效。大规模本窗口中心位置较稳定，但只有两个规模、每设置三次进程，未测修改版本，不能宣称建立了 1% 检出能力。没有样本级时间序列，尚不能定位调度、频率、驱动或计时路径中的因果来源。

## 复现与下一步

WSL 入口，输出目录必须不存在，以防覆盖证据：

```bash
python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/audit_reduce_measurements.py' \
  --probe-dir '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/<new-unique-directory>'
```

只读审计：同一脚本不带 --probe-dir，将两个旧完整 JSON 路径作为位置参数；标准输出包含汇总、输入 SHA256、逐配置指标。

下一阶段先沿固定版本 DeviceReduce sum 源码梳理实际策略分派、每 tile 元素量和多阶段路径，再选少量非 2 的幂与路径切换边界。优先探索可测的大规模范围；若只有小幅差异，先解决可测性，不直接给优化结论。候选现象独立复现后再考虑最小修改和修改前后交错比较。不租卡、不公开提交、不扩大到全仓库 benchmark。
