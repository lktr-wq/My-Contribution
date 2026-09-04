## 2026-09-04 首轮静态收集

- URL: https://github.com/NVIDIA/cccl/blob/main/CONTRIBUTING.md
  - 标题: Contributing to CCCL
  - 类型: 官方文档
  - 对什么问题有用: 对确认 CCCL 贡献流程、CUB 性能改动的 SASS 检查和 benchmark 回归要求有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/contributors/how_tos/install_build_test.html
  - 标题: Install, Build, Test
  - 类型: 官方文档
  - 对什么问题有用: 对复现 CCCL 官方构建、定向测试、benchmark compare 和 git bisect 工作流有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/cub/benchmarking.html
  - 标题: CUB Benchmarks
  - 类型: 官方文档
  - 对什么问题有用: 对建立 CUB 修改前后 NVBench 基线、保存 JSON、比较噪声与性能回归以及用 Nsight Compute profiling 有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/cub/tuning_infra.html
  - 标题: Automated Tuning Infrastructure
  - 类型: 官方文档
  - 对什么问题有用: 对搜索 threads-per-block、items-per-thread 等参数空间并验证不同 workload 与架构的 tuning 结果有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/cub/tuning.html
  - 标题: CUB Tunings
  - 类型: 官方文档
  - 对什么问题有用: 对理解 CUB policy selector、架构回退和算法参数如何影响性能而不改变功能语义有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/cub/developer/device_scope.html
  - 标题: CUB Device-scope Developer Overview
  - 类型: 官方文档
  - 对什么问题有用: 对定位 Device 级算法的 dispatch、agent、policy 与架构 tuning 分层有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/cub/api/structcub_1_1DeviceReduce.html
  - 标题: cub::DeviceReduce API
  - 类型: 官方文档
  - 对什么问题有用: 对核对 DeviceReduce 的公开接口、确定性、问题规模与调度行为边界有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://nvidia.github.io/cccl/unstable/cub/api/structcub_1_1DeviceScan.html
  - 标题: cub::DeviceScan API
  - 类型: 官方文档
  - 对什么问题有用: 对理解 DeviceScan 的 decoupled look-back 历史、数据移动目标和公开行为边界有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://github.com/NVIDIA/cccl/releases/tag/v3.4.0
  - 标题: CCCL v3.4.0
  - 类型: 官方Release
  - 对什么问题有用: 对确认 Blackwell DeviceScan warp-specialized/TMA 性能变化及当前 CUB API 演进有用。
  - 时间范围: 2026-07-16。

- URL: https://github.com/NVIDIA/cccl/pull/8407
  - 标题: Workaround nvc++ crash in warpspeed scan
  - 类型: 已合并PR
  - 对什么问题有用: 对观察维护者如何接受一个由小规模输入触发的 warpspeed scan 边界问题修复及其 CI 验证有用。
  - 时间范围: 2026-04-14 合并。

- URL: https://github.com/NVIDIA/cccl/pull/8642
  - 标题: Rewire binary search to transform with a small linear search
  - 类型: 已合并PR
  - 对什么问题有用: 对观察 CUB 用算法复用与小规模线性尾段优化 binary search 的已接受改动及测试要求有用。
  - 时间范围: 2026-04-23 合并。

- URL: https://github.com/NVIDIA/cccl/issues/8334
  - 标题: SM120 warpspeed DeviceScan small-N out-of-bounds report
  - 类型: 已关闭Issue
  - 对什么问题有用: 对查看小规模边界 shape 的完整复现、IR/PTX/SASS 线索及其与已合并修复 PR #8407 的关联有用。
  - 时间范围: 2026-04-08 提出；2026-04-14 前后关闭。

- URL: https://github.com/NVIDIA/cccl/issues/10577
  - 标题: Improve performance of DeviceSegmentedSort
  - 类型: 开放Issue
  - 对什么问题有用: 对了解分段长度分桶、过度填充、host round-trip、负载不均和 latency workload 的维护者问题清单有用。
  - 时间范围: 2026-08-01 提出；2026-09-04 核对为开放。

- URL: https://github.com/NVIDIA/cccl/issues/10661
  - 标题: DeviceSegmentedSort workload and feature prioritization
  - 类型: 开放Issue
  - 对什么问题有用: 对了解维护者正在征集的 segment 分布、数据类型、GPU 架构以及 latency/throughput 优先级证据有用。
  - 时间范围: 2026-08-05 提出；2026-09-04 核对为开放。

- URL: https://github.com/NVIDIA/cccl/issues/6792
  - 标题: Investigate fine-grained bucket sizes for SegmentedSort
  - 类型: 开放Issue
  - 对什么问题有用: 对研究细粒度分桶在减少浪费、增加 launch/occupancy 尾部成本和缓存局部性之间的取舍有用。
  - 时间范围: 2025-11-26 提出；2026-09-04 核对为开放。

- URL: https://github.com/NVIDIA/cccl/issues/8789
  - 标题: Support device-resident problem sizes in CUB device-level algorithms
  - 类型: 开放Issue
  - 对什么问题有用: 对比较 DeviceRadixSort、DeviceScan 在 Ada/B200 上面对小规模固定开销、CDP、Occupancy 与同步代价的实测资料有用。
  - 时间范围: 2026-05-03 提出；2026-09-04 核对为开放。

- URL: https://github.com/NVIDIA/nvbench
  - 标题: NVIDIA/NVBench
  - 类型: 官方文档
  - 对什么问题有用: 对确认 NVBench 的适用范围、cold/batch measurement、参数扫描、吞吐量和时钟控制能力有用。
  - 时间范围: 持续更新；2026-09-04 核对。

- URL: https://github.com/NVIDIA/nvbench/blob/main/docs/benchmarks.md
  - 标题: NVBench Benchmarks
  - 类型: 官方文档
  - 对什么问题有用: 对设计覆盖小规模、不规则规模、数据类型和运行参数的 benchmark axes 与计时区间有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://github.com/NVIDIA/nvbench/issues/150
  - 标题: Investigate refined benchmark sample stopping criterion
  - 类型: 已关闭Issue
  - 对什么问题有用: 对理解非正态和多峰测量分布下方差停止条件的局限，以及为何要改进噪声判定有用。
  - 时间范围: 2023-12-13 提出；关闭日期待核实。

- URL: https://github.com/NVIDIA/nvbench/releases/tag/python-0.3.0
  - 标题: NVBench Python Library v0.3.0
  - 类型: 官方Release
  - 对什么问题有用: 对追踪 entropy/stdrel、warmup、sample-count 和 robust compare 等当前 benchmark 稳定性能力有用。
  - 时间范围: 2026-08-05。

- URL: https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html
  - 标题: Nsight Compute Profiling Guide
  - 类型: 官方文档
  - 对什么问题有用: 对判断 metric replay、cache/clock 控制、序列化和 profiler 开销如何影响性能证据可信度有用。
  - 时间范围: Nsight Compute 13.3 文档；2026-09-04 核对。

- URL: https://developer.nvidia.com/nvidia-development-tools-solutions-err_nvgpuctrperm-permission-issue-performance-counters
  - 标题: ERR_NVGPUCTRPERM permission guidance
  - 类型: 官方文档
  - 对什么问题有用: 对识别性能计数器权限不足并界定 Windows、Linux、容器环境下可验证的 profiling 证据有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://docs.nvidia.com/nsight-compute/ReleaseNotes/topics/system-requirements.html
  - 标题: Nsight Compute System Requirements
  - 类型: 官方文档
  - 对什么问题有用: 对核对 WSL2、驱动版本、宿主机性能计数器权限和受支持 profiling 环境有用。
  - 时间范围: Nsight Compute 13.3 文档；2026-09-04 核对。

- URL: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html
  - 标题: CUDA C++ Best Practices Guide
  - 类型: 官方文档
  - 对什么问题有用: 对解释 block 大小、寄存器压力、Occupancy、ILP、访存合并和带宽之间的基础取舍有用。
  - 时间范围: CUDA 13.3 文档；2026-09-04 核对。

- URL: https://docs.nvidia.com/cuda/cuda-binary-utilities/
  - 标题: CUDA Binary Utilities
  - 类型: 官方文档
  - 对什么问题有用: 对使用 cuobjdump/nvdisasm 获取 SASS、资源用量和控制流信息并比较生成代码有用。
  - 时间范围: CUDA 13.3 文档；2026-09-04 核对。

- URL: https://docs.nvidia.com/vgpu/latest/grid-vgpu-user-guide/modifying-vgpu-configuration.html
  - 标题: Enabling CUDA Toolkit Profilers for NVIDIA vGPU
  - 类型: 官方文档
  - 对什么问题有用: 对判断 vGPU 中 profiler 开关、全局计数器、锁频和单 VM 限制如何影响 profiling 可信度有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/profiler.html
  - 标题: CUTLASS Profiler
  - 类型: 官方文档
  - 对什么问题有用: 对参考 shape sweep、kernel 枚举、固定 shape 搜索、验证和 CSV 输出的性能测量设计有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/gemm_performance_measurement_methodology_guidelines.html
  - 标题: GEMM Performance Measurement Methodology Guidelines
  - 类型: 官方文档
  - 对什么问题有用: 对建立包含 warmup、稳定时钟、L2 行为、最小 launch 间隙和可复核指标的 benchmark 方法有用。
  - 时间范围: 持续更新；最后更新时间待核实（2026-09-04 核对）。

- URL: https://research.nvidia.com/publication/2016-03_single-pass-parallel-prefix-scan-decoupled-look-back
  - 标题: Single-pass Parallel Prefix Scan with Decoupled Look-back
  - 类型: 论文
  - 对什么问题有用: 对理解 CUB DeviceScan 单遍扫描、约 2N 数据移动与用有限冗余工作隐藏全局前缀传播延迟的原始依据有用。
  - 时间范围: 2016-03-01。

- URL: https://developer.nvidia.com/gtc/2020/video/s21572-vid
  - 标题: A Faster Radix Sort Implementation
  - 类型: 官方会议演讲
  - 对什么问题有用: 对理解 OneSweep/decoupled look-back 如何减少 radix sort 分区阶段的数据移动并与 CUB 基线比较有用。
  - 时间范围: GTC 2020。
