# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[16781312,16781311,16777217,16777216,16777215,16773120,4097,4096,4095]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/round2.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/round2.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16781312]
Pass: Cold: 0.373156ms GPU, 0.437814ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [2/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16781311]
Pass: Cold: 0.373378ms GPU, 0.444302ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [3/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777217]
Pass: Cold: 0.373281ms GPU, 0.442582ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [4/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777216]
Pass: Cold: 0.373510ms GPU, 0.445495ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [5/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777215]
Pass: Cold: 0.373687ms GPU, 0.444053ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
Run:  [6/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16773120]
Pass: Cold: 0.373093ms GPU, 0.438470ms CPU, 0.37s total GPU, 0.54s total wall, 1000x 
Run:  [7/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4097]
Pass: Cold: 0.021569ms GPU, 0.108141ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [8/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4096]
Pass: Cold: 0.014799ms GPU, 0.109675ms CPU, 0.01s total GPU, 0.28s total wall, 1000x 
Run:  [9/9] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4095]
Pass: Cold: 0.017085ms GPU, 0.101285ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|------------|--------|------------|--------|----------|--------------|--------|
|   I32 |         I32 |     16781312 | 64.016 MiB |   1000x | 437.814 us |  6.73% | 373.156 us |  3.36% |  44.971G | 179.885 GB/s | 70.26% |
|   I32 |         I32 |     16781311 | 64.016 MiB |   1000x | 444.302 us |  8.28% | 373.378 us |  3.99% |  44.945G | 179.778 GB/s | 70.22% |
|   I32 |         I32 |     16777217 | 64.000 MiB |   1000x | 442.582 us |  7.43% | 373.281 us |  3.07% |  44.945G | 179.781 GB/s | 70.22% |
|   I32 |         I32 |     16777216 | 64.000 MiB |   1000x | 445.495 us |  8.66% | 373.510 us |  3.22% |  44.918G | 179.671 GB/s | 70.18% |
|   I32 |         I32 |     16777215 | 64.000 MiB |   1000x | 444.053 us |  8.47% | 373.687 us |  2.81% |  44.896G | 179.586 GB/s | 70.14% |
|   I32 |         I32 |     16773120 | 63.984 MiB |   1000x | 438.470 us |  7.01% | 373.093 us |  3.48% |  44.957G | 179.828 GB/s | 70.24% |
|   I32 |         I32 |         4097 | 16.004 KiB |   1000x | 108.141 us | 35.87% |  21.569 us | 72.52% | 189.952M | 759.992 MB/s |  0.30% |
|   I32 |         I32 |         4096 | 16.000 KiB |   1000x | 109.675 us | 43.48% |  14.799 us | 93.82% | 276.784M |   1.107 GB/s |  0.43% |
|   I32 |         I32 |         4095 | 15.996 KiB |   1000x | 101.285 us | 42.34% |  17.085 us | 99.03% | 239.679M | 958.949 MB/s |  0.37% |
