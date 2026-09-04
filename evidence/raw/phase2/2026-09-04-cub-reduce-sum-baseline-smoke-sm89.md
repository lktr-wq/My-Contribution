# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 --stopping-criterion entropy -a 'T{ct}=I32' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-sm89.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-sm89.md'
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
Run:  [1/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.022100ms GPU, 0.132637ms CPU, 0.01s total GPU, 0.17s total wall, 490x 
Run:  [2/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.038879ms GPU, 0.173470ms CPU, 0.05s total GPU, 0.50s total wall, 1230x 
Run:  [3/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.373611ms GPU, 0.500233ms CPU, 0.21s total GPU, 0.37s total wall, 560x 
Run:  [4/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 5.465623ms GPU, 5.624049ms CPU, 6.38s total GPU, 6.82s total wall, 1168x 
Run:  [5/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^16]
Warn: GPU throttled below threshold (1558.80 MHz / 2250.00 MHz) (69% < 75%) on sample 196. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.020524ms GPU, 0.150305ms CPU, 0.01s total GPU, 0.24s total wall, 548x 
Run:  [6/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.036415ms GPU, 0.151172ms CPU, 0.03s total GPU, 0.28s total wall, 832x 
Run:  [7/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.370901ms GPU, 0.497447ms CPU, 0.20s total GPU, 0.35s total wall, 534x 
Run:  [8/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 5.489902ms GPU, 5.649022ms CPU, 5.67s total GPU, 6.04s total wall, 1032x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |   Elements{io}   |    Size     | Samples |  CPU Time  |  Noise  |  GPU Time  |  Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|------------------|-------------|---------|------------|---------|------------|---------|---------|--------------|--------|
|   I32 |         I32 |     2^16 = 65536 | 256.000 KiB |    490x | 132.637 us |  99.41% |  22.100 us |  79.76% |  2.965G |  11.862 GB/s |  4.63% |
|   I32 |         I32 |   2^20 = 1048576 |   4.000 MiB |   1230x | 173.470 us | 290.71% |  38.879 us |  33.24% | 26.970G | 107.882 GB/s | 42.14% |
|   I32 |         I32 |  2^24 = 16777216 |  64.000 MiB |    560x | 500.233 us |  28.89% | 373.611 us |  11.12% | 44.906G | 179.622 GB/s | 70.16% |
|   I32 |         I32 | 2^28 = 268435456 |   1.000 GiB |   1168x |   5.624 ms |  35.79% |   5.466 ms |  35.41% | 49.113G | 196.454 GB/s | 76.73% |
|   I32 |         I64 |     2^16 = 65536 | 256.000 KiB |    548x | 150.305 us |  82.72% |  20.524 us | 193.37% |  3.193G |  12.773 GB/s |  4.99% |
|   I32 |         I64 |   2^20 = 1048576 |   4.000 MiB |    832x | 151.172 us |  84.72% |  36.415 us |  38.49% | 28.795G | 115.182 GB/s | 44.99% |
|   I32 |         I64 |  2^24 = 16777216 |  64.000 MiB |    534x | 497.447 us |  30.10% | 370.901 us |   7.71% | 45.234G | 180.935 GB/s | 70.67% |
|   I32 |         I64 | 2^28 = 268435456 |   1.000 GiB |   1032x |   5.649 ms |  36.12% |   5.490 ms |  35.90% | 48.896G | 195.585 GB/s | 76.39% |
