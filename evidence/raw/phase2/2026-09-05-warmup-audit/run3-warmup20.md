# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}[pow2]=[16,24]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-warmup-audit/run3-warmup20.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-warmup-audit/run3-warmup20.md'
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
Pass: Cold: 0.019632ms GPU, 0.114193ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [2/2] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.373586ms GPU, 0.446782ms CPU, 0.37s total GPU, 0.55s total wall, 1000x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |  Elements{io}   |    Size     | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|-----------------|-------------|---------|------------|--------|------------|--------|---------|--------------|--------|
|   I32 |         I32 |    2^16 = 65536 | 256.000 KiB |   1000x | 114.193 us | 37.11% |  19.632 us | 75.68% |  3.338G |  13.353 GB/s |  5.22% |
|   I32 |         I32 | 2^24 = 16777216 |  64.000 MiB |   1000x | 446.782 us |  9.71% | 373.586 us |  3.83% | 44.909G | 179.634 GB/s | 70.16% |
