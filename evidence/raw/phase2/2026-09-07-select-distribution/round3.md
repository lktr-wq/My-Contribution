# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-07-select-distribution/build/select_distribution' -d 0 -a 'Case=[2,0,1,4,5,3]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-07-select-distribution/round3.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-07-select-distribution/round3.md'
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
Run:  [1/6] select_distribution [Device=0 Case=2]
Pass: Cold: 0.056000ms GPU, 0.126422ms CPU, 0.06s total GPU, 0.28s total wall, 1000x 
Run:  [2/6] select_distribution [Device=0 Case=0]
Pass: Cold: 0.058869ms GPU, 0.132284ms CPU, 0.06s total GPU, 0.29s total wall, 1000x 
Run:  [3/6] select_distribution [Device=0 Case=1]
Pass: Cold: 0.057759ms GPU, 0.126507ms CPU, 0.06s total GPU, 0.28s total wall, 1000x 
Run:  [4/6] select_distribution [Device=0 Case=4]
Pass: Cold: 0.157507ms GPU, 0.225234ms CPU, 0.16s total GPU, 0.38s total wall, 1000x 
Run:  [5/6] select_distribution [Device=0 Case=5]
Pass: Cold: 0.154042ms GPU, 0.226543ms CPU, 0.15s total GPU, 0.38s total wall, 1000x 
Run:  [6/6] select_distribution [Device=0 Case=3]
Pass: Cold: 0.151354ms GPU, 0.258854ms CPU, 0.15s total GPU, 0.43s total wall, 1000x 
```

# Benchmark Results

## select_distribution

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Case | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|------|---------|------------|--------|------------|--------|---------|--------------|--------|
|    2 |   1000x | 126.422 us | 27.91% |  56.000 us | 19.15% | 18.725G | 131.072 GB/s | 51.19% |
|    0 |   1000x | 132.284 us | 30.44% |  58.869 us | 24.91% | 17.812G | 124.684 GB/s | 48.70% |
|    1 |   1000x | 126.507 us | 26.24% |  57.759 us | 20.18% | 18.154G | 127.081 GB/s | 49.63% |
|    4 |   1000x | 225.234 us | 15.78% | 157.507 us |  9.92% | 26.629G | 186.405 GB/s | 72.81% |
|    5 |   1000x | 226.543 us | 17.62% | 154.042 us |  9.63% | 27.228G | 190.598 GB/s | 74.44% |
|    3 |   1000x | 258.854 us | 24.19% | 151.354 us |  8.52% | 27.712G | 193.984 GB/s | 75.77% |
