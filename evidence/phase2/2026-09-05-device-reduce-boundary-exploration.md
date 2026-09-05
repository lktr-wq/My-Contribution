# DeviceReduce 源码引导的边界探索（2026-09-05）

## 结论

完成 9 个合法输入规模、3 种顺序、共 27 条正式测量，每条 1000 个接受样本。没有修改上游源码，没有发现足以进入修复阶段的性能问题。

- 4096 → 4097 确实从单 kernel 切换为两阶段归约，各轮 median 都增加，但小规模噪声高；不能从这次观测断言阈值不合理。
- 2^24 附近的完整/残余 tile 输入，本次 median 没有明显陡降。这个负结果只覆盖 I32/I32、指定规模和本机短窗口，不排除其他输入或小幅差异。
- 不把 benchmark 运行成功当作正确性检查：官方程序本轮未将输出与 CPU oracle 比较，未运行新的正确性测试。

## 固定条件与产物

- CCCL HEAD：`f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`；WSL `/home/lktr/src/cccl` 前后工作树无修改。
- NVBench HEAD：`410dcdd21c9b48191ecb3d3d77060b1bf4ac6244`。
- 既有官方程序：`/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base`。
- 二进制 SHA256：`950d9d1185acd25762a29a4210fb4d4b2ec35f83b0feffefdb5e3081e671c13f`。
- GPU：RTX 4060 Laptop，compute capability 8.9，24 SM；WSL2 CCCL-Ubuntu。
- 所有进程前后验证 Windows 为 Turbo；未改变电源设置、代理或驱动，没有下载或重建。
- 脚本：[probe_reduce_boundaries.py](probe_reduce_boundaries.py)，复用 [audit_reduce_measurements.py](audit_reduce_measurements.py) 的解析器。
- 原始证据：`evidence/raw/phase2/2026-09-05-reduce-boundaries/`。含 manifest、每轮 JSON/Markdown/stdout/stderr、源码文件 SHA256、完整命令、实际顺序、警告、GPU 前后快照与退出码。

## 从代码到实际执行路径

以下源码位置相对 `CCCL_CUB/`，版本以上述 HEAD 为准：

1. `cub/benchmarks/bench/reduce/sum.cu` 和 `base.cuh:44`：名为 sum 的 benchmark 实际调用 `DeviceReduce::Reduce`，传入 `cuda::std::plus<>` 和零初值。T=I32、OffsetT=I32。没有改用手写 kernel。
2. `nvbench_helper/nvbench_helper/nvbench_helper.cuh:769` 仅配置 stream 和缓存 allocator；未覆盖 determinism。`cub/cub/device/device_reduce.cuh:299` 默认 run-to-run 路线，不是原子 nondeterministic 路线。
3. `cub/cub/device/dispatch/tuning/tuning_reduce.cuh:462` 与 `cub/cub/util_arch.cuh:153`：sm_89 的 I32 使用 256 threads × 16 items/thread，vec_size=4，BLOCK_REDUCE_WARP_REDUCTIONS，LOAD_LDG。单 tile=4096 元素。
4. `cub/cub/device/dispatch/dispatch_reduce.cuh:1021`：N<=4096 走 SingleTile；更大走两阶段。
5. 同文件 `:716` 查询第一阶段 kernel 的最大驻留 block 数，乘 SM 数与 subscription_factor=5 得到 grid 上限。`cub/cub/grid/grid_even_share.cuh:118` 取 `min(ceil(N/4096), max_blocks)`。
6. `cub/cub/agent/agent_reduce.cuh:431` 实际选择 STRIP_MINE，block 按 grid×tile 步长跨 tile 消费；不能照搬 GridEvenShare 顶部“连续均分”的概括当作本路径行为。完整 tile 可走向量加载，残余 tile 使用带有效元素判断的处理，见 `:353`、`:446`。

使用现有运行时开关 `CCCL_EXPERIMENTAL_LOGGING=1` 配合 `--profile` 验证分派，不需重编译。这一轮关闭部分测量干扰，且有日志开销，只用来验证路径，不纳入性能表。

`dispatch-trace.stdout.log` 的实际记录：

| N | 第一阶段 | 第二阶段 | 日志行 |
|---:|---|---|---:|
| 4095 | SingleTile，1×256 threads | 无 | 35 |
| 4096 | SingleTile，1×256 threads | 无 | 47 |
| 4097 | Reduce，2×256 threads | SingleTile，1×256 | 59–60 |
| 16777216 | Reduce，720×256 threads | SingleTile，1×256 | 72–73 |
| 16777217 | Reduce，720×256 threads | SingleTile，1×256 | 85–86 |

日志报告的 6 SM occupancy 是每 SM 最大驻留 block 数的查询结果，不是 profiler 实测占用率。结合 24 SM 和 factor=5，grid 上限=720。公式推导：N=719×4096+1=2,945,025 时 grid 首次达到 720；N=720×4096+1=2,949,121 时 tile 数首次超过 grid 上限，至少一个 block 开始处理额外 tile。本轮未测这两个边界。N=2^24 与 N+1 的 grid 同为 720，不能将此处称为 kernel 数量切换。

## 正式测量设计

正式轮显式设置 `CCCL_EXPERIMENTAL_LOGGING=0`，不使用 --profile。每配置预热 20 次，sample-count=1000，timeout=15 秒。沿用 cold/no_batch；预热次数不是消除噪声的保证。

固定 9 个点：4095、4096、4097、N-4096、N-1、N、N+1、N+4095、N+4096，其中 N=2^24。后六点的输入字节量相差不到 0.05%，用于粗查尾块性能陡降，不是相同工作量的优化前后比较。

三种顺序：升序、降序、从 N-1 开始循环移位。manifest 中的 sizes_actual 验证实际顺序与请求一致。没有挑选最优轮或删除慢轮。只改 Elements 的合法值，不引入越界、错误长度或指针错位。

进程耗时：路径日志 0.57 秒，正式三轮 4.68、4.73、4.83 秒（不含外围环境查询）。四个进程退出码均为 0；正式 27/27 配置样本=1000，无时间边界配置，无 deadlock。第三轮 N=4095 有一次 throttle 警告（1461.83 MHz，约默认频率 65%），对应测量被 NVBench 丢弃，警告及该轮结果均保留。

## 结果

单位为 GPU 时间微秒；范围均为三轮的已观测值，不是置信区间。

| 元素数 | Round 1 median | Round 2 median | Round 3 median | 单轮相对标准差范围 |
|---:|---:|---:|---:|---:|
| 4095 | 13.312 | 14.336 | 14.464 | 67.86–99.03% |
| 4096 | 14.336 | 13.312 | 14.336 | 52.70–93.82% |
| 4097 | 18.432 | 17.408 | 16.448 | 60.61–76.60% |
| 16773120 | 371.712 | 372.736 | 372.736 | 2.12–3.48% |
| 16777215 | 372.736 | 372.736 | 371.712 | 2.81–5.04% |
| 16777216 | 372.736 | 372.736 | 372.736 | 3.19–3.87% |
| 16777217 | 372.736 | 372.736 | 371.712 | 2.96–4.45% |
| 16781311 | 372.736 | 372.736 | 372.736 | 2.19–3.99% |
| 16781312 | 372.736 | 372.736 | 372.736 | 1.97–3.63% |

小规模：4097 相较 4096 的 median 各轮增加约 28.57%、30.77%、14.73%。这是实现路径变化附近的描述性结果，不能把比例当作可实现的优化幅度。尚未用“强制单 kernel 处理 4097”对照，不能认定多 kernel 是全部时差的唯一原因，更不能认定当前阈值有缺陷。

大规模：18 条 median 位于 371.712–372.736 微秒，均值位于 372.273–373.731 微秒。没有观察到明显的残余 tile 陡降，因此暂不沿这个点做优化。中位数相同也不意味着时间完全相同、测量无噪声或可排除亚百分比差异。

## 复现与下一阶段

在 WSL 中执行，输出目录必须为新的唯一路径，脚本拒绝覆盖：

```bash
python3 -B '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/probe_reduce_boundaries.py' \
  '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/<new-unique-directory>'
```

下一候选是明确的 grid 上限及 block 循环工作量变化：根据本次记录的 720 blocks，选择 2,949,120 与其少量整数倍附近的合法输入，用同样交错重复方法探索。它与本轮“2^24 尾 tile”假设不同。先验证现象，再决定是否需要最小对照实现；若仍没有可重复、超出测量波动的异常，记录负结果并换候选，不强造贡献。仍不租卡、不公开发布、不重跑整个矩阵。
