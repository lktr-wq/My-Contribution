# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[16777215,16777216,16777217,16781311,16781312,4095,4096,4097,16773120]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/round3.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/round3.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777215]
Pass: Cold: 0.373376ms GPU, 0.451415ms CPU, 0.37s total GPU, 0.56s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777216]
Pass: Cold: 0.372408ms GPU, 0.438501ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777217]
Pass: Cold: 0.372807ms GPU, 0.451197ms CPU, 0.37s total GPU, 0.56s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16781311]
Pass: Cold: 0.372739ms GPU, 0.439211ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16781312]
Pass: Cold: 0.373731ms GPU, 0.439408ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4095]
Warn: GPU throttled below threshold (1461.83 MHz / 2250.00 MHz) (65% < 75%) on sample 506. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.016256ms GPU, 0.092112ms CPU, 0.02s total GPU, 0.31s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4096]
Pass: Cold: 0.016300ms GPU, 0.090147ms CPU, 0.02s total GPU, 0.26s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4097]
Pass: Cold: 0.021403ms GPU, 0.106357ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16773120]
Pass: Cold: 0.372483ms GPU, 0.437968ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|----------|--------------|--------|
|   I32 |         I32 |     16777215 | 64.000 MiB |   1000x | 451.415 us | 10.40% | 373.376 us |  5.04% |  44.934G | 179.735 GB/s | 70.20% |
|   I32 |         I32 |     16777216 | 64.000 MiB |   1000x | 438.501 us |  7.82% | 372.408 us |  3.87% |  45.051G | 180.203 GB/s | 70.38% |
|   I32 |         I32 |     16777217 | 64.000 MiB |   1000x | 451.197 us | 10.01% | 372.807 us |  4.45% |  45.002G | 180.010 GB/s | 70.31% |
|   I32 |         I32 |     16781311 | 64.016 MiB |   1000x | 439.211 us |  7.07% | 372.739 us |  2.19% |  45.022G | 180.086 GB/s | 70.34% |
|   I32 |         I32 |     16781312 | 64.016 MiB |   1000x | 439.408 us |  7.74% | 373.731 us |  3.63% |  44.902G | 179.608 GB/s | 70.15% |
|   I32 |         I32 |         4095 | 15.996 KiB |   1000x |  92.112 us | 37.26% |  16.256 us | 67.86% | 251.909M |   1.008 GB/s |  0.39% |
|   I32 |         I32 |         4096 | 16.000 KiB |   1000x |  90.147 us | 36.11% |  16.300 us | 52.70% | 251.284M |   1.005 GB/s |  0.39% |
|   I32 |         I32 |         4097 | 16.004 KiB |   1000x | 106.357 us | 33.63% |  21.403 us | 60.61% | 191.420M | 765.867 MB/s |  0.30% |
|   I32 |         I32 |     16773120 | 63.984 MiB |   1000x | 437.968 us |  6.63% | 372.483 us |  2.12% |  45.031G | 180.122 GB/s | 70.35% |
