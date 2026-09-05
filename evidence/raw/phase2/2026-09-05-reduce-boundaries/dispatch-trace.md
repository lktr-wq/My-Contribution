# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 -a 'T{ct}=I32' -a 'OffsetT{ct}=I32' -a 'Elements{io}=[4095,4096,4097,16777216,16777217]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/dispatch-trace.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-reduce-boundaries/dispatch-trace.md' --profile
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
Run:  [1/5] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4095]
Pass: Cold: 24.472576ms GPU, 24.832037ms CPU, 0.02s total GPU, 0.03s total wall, 1x 
Run:  [2/5] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4096]
Pass: Cold: 1.402880ms GPU, 1.439977ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [3/5] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=4097]
Pass: Cold: 1.450976ms GPU, 1.479678ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [4/5] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777216]
Pass: Cold: 1.573888ms GPU, 1.616168ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [5/5] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=16777217]
Pass: Cold: 1.615872ms GPU, 1.648739ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} | Elements{io} |    Size    | Samples | CPU Time  | Noise | GPU Time  | Noise |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|--------------|------------|---------|-----------|-------|-----------|-------|----------|--------------|--------|
|   I32 |         I32 |         4095 | 15.996 KiB |      1x | 24.832 ms |  inf% | 24.473 ms |  inf% | 167.330K | 669.484 KB/s |  0.00% |
|   I32 |         I32 |         4096 | 16.000 KiB |      1x |  1.440 ms |  inf% |  1.403 ms |  inf% |   2.920M |  11.682 MB/s |  0.00% |
|   I32 |         I32 |         4097 | 16.004 KiB |      1x |  1.480 ms |  inf% |  1.451 ms |  inf% |   2.824M |  11.297 MB/s |  0.00% |
|   I32 |         I32 |     16777216 | 64.000 MiB |      1x |  1.616 ms |  inf% |  1.574 ms |  inf% |  10.660G |  42.639 GB/s | 16.65% |
|   I32 |         I32 |     16777217 | 64.000 MiB |      1x |  1.649 ms |  inf% |  1.616 ms |  inf% |  10.383G |  41.531 GB/s | 16.22% |
