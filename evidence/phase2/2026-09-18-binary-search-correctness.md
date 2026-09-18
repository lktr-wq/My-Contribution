# 第三个短段：#11412 隔离诊断程序与正确性

## 结果

已编译并运行 `binary_search_11412.cu`。165 个配置、2595 次逐查询 GPU/CPU 比较全部通过，各配置输出两端哨兵通过。无 CUDA 错误。未修改 libcu++，未运行性能 benchmark，没有加速结论。

本段 UTC 2026-09-18 09:03:54 开始，限制 10 分钟。编译进程约 4.64 秒，正确性程序约 0.42 秒；这些是进程墙钟时间，不是算法性能数据。

## 覆盖

- 官方 `cuda::std::binary_search`。
- 自建 lower-bound 型搜索：64 位 / 32 位索引。
- 自建按 less-than 等价判断提前结束搜索：64 位 / 32 位索引。
- 长度 0、1、2、3、31、32、33、255、256、257、20000。
- 递增偶数、每四项重复、全部等于 7 三种排序数组。
- 固定查询含小于范围、间隙、范围内及大于范围的值；非空输入另查首项、中项、末项。空数组仍分配一个有效设备槽，但搜索范围为空。
- 每个查询独立对比 CPU `std::binary_search`，不是只比较总体命中计数。
- 独立 kernel 模板实例区分五个变体，CUDA 启动、同步、拷贝错误均检查。

自建算法只是整数排序输入的诊断参考，不是通用 STL 实现；未验证任意比较器、仅满足分区契约但非全排序的数组、forward iterator、超大长度等。哨兵检查不等同于 Compute Sanitizer，也不能排除所有越界读取。源码中声明 64 位不保证编译器保留所有 64 位运算，后续需要检查生成代码再解释性能。

## 环境与复现

CCCL-Ubuntu / lktr，CUDA 13.3.73，RTX 4060 Laptop，`-O3 -std=c++17 -arch=sm_89`。
CCCL 固定 HEAD `f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`，前后工作树干净。源码、脚本、二进制 SHA256、编译命令、输出与失败检查均保存在原始结果目录。没有下载依赖或改变电源模式。

```powershell
wsl -d CCCL-Ubuntu -u lktr -- python3 '/mnt/d/Projects/Open-Source Contribution/evidence/phase2/prepare_binary_search_11412.py' '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/binary-search-correctness-recheck'
```

输出目录必须不存在，避免覆盖。输入源程序 `evidence/phase2/binary_search_11412.cu`；驱动 `evidence/phase2/prepare_binary_search_11412.py`；原始结果 `evidence/raw/phase2/2026-09-18-binary-search-correctness/`。build 目录不进入 Git。

## 下一段提议（需确认，最多 10 分钟）

优先准备有代表性的计时入口并检查生成代码：恢复原问题的每块重复搜索结构，保持各变体相同工作量；区分分散命中、未命中、中点集中命中。保留逐查询正确性检查，避免直接使用原复现“只取十次最小值且不核对结果”的做法。

准备工作不需要增强模式。正式计时另段开始前再确认插电、增强、背景 GPU 负载；不能将当前 Silent 下的正确性运行耗时用作性能证据。原有三个未提交修改保持不动。
