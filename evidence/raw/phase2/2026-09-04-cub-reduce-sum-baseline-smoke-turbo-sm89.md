# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 --stopping-criterion entropy -a 'T{ct}=I32' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-turbo-sm89.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-04-cub-reduce-sum-baseline-smoke-turbo-sm89.md'
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
Pass: Cold: 0.021831ms GPU, 0.153598ms CPU, 0.01s total GPU, 0.23s total wall, 614x 
Run:  [2/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.038894ms GPU, 0.131505ms CPU, 0.02s total GPU, 0.17s total wall, 516x 
Run:  [3/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.367424ms GPU, 0.483979ms CPU, 0.23s total GPU, 0.40s total wall, 618x 
Run:  [4/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 5.370206ms GPU, 5.536808ms CPU, 6.19s total GPU, 6.62s total wall, 1152x 
Run:  [5/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.022274ms GPU, 0.142858ms CPU, 0.02s total GPU, 0.27s total wall, 790x 
Run:  [6/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.033593ms GPU, 0.142986ms CPU, 0.01s total GPU, 0.12s total wall, 350x 
Run:  [7/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.370523ms GPU, 0.483382ms CPU, 0.14s total GPU, 0.25s total wall, 388x 
Run:  [8/8] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 5.379579ms GPU, 5.544459ms CPU, 5.99s total GPU, 6.41s total wall, 1114x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |   Elements{io}   |    Size     | Samples |  CPU Time  | Noise  |  GPU Time  |  Noise  | Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|------------------|-------------|---------|------------|--------|------------|---------|---------|--------------|--------|
|   I32 |         I32 |     2^16 = 65536 | 256.000 KiB |    614x | 153.598 us | 89.71% |  21.831 us | 176.94% |  3.002G |  12.008 GB/s |  4.69% |
|   I32 |         I32 |   2^20 = 1048576 |   4.000 MiB |    516x | 131.505 us | 91.64% |  38.894 us | 100.56% | 26.960G | 107.839 GB/s | 42.12% |
|   I32 |         I32 |  2^24 = 16777216 |  64.000 MiB |    618x | 483.979 us | 28.89% | 367.424 us |   4.84% | 45.662G | 182.647 GB/s | 71.34% |
|   I32 |         I32 | 2^28 = 268435456 |   1.000 GiB |   1152x |   5.537 ms | 34.68% |   5.370 ms |  33.85% | 49.986G | 199.944 GB/s | 78.09% |
|   I32 |         I64 |     2^16 = 65536 | 256.000 KiB |    790x | 142.858 us | 84.03% |  22.274 us |  86.27% |  2.942G |  11.769 GB/s |  4.60% |
|   I32 |         I64 |   2^20 = 1048576 |   4.000 MiB |    350x | 142.986 us | 83.36% |  33.593 us |  22.14% | 31.214G | 124.857 GB/s | 48.77% |
|   I32 |         I64 |  2^24 = 16777216 |  64.000 MiB |    388x | 483.382 us | 29.98% | 370.523 us |  12.85% | 45.280G | 181.120 GB/s | 70.74% |
|   I32 |         I64 | 2^28 = 268435456 |   1.000 GiB |   1114x |   5.544 ms | 34.94% |   5.380 ms |  34.21% | 49.899G | 199.596 GB/s | 77.96% |
