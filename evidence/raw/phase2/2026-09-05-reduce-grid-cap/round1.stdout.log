# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[2945023,2945024,2945025,2949119,2949120,2949121,5898239,5898240,5898241]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/round1.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/round1.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Pass: Cold: 0.087536ms GPU, 0.183494ms CPU, 0.09s total GPU, 0.36s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 0.075743ms GPU, 0.155126ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 0.076434ms GPU, 0.161399ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 0.078877ms GPU, 0.164526ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949120]
Pass: Cold: 0.076700ms GPU, 0.161805ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 0.077340ms GPU, 0.158616ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 0.141626ms GPU, 0.221244ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 0.138665ms GPU, 0.229928ms CPU, 0.14s total GPU, 0.38s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898241]
Pass: Cold: 0.140089ms GPU, 0.218684ms CPU, 0.14s total GPU, 0.37s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |      2945023 | 11.234 MiB |   1000x | 183.494 us | 44.45% |  87.536 us | 15.13% | 33.644G | 134.574 GB/s | 52.56% |
|   I32 |         I32 |      2945024 | 11.234 MiB |   1000x | 155.126 us | 40.85% |  75.743 us | 14.42% | 38.882G | 155.528 GB/s | 60.75% |
|   I32 |         I32 |      2945025 | 11.234 MiB |   1000x | 161.399 us | 44.20% |  76.434 us | 12.42% | 38.530G | 154.121 GB/s | 60.20% |
|   I32 |         I32 |      2949119 | 11.250 MiB |   1000x | 164.526 us | 42.86% |  78.877 us | 18.01% | 37.389G | 149.556 GB/s | 58.41% |
|   I32 |         I32 |      2949120 | 11.250 MiB |   1000x | 161.805 us | 46.67% |  76.700 us | 19.22% | 38.450G | 153.800 GB/s | 60.07% |
|   I32 |         I32 |      2949121 | 11.250 MiB |   1000x | 158.616 us | 41.38% |  77.340 us | 16.26% | 38.132G | 152.527 GB/s | 59.57% |
|   I32 |         I32 |      5898239 | 22.500 MiB |   1000x | 221.244 us | 32.17% | 141.626 us |  8.03% | 41.647G | 166.586 GB/s | 65.06% |
|   I32 |         I32 |      5898240 | 22.500 MiB |   1000x | 229.928 us | 32.77% | 138.665 us |  5.16% | 42.536G | 170.144 GB/s | 66.45% |
|   I32 |         I32 |      5898241 | 22.500 MiB |   1000x | 218.684 us | 31.92% | 140.089 us |  5.77% | 42.104G | 168.415 GB/s | 65.78% |
