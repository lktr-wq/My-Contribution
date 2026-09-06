# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-v2/build/tail_ab' -d 0 -a 'Case=[1,0,13,12,9,8,7,6,5,4,11,10,3,2]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-recovery/round4.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-06-tail-ab-recovery/round4.md'
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
Pass: Cold: 0.088379ms GPU, 0.187579ms CPU, 0.09s total GPU, 0.36s total wall, 1000x 
Run:  [2/14] tail_ab [Device=0 Case=0]
Pass: Cold: 0.088814ms GPU, 0.196747ms CPU, 0.09s total GPU, 0.38s total wall, 1000x 
Run:  [3/14] tail_ab [Device=0 Case=13]
Pass: Cold: 0.079884ms GPU, 0.179399ms CPU, 0.08s total GPU, 0.34s total wall, 1000x 
Run:  [4/14] tail_ab [Device=0 Case=12]
Pass: Cold: 0.081738ms GPU, 0.190798ms CPU, 0.08s total GPU, 0.36s total wall, 1000x 
Run:  [5/14] tail_ab [Device=0 Case=9]
Pass: Cold: 0.083168ms GPU, 0.194379ms CPU, 0.08s total GPU, 0.36s total wall, 1000x 
Run:  [6/14] tail_ab [Device=0 Case=8]
Pass: Cold: 0.081063ms GPU, 0.168087ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [7/14] tail_ab [Device=0 Case=7]
Pass: Cold: 0.076631ms GPU, 0.172691ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [8/14] tail_ab [Device=0 Case=6]
Pass: Cold: 0.079456ms GPU, 0.164208ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [9/14] tail_ab [Device=0 Case=5]
Pass: Cold: 0.081515ms GPU, 0.163381ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [10/14] tail_ab [Device=0 Case=4]
Pass: Cold: 0.078035ms GPU, 0.153219ms CPU, 0.08s total GPU, 0.30s total wall, 1000x 
Run:  [11/14] tail_ab [Device=0 Case=11]
Pass: Cold: 0.076861ms GPU, 0.151758ms CPU, 0.08s total GPU, 0.30s total wall, 1000x 
Run:  [12/14] tail_ab [Device=0 Case=10]
Pass: Cold: 0.077014ms GPU, 0.151855ms CPU, 0.08s total GPU, 0.30s total wall, 1000x 
Run:  [13/14] tail_ab [Device=0 Case=3]
Pass: Cold: 0.077939ms GPU, 0.160000ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [14/14] tail_ab [Device=0 Case=2]
Pass: Cold: 0.077583ms GPU, 0.161620ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
```

# Benchmark Results

## tail_ab

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Case | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|    1 |   1000x | 187.579 us | 31.30% | 88.379 us | 17.97% | 33.322G | 133.290 GB/s | 52.06% |
|    0 |   1000x | 196.747 us | 39.74% | 88.814 us | 17.83% | 33.160G | 132.638 GB/s | 51.81% |
|   13 |   1000x | 179.399 us | 48.23% | 79.884 us | 14.19% | 36.918G | 147.671 GB/s | 57.68% |
|   12 |   1000x | 190.798 us | 43.52% | 81.738 us | 19.11% | 36.080G | 144.321 GB/s | 56.37% |
|    9 |   1000x | 194.379 us | 40.75% | 83.168 us | 20.39% | 35.460G | 141.839 GB/s | 55.40% |
|    8 |   1000x | 168.087 us | 47.24% | 81.063 us | 18.99% | 36.380G | 145.522 GB/s | 56.84% |
|    7 |   1000x | 172.691 us | 66.27% | 76.631 us |  9.64% | 38.485G | 153.938 GB/s | 60.12% |
|    6 |   1000x | 164.208 us | 27.50% | 79.456 us | 15.20% | 37.116G | 148.465 GB/s | 57.99% |
|    5 |   1000x | 163.381 us | 31.56% | 81.515 us | 18.30% | 36.178G | 144.714 GB/s | 56.52% |
|    4 |   1000x | 153.219 us | 26.56% | 78.035 us | 10.83% | 37.792G | 151.167 GB/s | 59.04% |
|   11 |   1000x | 151.758 us | 36.07% | 76.861 us | 10.25% | 38.370G | 153.478 GB/s | 59.94% |
|   10 |   1000x | 151.855 us | 40.51% | 77.014 us | 13.82% | 38.293G | 153.174 GB/s | 59.83% |
|    3 |   1000x | 160.000 us | 50.48% | 77.939 us | 18.12% | 37.813G | 151.250 GB/s | 59.07% |
|    2 |   1000x | 161.620 us | 47.33% | 77.583 us | 10.52% | 37.986G | 151.945 GB/s | 59.35% |
