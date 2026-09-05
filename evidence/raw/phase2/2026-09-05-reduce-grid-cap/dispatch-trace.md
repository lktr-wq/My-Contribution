# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[2945023,2945024,2945025,2949119,2949120,2949121,5898239,5898240,5898241]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/dispatch-trace.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/dispatch-trace.md' --profile
```

# Devices

## [0] `NVIDIA GeForce RTX 4060 Laptop GPU`
* SM Version: 890 (PTX Version: 890)
* Number of SMs: 24
* SM Default Clock Rate: 2250 MHz
* Global Memory: 7096 MiB Free / 8187 MiB Total
* Global Memory Bus Peak: 256 GB/sec (128-bit DDR @8001MHz)
* Max Shared Memory: 100 KiB/SM, 48 KiB/Block
* L2 Cache Size: 32768 KiB
* Maximum Active Blocks: 24/SM
* Maximum Active Threads: 1536/SM, 1024/Block
* Available Registers: 65536/SM, 65536/Block
* ECC Enabled: No

# Log

```
Run:  [1/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945023]
Pass: Cold: 25.234432ms GPU, 25.730661ms CPU, 0.03s total GPU, 0.03s total wall, 1x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 1.371936ms GPU, 1.424801ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 1.537024ms GPU, 1.579530ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 1.388544ms GPU, 1.437189ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949120]
Pass: Cold: 1.390592ms GPU, 1.421790ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 1.597280ms GPU, 1.649551ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 1.895328ms GPU, 2.034458ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 1.589248ms GPU, 1.641616ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898241]
Pass: Cold: 1.690624ms GPU, 1.833235ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples | CPU Time  | Noise | GPU Time  | Noise |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|-----------|-------|-----------|-------|----------|--------------|--------|
|   I32 |         I32 |      2945023 | 11.234 MiB |      1x | 25.731 ms |  inf% | 25.234 ms |  inf% | 116.707M | 466.826 MB/s |  0.18% |
|   I32 |         I32 |      2945024 | 11.234 MiB |      1x |  1.425 ms |  inf% |  1.372 ms |  inf% |   2.147G |   8.586 GB/s |  3.35% |
|   I32 |         I32 |      2945025 | 11.234 MiB |      1x |  1.580 ms |  inf% |  1.537 ms |  inf% |   1.916G |   7.664 GB/s |  2.99% |
|   I32 |         I32 |      2949119 | 11.250 MiB |      1x |  1.437 ms |  inf% |  1.389 ms |  inf% |   2.124G |   8.496 GB/s |  3.32% |
|   I32 |         I32 |      2949120 | 11.250 MiB |      1x |  1.422 ms |  inf% |  1.391 ms |  inf% |   2.121G |   8.483 GB/s |  3.31% |
|   I32 |         I32 |      2949121 | 11.250 MiB |      1x |  1.650 ms |  inf% |  1.597 ms |  inf% |   1.846G |   7.385 GB/s |  2.88% |
|   I32 |         I32 |      5898239 | 22.500 MiB |      1x |  2.034 ms |  inf% |  1.895 ms |  inf% |   3.112G |  12.448 GB/s |  4.86% |
|   I32 |         I32 |      5898240 | 22.500 MiB |      1x |  1.642 ms |  inf% |  1.589 ms |  inf% |   3.711G |  14.845 GB/s |  5.80% |
|   I32 |         I32 |      5898241 | 22.500 MiB |      1x |  1.833 ms |  inf% |  1.691 ms |  inf% |   3.489G |  13.955 GB/s |  5.45% |
