# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-v2/build/tail_ab' -d 0 -a 'Case=[1,0,9,8,7,6,5,4,13,12,11,10,3,2]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-recovery/round2.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-recovery/round2.md'
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
Run:  [1/14] tail_ab [Device=0 Case=1]
Pass: Cold: 0.079033ms GPU, 0.166738ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [2/14] tail_ab [Device=0 Case=0]
Pass: Cold: 0.080281ms GPU, 0.157659ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [3/14] tail_ab [Device=0 Case=9]
Pass: Cold: 0.078387ms GPU, 0.195807ms CPU, 0.08s total GPU, 0.37s total wall, 1000x 
Run:  [4/14] tail_ab [Device=0 Case=8]
Pass: Cold: 0.079000ms GPU, 0.188797ms CPU, 0.08s total GPU, 0.35s total wall, 1000x 
Run:  [5/14] tail_ab [Device=0 Case=7]
Pass: Cold: 0.079487ms GPU, 0.159988ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [6/14] tail_ab [Device=0 Case=6]
Pass: Cold: 0.078863ms GPU, 0.179449ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [7/14] tail_ab [Device=0 Case=5]
Pass: Cold: 0.078606ms GPU, 0.166382ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [8/14] tail_ab [Device=0 Case=4]
Pass: Cold: 0.078706ms GPU, 0.177828ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [9/14] tail_ab [Device=0 Case=13]
Pass: Cold: 0.079245ms GPU, 0.172675ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [10/14] tail_ab [Device=0 Case=12]
Warn: GPU throttled below threshold (993.68 MHz / 2250.00 MHz) (44% < 75%) on sample 630. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.078526ms GPU, 0.156689ms CPU, 0.08s total GPU, 0.36s total wall, 1000x 
Run:  [11/14] tail_ab [Device=0 Case=11]
Pass: Cold: 0.078053ms GPU, 0.159329ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [12/14] tail_ab [Device=0 Case=10]
Pass: Cold: 0.075902ms GPU, 0.171470ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [13/14] tail_ab [Device=0 Case=3]
Pass: Cold: 0.077500ms GPU, 0.161591ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [14/14] tail_ab [Device=0 Case=2]
Pass: Cold: 0.077652ms GPU, 0.164751ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
```

# Benchmark Results

## tail_ab

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Case | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|    1 |   1000x | 166.738 us | 34.46% | 79.033 us | 15.13% | 37.263G | 149.053 GB/s | 58.22% |
|    0 |   1000x | 157.659 us | 28.80% | 80.281 us | 23.54% | 36.684G | 146.735 GB/s | 57.31% |
|    9 |   1000x | 195.807 us | 55.27% | 78.387 us | 15.26% | 37.623G | 150.490 GB/s | 58.78% |
|    8 |   1000x | 188.797 us | 56.44% | 79.000 us | 16.72% | 37.331G | 149.323 GB/s | 58.32% |
|    7 |   1000x | 159.988 us | 26.58% | 79.487 us | 15.00% | 37.102G | 148.407 GB/s | 57.96% |
|    6 |   1000x | 179.449 us | 35.18% | 78.863 us | 16.66% | 37.396G | 149.582 GB/s | 58.42% |
|    5 |   1000x | 166.382 us | 29.21% | 78.606 us | 16.16% | 37.518G | 150.070 GB/s | 58.61% |
|    4 |   1000x | 177.828 us | 28.48% | 78.706 us | 15.17% | 37.470G | 149.879 GB/s | 58.54% |
|   13 |   1000x | 172.675 us | 27.36% | 79.245 us | 14.32% | 37.215G | 148.861 GB/s | 58.14% |
|   12 |   1000x | 156.689 us | 31.53% | 78.526 us | 12.25% | 37.556G | 150.225 GB/s | 58.67% |
|   11 |   1000x | 159.329 us | 29.41% | 78.053 us | 12.25% | 37.784G | 151.135 GB/s | 59.03% |
|   10 |   1000x | 171.470 us | 46.69% | 75.902 us |  9.72% | 38.854G | 155.418 GB/s | 60.70% |
|    3 |   1000x | 161.591 us | 25.00% | 77.500 us | 11.20% | 38.027G | 152.107 GB/s | 59.41% |
|    2 |   1000x | 164.751 us | 30.68% | 77.652 us | 11.83% | 37.952G | 151.809 GB/s | 59.29% |
