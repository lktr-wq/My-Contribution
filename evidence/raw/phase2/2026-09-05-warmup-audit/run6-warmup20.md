# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}[pow2]=[16,24]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-warmup-audit/run6-warmup20.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-warmup-audit/run6-warmup20.md'
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
Pass: Cold: 0.020335ms GPU, 0.101381ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [2/2] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.373765ms GPU, 0.440885ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |  Elements{io}   |    Size     | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|-----------------|-------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |    2^16 = 65536 | 256.000 KiB |   1000x | 101.381 us | 35.70% |  20.335 us | 69.50% |  3.223G |  12.892 GB/s |  5.04% |
|   I32 |         I32 | 2^24 = 16777216 |  64.000 MiB |   1000x | 440.885 us |  8.31% | 373.765 us |  3.01% | 44.887G | 179.549 GB/s | 70.13% |
