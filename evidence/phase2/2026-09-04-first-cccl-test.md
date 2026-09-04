# CCCL/CUB 首个官方正确性测试（2026-09-04）

## 固定输入

- WSL 工作副本：`/home/lktr/src/cccl`
- 上游：`https://github.com/NVIDIA/cccl.git`
- 分支：`main`
- commit：`f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`
- 工作树：测试前后无源码修改
- GPU：RTX 4060 Laptop，Ada `sm_89`
- CUDA/NVCC：13.3 / `13.3.73`
- host compiler：GCC/G++ `13.3.0`
- CMake：Kitware `3.31.12`
- Ninja：`1.11.1`
- C++/CUDA standard：C++17

## 配置

使用官方 preset `cub-cpp17`，架构限制为本机 `89`：

```bash
/home/lktr/.local/opt/cmake-3.31.12-linux-x86_64/bin/cmake \
  --preset cub-cpp17 \
  -DCMAKE_CUDA_ARCHITECTURES=89 \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DCMAKE_CUDA_HOST_COMPILER=/usr/bin/c++
```

最终缓存确认：

```text
cuobjdump=/usr/local/cuda/bin/cuobjdump
FileCheck=/usr/lib/llvm-18/bin/FileCheck
```

## 发现并修正的环境缺口

1. Ubuntu CMake `3.28.3` 低于 CCCL RAPIDS 测试层要求的 `3.30.4`：改用经官方 SHA256 清单校验的用户目录 CMake `3.31.12`。
2. 初始 CUDA 组合缺少 `CUDA::nvrtc`：增量安装 `cuda-nvrtc-dev-13-3`。
3. cubin-check 找不到 `cuobjdump`：把 `/usr/local/cuda/bin` 加入 CMake program search path。
4. FileCheck 不在默认 PATH：安装 `llvm-18-tools`，CMake 使用 `/usr/lib/llvm-18/bin/FileCheck`。

这些都是环境修正；没有改动 CCCL 源码，也没有关闭仓库构建检查。

## 最小构建目标

```bash
ninja -C /home/lktr/src/cccl/build/cub-cpp17 -j 2 \
  generate_ctest_json \
  cub.test.device.reduce.lid_0.types_0
```

结果：`117/117` 编译与链接步骤完成，生成：

```text
/home/lktr/src/cccl/build/cub-cpp17/bin/cub.test.device.reduce.lid_0.types_0
```

## CTest 结果

```bash
ctest --test-dir /home/lktr/src/cccl/build/cub-cpp17 \
  --output-on-failure \
  -R '^cub.test.device.reduce.lid_0.types_0$'
```

```text
Test   #1: generate_resource_spec ................. Passed  0.12 sec
Test #290: cub.test.device.reduce.lid_0.types_0 ... Passed  2.85 sec
100% tests passed, 0 tests failed out of 2
Total Test time (real) = 2.99 sec
```

## 结论与边界

本机已跑通一个来自当前 CCCL 提交、由官方 CMake/CTest 注册的 CUB DeviceReduce 正确性测试。这证明当前 WSL2 + CUDA 13.3 + GCC 13 + CMake 3.31 环境能够配置、编译并执行该最小目标。

尚未完成：

- CUB 全量或 DeviceReduce 全矩阵测试；
- 官方 NVBench benchmark；
- 性能稳定性/噪声分析；
- Nsight Compute counters；
- 任何 CCCL 源码修改、公开 issue 或 PR。

当前只能表述为“本地环境与首个官方 DeviceReduce 正确性测试已跑通”，不能表述为已经发现性能问题或完成开源贡献。
