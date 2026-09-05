# DeviceReduce 残余 tile：实际指令与上游覆盖核查

日期：2026-09-06，Asia/Shanghai。阶段：只读分析既有二进制和公开上游信息；没有新增 GPU benchmark、修改 CUB、提交公开 issue/PR 或产生云费用。

## 结论

已经把“源码看起来走不同路径”推进到“测量过的二进制确实存在不同读取指令”。对齐的完整 tile 使用 128-bit 向量读取；残余 tile 使用标量读取和额外边界/循环控制。但没有动态执行计数、分 kernel 时间线或修改版 A/B，不能认定这就是之前 2.78%–6.94% 描述性差异的根因，不能声称已经发现 bug 或获得性能收益。

本次四组上游检索共返回 110 条、去重 100 条 issue/PR，未识别到直接覆盖当前 I32 残余读取候选的实现。最新 main 的三个相关源码文件与固定基线逐字节一致。部分 PR 详情及评论因匿名 API 限流没有获取，不能保证不存在相关工作；公开提出新贡献前仍须刷新。

## 证据身份与抽取验收

- 固定 CCCL：`f747ef146b77ed1e8f38fe8cb3c67effaf7793f2`，本轮重新确认 WSL checkout 干净。
- 使用上一轮成功的 `2026-09-05-fixed-input-reduce-v2/build/fixed_input_reduce`，未重编译。
- 二进制 SHA256：`0f997ed19d59bd20343f557f7766b53ab8f9ca74248e8df2c61533b98eaa6f95`，抽取前校验通过。
- 从本地 object 唯一定位非 SingleTile 的 `DeviceReduceKernel`，再从实际可执行文件抽取同名函数。模板参数确认输入/累加为 int，内部 OffsetT 为 unsigned int，plus<void>、identity。内部 unsigned 类型与 `cub/detail/choose_offset.cuh` 的 32-bit 选择规则相符，不应把 benchmark 的外部 I32 长度标签误写成内部 signed int。
- object 和实际二进制的目标 SASS 指令行逐项相同；原始转储哈希复验通过，见 `validation.json`。
- 目标编译资源：REG 40、STACK 0、SHARED 44、LOCAL 0。这些是静态资源信息，不是 occupancy 或 stall 计数。
- `cuobjdump --function` 对 SASS 生效，但本次 PTX 转储仍含全部模块。保存原始输出，再按完整符号和配对大括号抽出唯一 entry（原始 PTX 第 107976–109046 行）；不把 NVBench 辅助 kernel 混入分析。
- SASS/resource 命令退出码为 0，但 stderr 存在 function not found 警告；原样保留。不能把该转储描述成“无警告”。输出中确有唯一目标函数，并额外通过 object/二进制指令一致性检查确认提取有效；不对警告来源作未经验证的归因。

证据目录：`evidence/raw/phase2/2026-09-06-reduce-sass/`。优先阅读 `target-sass-instructions.txt`、`target-reduce.ptx`、`manifest.json`、`validation.json`。保留原始转储；目录内关闭 Git 文本换行转换以保存哈希。

## 一份数据如何经过这三条路径

设 B=720×4096=2,949,120；tile=256 threads×16 I32。固定输入 cudaMalloc 指针对齐。第一阶段 grid=720，block 初始偏移=blockIdx×4096，stride=720×4096。

| 长度 | 特殊 block 的数据 | 源码路径 | 测量二进制中的位置 |
|---|---|---|---|
| B | 每个 block 都有 4096 个有效元素 | 对齐完整首 tile，随后归约 | 对齐入口 0x27d0；0x2800 比较 4096；0x2880–0x28b0 四条 LDG.E.128.CONSTANT |
| B-1 | block 719 从一开始只有 4095 个有效元素 | ConsumePartialTile<true>，再进入带 valid_items 的 collective Reduce | 0x2810 转至 0x3620；首标量读 0x36b0；0x37c0 标量余数循环，0x3820 回跳；后续亦有展开的标量读取 |
| B+1 | block 0 先读完整 4096 个，再跨 stride 读最后 1 个 | ConsumeFullTileRange 后的 ConsumePartialTile<false> | 完整首 tile 后进入 0x2b90 起的后续残余控制；它不是 0x3620 的“首 tile 不足”分支 |

源码定位：固定版本 `cub/cub/agent/agent_reduce.cuh` 的 ConsumeFullTile（约 304 行）、ConsumePartialTile（约 353 行）、ConsumeRange（约 385 行）、ConsumeFullTileRange（约 446 行）。这是结合源码与控制流的静态映射，没有采集实际 GPU 分支轨迹。

PTX 交叉核查：对齐入口 `$L__BB2_36` 按剩余元素是否少于 4096 分支；完整首 tile 的 `$L__BB2_37` 有四条 `ld.global.nc.v2.u64`（第 620、626、632、638 行）；首残余路径 `$L__BB2_53`、`$L__BB2_58`、`$L__BB2_61` 使用 `ld.global.nc.u32`，包含步长 256 的余数处理及展开处理。

这里的“标量”不等于“未合并访存”：相邻线程仍可读取相邻 I32。编译器也已展开部分循环，不能简单宣称每次读取都执行同样一次判断，或用静态指令行数推算耗时。完整/残余的 collective 归约入口也有差别；只有进一步控制实验才能区分这些因素。

## 上游覆盖检查

查询（每组 per_page=100）：`repo:NVIDIA/cccl "partial tile" reduce`（33）、`repo:NVIDIA/cccl "tail" "reduce"`（61）、`repo:NVIDIA/cccl "ConsumePartialTile"`（1）、`repo:NVIDIA/cccl "vectorize" "reduce"`（15）。均 incomplete_results=false 且返回数量等于 total_count。数量只是搜索覆盖范围，不能代表逐条评论及实现均被审查。

| 上游项 | 本轮证据与范围判断 |
|---|---|
| [#9762 大类型向量化回退](https://github.com/NVIDIA/cccl/pull/9762) | 搜索状态 closed；本地历史 8f2803715e 已包含 sizeof(InputT)<=8 的限制。4-byte I32 仍满足条件，不是当前残余路径修复。 |
| [#10928 vector buffer 对齐](https://github.com/NVIDIA/cccl/pull/10928) | 本地历史 1fb7869e6c 已包含 alignas(VectorT)。修改完整 tile 局部缓冲对齐；不能把它作为本项目新贡献。未取得最新 PR 详情。 |
| [#7571 扩展可向量化类型](https://github.com/NVIDIA/cccl/pull/7571) | 搜索状态 closed；正文为减少 is_primitive 限制的类型兼容性调整，不是 near-full partial tile 加载实现。 |
| [#11164 WarpReduce dispatch](https://github.com/NVIDIA/cccl/pull/11164) | 搜索状态 closed；本地 1749f8f6de 已包含。涉及逻辑 warp/物理 warp 与 redux 选择，不应重复开发其已有方案。 |
| [#9101 blockReduceWarp](https://github.com/NVIDIA/cccl/pull/9101) | 搜索状态 open；正文为顺序汇总改为 cooperative warp reduction，可能影响 collective 成本，是相邻并行工作。未取得完整 diff/review；不能据此断言没有重叠。后续限定加载假设，不改 collective。 |
| [#307 CUB 向量化任务](https://github.com/NVIDIA/cccl/issues/307) | 搜索状态 open；正文已承认 reduce 使用向量读取，任务列出其他算法，不是当前 I32 partial tile 的现成实现。 |
| [#3871 work stealing](https://github.com/NVIDIA/cccl/issues/3871) | 搜索状态 open；包含 DeviceReduce 的更广泛任务，不是本轮 sm_89 残余读取的直接替代方案。 |
| [#9771 gpu_to_gpu 越界](https://github.com/NVIDIA/cccl/issues/9771) | 搜索状态 open；正文指 gpu_to_gpu/RFA 与 INT32_MAX 整数倍的分块问题。当前普通 I32 两阶段约 295 万元素不匹配。 |

通过 `git ls-remote` 只读获取当时 main：`486de1c44daf7d1a343cbbf0f5477e9bea8ad600`。按该不可变 SHA 获取 agent_reduce.cuh、warp_reduce_shfl.cuh、block_reduce_warp_reductions.cuh，均与固定 WSL 基线逐字节相同。没有拉取/切换项目版本。官方 [该版本 agent_reduce.cuh](https://github.com/NVIDIA/cccl/blob/486de1c44daf7d1a343cbbf0f5477e9bea8ad600/cub/cub/agent/agent_reduce.cuh) 仍保留上述残余读取逻辑。

限制与原始响应在 `evidence/raw/phase2/2026-09-06-reduce-upstream/`。四组搜索之后 PR 详情 API 触发限流；一个 raw 文件首次 TLS 失败、单次重试成功，没有关闭证书校验。没有穷尽不同措辞、全部评论、分支及尚未公开工作。

## 下一阶段：一个可证伪问题，而不是先承诺优化

假设：在对齐 I32、普通加法、接近完整的首残余 tile 条件下，用有界向量读取处理完整的 4 元素组、标量读取不足 4 个的尾巴，能减少加载/控制成本，并在原受控输入上带来可重复的端到端收益。

建议下一轮仅做本地实验：

1. 保留基线和原始日志，在独立实验副本/包含目录中做受限变体；不改公共 API、grid、tile policy、collective 归约或默认上游 checkout。短尾、非对齐输入及未证明安全的类型保留原路径。
2. 先验正确性：0、1、255/256/257、4095/4096/4097、B 附近及对齐/不对齐指针；仅使用不溢出 I32 的数据，加入多种输入模式。检查每条向量读取全部位于有效范围内，禁止读后屏蔽越界值。
3. 比较变体 SASS，确认目标路径确实改变；完整 tile 控制组、输出/scratch/stream 固定。基线/变体的构建参数一致，交错 A/B 顺序，不拿跨程序历史绝对时间当优化。
4. 若结果错误、越界、完整 tile 回退或预设短实验中没有稳定收益，停止这条假设；若有收益，再扩展测试和统计，不立即提交 PR。需要长时间构建/测试时先告知用户成本。

本轮没有执行这份方案，也没有测量新收益。用户个人理解验收、完整 CCCL 测试矩阵及公开贡献均尚未完成。

## 本轮复现工具

WSL：`inspect_reduce_sass.py <new-output-dir>` 抽取；`summarize_reduce_sass.py <that-dir>` 生成单函数视图。已有证据可由 `verify_reduce_audit.py` 的断言复核（脚本当前会写入新的 validation.json，已存在时拒绝覆盖）。PowerShell：`snapshot_reduce_upstream.ps1 -OutputDirectory <new-dir>` 保存公开搜索/API 响应；`finish_reduce_upstream.ps1` 用本轮已记录的不可变 SHA 补充 raw 源码与本地历史。后者不是自动获取未来最新版本的工具。
