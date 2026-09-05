# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}[pow2]=[16,24]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 1 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-warmup-audit/run4-warmup1.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-warmup-audit/run4-warmup1.md'
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
Run:  [1/2] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.018245ms GPU, 0.109636ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [2/2] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.373777ms GPU, 0.449633ms CPU, 0.37s total GPU, 0.56s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |  Elements{io}   |    Size     | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|-----------------|-------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |    2^16 = 65536 | 256.000 KiB |   1000x | 109.636 us | 36.65% |  18.245 us | 62.81% |  3.592G |  14.368 GB/s |  5.61% |
|   I32 |         I32 | 2^24 = 16777216 |  64.000 MiB |   1000x | 449.633 us | 11.31% | 373.777 us |  7.46% | 44.886G | 179.543 GB/s | 70.13% |
