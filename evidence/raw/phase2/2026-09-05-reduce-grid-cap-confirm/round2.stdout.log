# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[5898241,5898240,5898239,2949121,2949120,2949119,2945025,2945024,2945023]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap-confirm/round2.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap-confirm/round2.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898241]
Pass: Cold: 0.139200ms GPU, 0.223603ms CPU, 0.14s total GPU, 0.38s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 0.138752ms GPU, 0.235316ms CPU, 0.14s total GPU, 0.39s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 0.139980ms GPU, 0.223241ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 0.075291ms GPU, 0.155198ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949120]
Pass: Cold: 0.074468ms GPU, 0.151856ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 0.076712ms GPU, 0.157642ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 0.074622ms GPU, 0.152017ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 0.077408ms GPU, 0.165185ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945023]
Pass: Cold: 0.079358ms GPU, 0.175673ms CPU, 0.08s total GPU, 0.34s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |      5898241 | 22.500 MiB |   1000x | 223.603 us | 32.09% | 139.200 us |  6.91% | 42.372G | 169.490 GB/s | 66.20% |
|   I32 |         I32 |      5898240 | 22.500 MiB |   1000x | 235.316 us | 33.12% | 138.752 us |  6.43% | 42.509G | 170.037 GB/s | 66.41% |
|   I32 |         I32 |      5898239 | 22.500 MiB |   1000x | 223.241 us | 32.84% | 139.980 us |  5.58% | 42.136G | 168.546 GB/s | 65.83% |
|   I32 |         I32 |      2949121 | 11.250 MiB |   1000x | 155.198 us | 45.10% |  75.291 us |  9.46% | 39.170G | 156.678 GB/s | 61.19% |
|   I32 |         I32 |      2949120 | 11.250 MiB |   1000x | 151.856 us | 44.70% |  74.468 us |  7.91% | 39.602G | 158.409 GB/s | 61.87% |
|   I32 |         I32 |      2949119 | 11.250 MiB |   1000x | 157.642 us | 45.36% |  76.712 us | 13.61% | 38.444G | 153.776 GB/s | 60.06% |
|   I32 |         I32 |      2945025 | 11.234 MiB |   1000x | 152.017 us | 46.32% |  74.622 us | 25.04% | 39.466G | 157.863 GB/s | 61.66% |
|   I32 |         I32 |      2945024 | 11.234 MiB |   1000x | 165.185 us | 47.45% |  77.408 us | 27.90% | 38.045G | 152.181 GB/s | 59.44% |
|   I32 |         I32 |      2945023 | 11.234 MiB |   1000x | 175.673 us | 45.94% |  79.358 us | 14.08% | 37.111G | 148.443 GB/s | 57.98% |
