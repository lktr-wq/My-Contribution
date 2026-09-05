# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[4095,4096,4097,16773120,16777215,16777216,16777217,16781311,16781312]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/round1.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/round1.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4095]
Pass: Cold: 0.015458ms GPU, 0.089793ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4096]
Pass: Cold: 0.015322ms GPU, 0.091475ms CPU, 0.02s total GPU, 0.26s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4097]
Pass: Cold: 0.022081ms GPU, 0.104831ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16773120]
Pass: Cold: 0.372651ms GPU, 0.440336ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777215]
Pass: Cold: 0.373095ms GPU, 0.441109ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777216]
Pass: Cold: 0.372273ms GPU, 0.439289ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777217]
Pass: Cold: 0.372850ms GPU, 0.438597ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16781311]
Pass: Cold: 0.372759ms GPU, 0.438190ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16781312]
Pass: Cold: 0.372599ms GPU, 0.434870ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|----------|--------------|--------|
|   I32 |         I32 |         4095 | 15.996 KiB |   1000x |  89.793 us | 41.25% |  15.458 us | 77.03% | 264.919M |   1.060 GB/s |  0.41% |
|   I32 |         I32 |         4096 | 16.000 KiB |   1000x |  91.475 us | 36.82% |  15.322 us | 54.42% | 267.324M |   1.070 GB/s |  0.42% |
|   I32 |         I32 |         4097 | 16.004 KiB |   1000x | 104.831 us | 34.42% |  22.081 us | 76.60% | 185.548M | 742.373 MB/s |  0.29% |
|   I32 |         I32 |     16773120 | 63.984 MiB |   1000x | 440.336 us |  8.38% | 372.651 us |  3.40% |  45.010G | 180.041 GB/s | 70.32% |
|   I32 |         I32 |     16777215 | 64.000 MiB |   1000x | 441.109 us |  8.64% | 373.095 us |  3.14% |  44.968G | 179.871 GB/s | 70.25% |
|   I32 |         I32 |     16777216 | 64.000 MiB |   1000x | 439.289 us |  6.93% | 372.273 us |  3.19% |  45.067G | 180.268 GB/s | 70.41% |
|   I32 |         I32 |     16777217 | 64.000 MiB |   1000x | 438.597 us |  6.87% | 372.850 us |  2.96% |  44.997G | 179.989 GB/s | 70.30% |
|   I32 |         I32 |     16781311 | 64.016 MiB |   1000x | 438.190 us | 15.85% | 372.759 us |  2.42% |  45.019G | 180.077 GB/s | 70.33% |
|   I32 |         I32 |     16781312 | 64.016 MiB |   1000x | 434.870 us |  6.40% | 372.599 us |  1.97% |  45.039G | 180.154 GB/s | 70.36% |
