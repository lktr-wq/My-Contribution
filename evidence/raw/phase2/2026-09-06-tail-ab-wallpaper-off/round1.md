# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-v2/build/tail_ab' -d 0 -a 'Case=[12,13,4,5,6,7,8,9,10,11,0,1,2,3]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-wallpaper-off/round1.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-wallpaper-off/round1.md'
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
Run:  [1/14] tail_ab [Device=0 Case=12]
Warn: GPU throttled below threshold (1447.30 MHz / 2250.00 MHz) (64% < 75%) on sample 200. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.078542ms GPU, 0.176111ms CPU, 0.08s total GPU, 0.38s total wall, 1000x 
Run:  [2/14] tail_ab [Device=0 Case=13]
Pass: Cold: 0.080669ms GPU, 0.170217ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [3/14] tail_ab [Device=0 Case=4]
Pass: Cold: 0.081974ms GPU, 0.166430ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [4/14] tail_ab [Device=0 Case=5]
Pass: Cold: 0.079130ms GPU, 0.157969ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [5/14] tail_ab [Device=0 Case=6]
Pass: Cold: 0.080019ms GPU, 0.164801ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [6/14] tail_ab [Device=0 Case=7]
Pass: Cold: 0.080822ms GPU, 0.174331ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [7/14] tail_ab [Device=0 Case=8]
Pass: Cold: 0.079146ms GPU, 0.159720ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [8/14] tail_ab [Device=0 Case=9]
Pass: Cold: 0.075147ms GPU, 0.167366ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [9/14] tail_ab [Device=0 Case=10]
Pass: Cold: 0.075468ms GPU, 0.157629ms CPU, 0.08s total GPU, 0.30s total wall, 1000x 
Run:  [10/14] tail_ab [Device=0 Case=11]
Pass: Cold: 0.074898ms GPU, 0.146987ms CPU, 0.07s total GPU, 0.29s total wall, 1000x 
Run:  [11/14] tail_ab [Device=0 Case=0]
Warn: GPU throttled below threshold (696.16 MHz / 2250.00 MHz) (31% < 75%) on sample 458. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.075066ms GPU, 0.152207ms CPU, 0.08s total GPU, 0.35s total wall, 1000x 
Run:  [12/14] tail_ab [Device=0 Case=1]
Pass: Cold: 0.074314ms GPU, 0.165496ms CPU, 0.07s total GPU, 0.32s total wall, 1000x 
Run:  [13/14] tail_ab [Device=0 Case=2]
Pass: Cold: 0.077826ms GPU, 0.155173ms CPU, 0.08s total GPU, 0.30s total wall, 1000x 
Run:  [14/14] tail_ab [Device=0 Case=3]
Pass: Cold: 0.077535ms GPU, 0.151156ms CPU, 0.08s total GPU, 0.30s total wall, 1000x 
```

# Benchmark Results

## tail_ab

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Case | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|   12 |   1000x | 176.111 us | 33.28% | 78.542 us | 15.70% | 37.548G | 150.193 GB/s | 58.66% |
|   13 |   1000x | 170.217 us | 29.81% | 80.669 us | 18.91% | 36.558G | 146.234 GB/s | 57.12% |
|    4 |   1000x | 166.430 us | 26.33% | 81.974 us | 15.43% | 35.976G | 143.903 GB/s | 56.20% |
|    5 |   1000x | 157.969 us | 25.65% | 79.130 us | 15.76% | 37.269G | 149.076 GB/s | 58.23% |
|    6 |   1000x | 164.801 us | 28.81% | 80.019 us | 13.38% | 36.855G | 147.421 GB/s | 57.58% |
|    7 |   1000x | 174.331 us | 33.38% | 80.822 us | 19.09% | 36.489G | 145.955 GB/s | 57.01% |
|    8 |   1000x | 159.720 us | 29.05% | 79.146 us | 11.79% | 37.262G | 149.047 GB/s | 58.21% |
|    9 |   1000x | 167.366 us | 30.47% | 75.147 us | 13.14% | 39.245G | 156.979 GB/s | 61.31% |
|   10 |   1000x | 157.629 us | 27.58% | 75.468 us | 12.92% | 39.078G | 156.311 GB/s | 61.05% |
|   11 |   1000x | 146.987 us | 24.76% | 74.898 us | 11.12% | 39.375G | 157.501 GB/s | 61.52% |
|    0 |   1000x | 152.207 us | 27.71% | 75.066 us | 12.59% | 39.233G | 156.931 GB/s | 61.29% |
|    1 |   1000x | 165.496 us | 30.70% | 74.314 us |  7.55% | 39.630G | 158.519 GB/s | 61.91% |
|    2 |   1000x | 155.173 us | 28.65% | 77.826 us | 10.81% | 37.867G | 151.470 GB/s | 59.16% |
|    3 |   1000x | 151.156 us | 25.34% | 77.535 us | 14.64% | 38.010G | 152.039 GB/s | 59.38% |
