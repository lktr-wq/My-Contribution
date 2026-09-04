# CUB DeviceReduce 官方基线（2026-09-04 至 2026-09-05）

## 目标与固定条件

- 上游工作副本：`/home/lktr/src/cccl`
- commit：`f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`
- benchmark：`cub.bench.reduce.sum.base`
- NVBench：CCCL 固定 commit `410dcdd21c9b48191ecb3d3d77060b1bf4ac6244`
- GPU：RTX 4060 Laptop，Ada `sm_89`，24 SM，8 GiB
- CUDA/NVCC：13.3 / `13.3.73`
- Windows/华硕运行模式：`Turbo`（华硕控制面板显示“增强”）
- 测量方式：GPU 0、NVBench `entropy` stopping criterion
- 比较脚本表格依赖：Ubuntu `python3-tabulate` `0.8.10-1`
- 原始输出：每轮同时保存 NVBench JSON 和 Markdown

官方程序列出 80 个默认配置：

- `T{ct}`：I8、I16、I32、I64、I128、F32、F64、C32、F16、BF16；
- `OffsetT{ct}`：I32、I64；
- `Elements{io}`：`2^16`、`2^20`、`2^24`、`2^28`。

## 环境烟雾轮

最初在 Windows `Silent` 电源方案下运行 I32 子集（8 个配置）。这轮出现：

- 一次 `Possible Deadlock Detected`；
- 一次 GPU throttle warning；
- GPU relative noise 为 7.71% 至 193.37%。

该轮仅作为失败环境记录，不是有效性能基线：

- `evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-sm89.json`
- `evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-sm89.md`

用户在华硕控制面板切换至“增强”后，Windows 实际电源方案变为 `Turbo`。相同 I32 子集复跑不再出现 deadlock 或 throttle warning，`2^24` 与 `2^28` 的跨轮 GPU 时间差约为 0.1% 至 2%。

- `evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-turbo-sm89.json`
- `evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-turbo-sm89.md`

## 两轮完整官方基线

两轮均执行：

```bash
./bin/cub.bench.reduce.sum.base \
  -d 0 \
  --stopping-criterion entropy \
  --json <run.json> \
  --md <run.md>
```

结果文件：

- Run 1：
  - `evidence/raw/phase2/2026-09-04-cub-reduce-sum-official-full-run1-turbo-sm89.json`
  - `evidence/raw/phase2/2026-09-04-cub-reduce-sum-official-full-run1-turbo-sm89.md`
- Run 2：
  - `evidence/raw/phase2/2026-09-05-cub-reduce-sum-official-full-run2-turbo-sm89.json`
  - `evidence/raw/phase2/2026-09-05-cub-reduce-sum-official-full-run2-turbo-sm89.md`

两轮均得到 80/80 条结果，没有 OOM、deadlock 或失败配置。Run 1 出现 5 次 throttle warning，Run 2 出现 1 次；NVBench 明确丢弃对应 trial 后重新测量。所有配置记录的平均 SM clock scaling 仍约为默认时钟的 104% 至 115%。

## 重复性分析

独立解析两轮 JSON，并按 `T × OffsetT × Elements` 对齐。使用 GPU median 检查长尾样本之外的中心位置：

| Elements | 配置数 | 两轮 median 绝对差均值 | 最大值 |
|---:|---:|---:|---:|
| `2^16` | 20 | 7.65% | 26.04% |
| `2^20` | 20 | 4.21% | 21.43% |
| `2^24` | 20 | 0.27% | 1.57% |
| `2^28` | 20 | 0.15% | 1.29% |

小规模 kernel 的均值、median 和 relative noise 均明显受调度与长尾影响；大规模配置的跨轮重复性良好。

使用 CCCL 构建目录内随附的官方比较脚本：

```bash
PYTHONPATH=./_deps/nvbench-src/python/scripts \
python3 ./_deps/nvbench-src/python/scripts/nvbench_compare.py \
  --no-color \
  --threshold-diff 0.05 \
  <run1.json> <run2.json>
```

官方比较结果：

```text
Total Matches: 80
Pass (diff <= min_noise): 80
Unknown (infinite noise): 0
Failure (diff > min_noise): 0
```

以 I32 为例，Run 1 的大规模带宽表现为：

| OffsetT | Elements | GlobalMem BW | BWUtil |
|---|---:|---:|---:|
| I32 | `2^24` | 182.39 GB/s | 71.24% |
| I64 | `2^24` | 180.87 GB/s | 70.65% |
| I32 | `2^28` | 199.76 GB/s | 78.02% |
| I64 | `2^28` | 198.80 GB/s | 77.65% |

## 当前结论与边界

在本机 Ada `sm_89`、当前 CCCL commit 和官方默认 DeviceReduce sum axes 下：

- 尚未发现可重复、统计上显著的性能异常；
- 两个大规模点在两轮间稳定，I32/I64 offset 表现接近；
- 小规模点存在显著测量噪声，但方向不稳定，不能解释为 CUB 性能缺陷；
- 官方比较工具把 80 个配置全部判定为 `SAME`。

因此当前只能表述为“官方 DeviceReduce sum 基线已在本机完整跑通并保存；默认 axes 暂未发现稳定异常”。下一阶段如果继续寻找问题，应扩大合法输入覆盖（尤其是 policy 边界附近和非 2 的幂规模），并对候选点进行交错重复测量；不能把本轮小规模噪声包装成性能问题。
