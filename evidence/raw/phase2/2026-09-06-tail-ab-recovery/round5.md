# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-v2/build/tail_ab' -d 0 -a 'Case=[4,5,2,3,6,7,0,1,12,13,8,9,10,11]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-recovery/round5.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-recovery/round5.md'
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
Run:  [1/14] tail_ab [Device=0 Case=4]
Pass: Cold: 0.079287ms GPU, 0.186614ms CPU, 0.08s total GPU, 0.35s total wall, 1000x 
Run:  [2/14] tail_ab [Device=0 Case=5]
Pass: Cold: 0.079556ms GPU, 0.185101ms CPU, 0.08s total GPU, 0.35s total wall, 1000x 
Run:  [3/14] tail_ab [Device=0 Case=2]
Pass: Cold: 0.079508ms GPU, 0.170309ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [4/14] tail_ab [Device=0 Case=3]
Pass: Cold: 0.076180ms GPU, 0.175377ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [5/14] tail_ab [Device=0 Case=6]
Warn: GPU throttled below threshold (721.42 MHz / 2250.00 MHz) (32% < 75%) on sample 817. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.080774ms GPU, 0.183432ms CPU, 0.08s total GPU, 0.40s total wall, 1000x 
Run:  [6/14] tail_ab [Device=0 Case=7]
Pass: Cold: 0.077138ms GPU, 0.161831ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [7/14] tail_ab [Device=0 Case=0]
Pass: Cold: 0.078197ms GPU, 0.154683ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [8/14] tail_ab [Device=0 Case=1]
Pass: Cold: 0.078972ms GPU, 0.185308ms CPU, 0.08s total GPU, 0.35s total wall, 1000x 
Run:  [9/14] tail_ab [Device=0 Case=12]
Pass: Cold: 0.077111ms GPU, 0.157945ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [10/14] tail_ab [Device=0 Case=13]
Pass: Cold: 0.077953ms GPU, 0.164106ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [11/14] tail_ab [Device=0 Case=8]
Pass: Cold: 0.079983ms GPU, 0.175788ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [12/14] tail_ab [Device=0 Case=9]
Pass: Cold: 0.076407ms GPU, 0.178637ms CPU, 0.08s total GPU, 0.34s total wall, 1000x 
Run:  [13/14] tail_ab [Device=0 Case=10]
Pass: Cold: 0.079169ms GPU, 0.174402ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [14/14] tail_ab [Device=0 Case=11]
Pass: Cold: 0.078372ms GPU, 0.189156ms CPU, 0.08s total GPU, 0.35s total wall, 1000x 
```

# Benchmark Results

## tail_ab

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Case | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|    4 |   1000x | 186.614 us | 54.77% | 79.287 us | 14.22% | 37.195G | 148.780 GB/s | 58.11% |
|    5 |   1000x | 185.101 us | 30.75% | 79.556 us | 15.63% | 37.069G | 148.278 GB/s | 57.91% |
|    2 |   1000x | 170.309 us | 29.01% | 79.508 us | 12.87% | 37.067G | 148.266 GB/s | 57.91% |
|    3 |   1000x | 175.377 us | 33.05% | 76.180 us | 12.98% | 38.686G | 154.742 GB/s | 60.44% |
|    6 |   1000x | 183.432 us | 55.13% | 80.774 us | 17.43% | 36.511G | 146.043 GB/s | 57.04% |
|    7 |   1000x | 161.831 us | 50.09% | 77.138 us | 12.30% | 38.232G | 152.927 GB/s | 59.73% |
|    0 |   1000x | 154.683 us | 32.82% | 78.197 us | 15.61% | 37.662G | 150.647 GB/s | 58.84% |
|    1 |   1000x | 185.308 us | 56.37% | 78.972 us | 16.15% | 37.292G | 149.167 GB/s | 58.26% |
|   12 |   1000x | 157.945 us | 29.77% | 77.111 us | 15.93% | 38.245G | 152.980 GB/s | 59.75% |
|   13 |   1000x | 164.106 us | 41.05% | 77.953 us | 21.11% | 37.832G | 151.329 GB/s | 59.11% |
|    8 |   1000x | 175.788 us | 61.48% | 79.983 us | 13.75% | 36.872G | 147.488 GB/s | 57.61% |
|    9 |   1000x | 178.637 us | 51.26% | 76.407 us | 12.36% | 38.598G | 154.391 GB/s | 60.30% |
|   10 |   1000x | 174.402 us | 47.38% | 79.169 us | 16.90% | 37.251G | 149.003 GB/s | 58.20% |
|   11 |   1000x | 189.156 us | 60.53% | 78.372 us | 14.46% | 37.630G | 150.520 GB/s | 58.79% |
