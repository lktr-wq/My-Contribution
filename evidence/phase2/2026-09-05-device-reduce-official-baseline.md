# CUB DeviceReduce 官方基线（2026-09-04 至 2026-09-05）

> 2026-09-05 审计修订：保留原始结果，撤回从 `SAME` 推导“无统计显著异常”的表述。见 [测量可信度审计](2026-09-05-device-reduce-measurement-audit.md)。

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

两轮 JSON 均得到 80/80 条未跳过结果。保存的 Markdown 中未发现 OOM 或 deadlock；但没有单独持久化进程 stdout/stderr，不能仅凭 Markdown 排除绕过打印器的设备端警告。Run 1 出现 5 次 throttle warning，Run 2 出现 1 次。源码表明 NVBench 丢弃被判定降频的单次测量，保留其他已接受样本，不是清空整个配置重测。平均 SM clock scaling 约为默认时钟的 104% 至 115%，不能证明每个时刻都稳定。

Run 1 的 5 个、Run 2 的 4 个配置，其 cold walltime 达到或超过 15 秒。这些配置的 entropy 收敛未获确认；JSON 未保存实际停止原因。

## 重复性分析

独立解析两轮 JSON，并按 `T × OffsetT × Elements` 对齐。使用 GPU median 检查长尾样本之外的中心位置：

| Elements | 配置数 | 两轮 median 绝对差均值 | 最大值 |
|---:|---:|---:|---:|
| `2^16` | 20 | 7.65% | 26.04% |
| `2^20` | 20 | 4.21% | 21.43% |
| `2^24` | 20 | 0.27% | 1.57% |
| `2^28` | 20 | 0.15% | 1.29% |

小规模 kernel 的均值、median 和 relative noise 显示明显波动；调度、时钟等原因尚未隔离验证。大规模仅在这两轮的 median 上接近，不能推导完整分布稳定或细小性能差异可检出。

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

- 已获得两轮相同代码的测量；尚未完成性能异常检出能力验证；
- 两个大规模点的跨轮 median 接近，I32/I64 offset 的已观测表现接近；
- 小规模点噪声较大，不能直接解释为 CUB 性能缺陷；
- 80 个 `SAME` 只代表满足该脚本的噪声阈值规则，不是统计显著性检验。

`SAME` 条件为 `abs((cmp_mean - ref_mean) / ref_mean) <= min(ref_noise, cmp_noise)`。noise 是样本标准差除以均值，不是均值差的置信区间。命令中的 `--threshold-diff 0.05` 不能把这个条件解释为“差异小于 5%”。

当前只能表述为“默认 80 个配置完成两轮测量并保存，但部分配置噪声较大或停止原因不确定，尚不能据此判断 CUB 有无性能问题”。先审计测量可信度，再按源码选择少量合法输入边界。未比较其他实现或修改版本，也未验证优化；不能把噪声包装成性能问题。
