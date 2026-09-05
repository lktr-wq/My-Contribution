# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[5898241,5898240,5898239,2949121,2949120,2949119,2945025,2945024,2945023]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/round2.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-grid-cap/round2.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Pass: Cold: 0.140881ms GPU, 0.231141ms CPU, 0.14s total GPU, 0.38s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898240]
Pass: Cold: 0.139443ms GPU, 0.238714ms CPU, 0.14s total GPU, 0.39s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=5898239]
Pass: Cold: 0.140246ms GPU, 0.225349ms CPU, 0.14s total GPU, 0.38s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949121]
Pass: Cold: 0.075856ms GPU, 0.157772ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949120]
Pass: Cold: 0.074621ms GPU, 0.155186ms CPU, 0.07s total GPU, 0.31s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2949119]
Pass: Cold: 0.077600ms GPU, 0.157467ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945025]
Pass: Cold: 0.074280ms GPU, 0.149367ms CPU, 0.07s total GPU, 0.30s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945024]
Pass: Cold: 0.075531ms GPU, 0.160186ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2945023]
Pass: Cold: 0.078673ms GPU, 0.156827ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |      5898241 | 22.500 MiB |   1000x | 231.141 us | 34.30% | 140.881 us | 14.77% | 41.867G | 167.467 GB/s | 65.41% |
|   I32 |         I32 |      5898240 | 22.500 MiB |   1000x | 238.714 us | 37.64% | 139.443 us |  5.63% | 42.299G | 169.195 GB/s | 66.08% |
|   I32 |         I32 |      5898239 | 22.500 MiB |   1000x | 225.349 us | 36.77% | 140.246 us |  9.16% | 42.056G | 168.226 GB/s | 65.71% |
|   I32 |         I32 |      2949121 | 11.250 MiB |   1000x | 157.772 us | 51.34% |  75.856 us | 17.40% | 38.878G | 155.512 GB/s | 60.74% |
|   I32 |         I32 |      2949120 | 11.250 MiB |   1000x | 155.186 us | 46.53% |  74.621 us | 15.35% | 39.521G | 158.085 GB/s | 61.74% |
|   I32 |         I32 |      2949119 | 11.250 MiB |   1000x | 157.467 us | 43.79% |  77.600 us | 27.02% | 38.004G | 152.017 GB/s | 59.37% |
|   I32 |         I32 |      2945025 | 11.234 MiB |   1000x | 149.367 us | 43.68% |  74.280 us | 12.08% | 39.648G | 158.590 GB/s | 61.94% |
|   I32 |         I32 |      2945024 | 11.234 MiB |   1000x | 160.186 us | 47.19% |  75.531 us | 21.17% | 38.991G | 155.964 GB/s | 60.92% |
|   I32 |         I32 |      2945023 | 11.234 MiB |   1000x | 156.827 us | 47.61% |  78.673 us | 35.10% | 37.434G | 149.736 GB/s | 58.48% |
