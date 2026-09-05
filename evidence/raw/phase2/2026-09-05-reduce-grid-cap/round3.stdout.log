# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[2949120,2949121,5898239,5898240,5898241,2945023,2945024,2945025,2949119]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/round3.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/round3.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Pass: Cold: 0.074355ms GPU, 0.155742ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 0.076110ms GPU, 0.159905ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 0.140557ms GPU, 0.228787ms CPU, 0.14s total GPU, 0.38s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 0.139186ms GPU, 0.215830ms CPU, 0.14s total GPU, 0.36s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898241]
Pass: Cold: 0.138979ms GPU, 0.232746ms CPU, 0.14s total GPU, 0.39s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945023]
Pass: Cold: 0.076580ms GPU, 0.154445ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 0.074864ms GPU, 0.152815ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 0.074499ms GPU, 0.156202ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 0.075939ms GPU, 0.165314ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |      2949120 | 11.250 MiB |   1000x | 155.742 us | 45.77% |  74.355 us | 10.28% | 39.663G | 158.652 GB/s | 61.97% |
|   I32 |         I32 |      2949121 | 11.250 MiB |   1000x | 159.905 us | 48.06% |  76.110 us | 30.49% | 38.748G | 154.992 GB/s | 60.54% |
|   I32 |         I32 |      5898239 | 22.500 MiB |   1000x | 228.787 us | 33.57% | 140.557 us |  9.91% | 41.963G | 167.853 GB/s | 65.56% |
|   I32 |         I32 |      5898240 | 22.500 MiB |   1000x | 215.830 us | 32.98% | 139.186 us |  7.79% | 42.377G | 169.507 GB/s | 66.21% |
|   I32 |         I32 |      5898241 | 22.500 MiB |   1000x | 232.746 us | 37.34% | 138.979 us |  7.20% | 42.440G | 169.759 GB/s | 66.30% |
|   I32 |         I32 |      2945023 | 11.234 MiB |   1000x | 154.445 us | 44.72% |  76.580 us | 14.19% | 38.457G | 153.828 GB/s | 60.08% |
|   I32 |         I32 |      2945024 | 11.234 MiB |   1000x | 152.815 us | 44.88% |  74.864 us | 12.65% | 39.338G | 157.354 GB/s | 61.46% |
|   I32 |         I32 |      2945025 | 11.234 MiB |   1000x | 156.202 us | 44.02% |  74.499 us | 14.74% | 39.531G | 158.123 GB/s | 61.76% |
|   I32 |         I32 |      2949119 | 11.250 MiB |   1000x | 165.314 us | 46.13% |  75.939 us |  9.88% | 38.835G | 155.341 GB/s | 60.67% |
