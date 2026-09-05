# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[2949120,2949121,5898239,5898240,5898241,2945023,2945024,2945025,2949119]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap-confirm/round3.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap-confirm/round3.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949120]
Pass: Cold: 0.075757ms GPU, 0.163553ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 0.075257ms GPU, 0.154414ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 0.142022ms GPU, 0.223467ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 0.141380ms GPU, 0.216563ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898241]
Pass: Cold: 0.140504ms GPU, 0.214441ms CPU, 0.14s total GPU, 0.36s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945023]
Pass: Cold: 0.077149ms GPU, 0.152242ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 0.075029ms GPU, 0.153187ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 0.074179ms GPU, 0.150719ms CPU, 0.07s total GPU, 0.30s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 0.078518ms GPU, 0.153872ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |      2949120 | 11.250 MiB |   1000x | 163.553 us | 46.83% |  75.757 us | 14.51% | 38.929G | 155.715 GB/s | 60.82% |
|   I32 |         I32 |      2949121 | 11.250 MiB |   1000x | 154.414 us | 43.63% |  75.257 us | 12.26% | 39.188G | 156.750 GB/s | 61.22% |
|   I32 |         I32 |      5898239 | 22.500 MiB |   1000x | 223.467 us | 34.49% | 142.022 us |  6.80% | 41.530G | 166.122 GB/s | 64.88% |
|   I32 |         I32 |      5898240 | 22.500 MiB |   1000x | 216.563 us | 32.04% | 141.380 us | 13.60% | 41.719G | 166.877 GB/s | 65.18% |
|   I32 |         I32 |      5898241 | 22.500 MiB |   1000x | 214.441 us | 31.87% | 140.504 us |  4.37% | 41.979G | 167.917 GB/s | 65.58% |
|   I32 |         I32 |      2945023 | 11.234 MiB |   1000x | 152.242 us | 43.45% |  77.149 us |  9.17% | 38.173G | 152.693 GB/s | 59.64% |
|   I32 |         I32 |      2945024 | 11.234 MiB |   1000x | 153.187 us | 43.70% |  75.029 us |  7.47% | 39.252G | 157.006 GB/s | 61.32% |
|   I32 |         I32 |      2945025 | 11.234 MiB |   1000x | 150.719 us | 45.86% |  74.179 us |  7.75% | 39.702G | 158.807 GB/s | 62.03% |
|   I32 |         I32 |      2949119 | 11.250 MiB |   1000x | 153.872 us | 46.45% |  78.518 us | 34.46% | 37.560G | 150.240 GB/s | 58.68% |
