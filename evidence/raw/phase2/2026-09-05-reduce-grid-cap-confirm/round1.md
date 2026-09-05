# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[2945023,2945024,2945025,2949119,2949120,2949121,5898239,5898240,5898241]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap-confirm/round1.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap-confirm/round1.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Pass: Cold: 0.088229ms GPU, 0.169193ms CPU, 0.09s total GPU, 0.34s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 0.076646ms GPU, 0.153041ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 0.074165ms GPU, 0.154185ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 0.076971ms GPU, 0.153968ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949120]
Pass: Cold: 0.074034ms GPU, 0.156488ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 0.074365ms GPU, 0.155441ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 0.141169ms GPU, 0.221061ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 0.139453ms GPU, 0.217861ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898241]
Pass: Cold: 0.139759ms GPU, 0.231488ms CPU, 0.14s total GPU, 0.38s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |      2945023 | 11.234 MiB |   1000x | 169.193 us | 48.57% |  88.229 us |  9.32% | 33.379G | 133.517 GB/s | 52.15% |
|   I32 |         I32 |      2945024 | 11.234 MiB |   1000x | 153.041 us | 44.25% |  76.646 us | 10.18% | 38.424G | 153.696 GB/s | 60.03% |
|   I32 |         I32 |      2945025 | 11.234 MiB |   1000x | 154.185 us | 46.03% |  74.165 us |  9.95% | 39.709G | 158.837 GB/s | 62.04% |
|   I32 |         I32 |      2949119 | 11.250 MiB |   1000x | 153.968 us | 45.80% |  76.971 us |  8.48% | 38.315G | 153.258 GB/s | 59.86% |
|   I32 |         I32 |      2949120 | 11.250 MiB |   1000x | 156.488 us | 45.99% |  74.034 us | 12.20% | 39.835G | 159.339 GB/s | 62.23% |
|   I32 |         I32 |      2949121 | 11.250 MiB |   1000x | 155.441 us | 44.33% |  74.365 us | 10.22% | 39.657G | 158.629 GB/s | 61.96% |
|   I32 |         I32 |      5898239 | 22.500 MiB |   1000x | 221.061 us | 33.65% | 141.169 us | 10.01% | 41.782G | 167.126 GB/s | 65.28% |
|   I32 |         I32 |      5898240 | 22.500 MiB |   1000x | 217.861 us | 32.66% | 139.453 us |  7.04% | 42.296G | 169.182 GB/s | 66.08% |
|   I32 |         I32 |      5898241 | 22.500 MiB |   1000x | 231.488 us | 33.04% | 139.759 us |  7.23% | 42.203G | 168.811 GB/s | 65.93% |
