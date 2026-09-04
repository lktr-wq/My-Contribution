# CUB DeviceReduce benchmark 构建（2026-09-04）

## 固定输入

- WSL 工作副本：`/home/lktr/src/cccl`
- 上游：`https://github.com/NVIDIA/cccl.git`
- 分支：`main`
- commit：`f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`
- GPU：RTX 4060 Laptop，Ada `sm_89`
- CUDA/NVCC：13.3 / `13.3.73`
- host compiler：GCC/G++ `13.3.0`
- Ninja：`1.11.1`
- C++/CUDA standard：C++17
- benchmark framework：CCCL 固定的 NVBench commit `410dcdd21c9b48191ecb3d3d77060b1bf4ac6244`

## 配置与环境补齐

使用官方 preset `cub-benchmark`，并将 CUDA 架构限制为本机 `89`：

```bash
/home/lktr/.local/opt/cmake-4.4.3-linux-x86_64/bin/cmake \
  --preset cub-benchmark \
  -DCMAKE_CUDA_ARCHITECTURES=89 \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DCMAKE_CUDA_HOST_COMPILER=/usr/bin/c++
```

首次配置暴露出 benchmark 路径比正确性测试需要更多开发依赖：

1. NVBench 拉取的 `rapids-cmake` 要求 CMake `>=4.0`，因此新增经 Kitware SHA-256 清单校验的用户目录 CMake `4.4.3`；系统 CMake 和已有 CMake `3.31.12` 均未替换。
2. `CUDA::nvml` 缺失：安装 `cuda-nvml-dev-13-3` `13.3.29-1`。WSL NVML 运行库原本已存在，未安装 Linux NVIDIA 驱动。
3. `CUDA::curand` 缺失：安装 `libcurand-13-3` 与 `libcurand-dev-13-3` `10.4.3.29-1`。
4. `cuda_profiler_api.h` 缺失：安装 `cuda-profiler-api-13-3` `13.3.27-1`。CUPTI 运行库和开发包原本已存在。

这些均为构建环境修正；没有修改 CCCL 或 NVBench 源码，也没有跳过上游检查。

最终配置结果：

```text
NVBench CUDA architectures: 89
CTK version: 13.3.73
Configuring done (430.8s)
Generating done (0.2s)
Build files have been written to: /home/lktr/src/cccl/build/cub-benchmark
```

## 最小构建目标

只构建官方 DeviceReduce sum 基线目标，不构建全量 benchmark：

```bash
/home/lktr/.local/opt/cmake-4.4.3-linux-x86_64/bin/cmake \
  --build --preset cub-benchmark \
  --target cub.bench.reduce.sum.base \
  --parallel 2
```

第一次编译在第 3/46 步因缺少 `cuda_profiler_api.h` 停止。补齐对应开发包后增量重试，`44/44` 步骤完成并生成：

```text
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base
```

## 非性能启动验证

产物是 x86-64 Linux ELF，可正常执行 `--help`：

```text
NVBench v0.1.0 (HEAD:python-0.3.0-7-g410dcdd)
```

`cuobjdump --list-elf` 确认其中包含三个 `sm_89` cubin：

```text
cub.bench.reduce.sum.1.sm_89.cubin
cub.bench.reduce.sum.2.sm_89.cubin
cub.bench.reduce.sum.3.sm_89.cubin
```

## 结论与边界

当前 WSL2 + CUDA 13.3 环境已成功配置并构建官方 CUB DeviceReduce sum NVBench 基线目标，且产物能够启动并包含面向本机 Ada `sm_89` 的 CUDA 代码。

本阶段没有运行 benchmark workload，因此没有吞吐量、延迟、带宽、方差或 profiler counter 数据。当前只能表述为“官方 benchmark 已构建并通过非性能启动验证”，不能表述为“性能测试已完成”或“已发现性能问题”。
