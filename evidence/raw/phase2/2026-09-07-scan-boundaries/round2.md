# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-07-scan-boundaries/build/scan_boundaries' -d 0 -a 'N=[245761,245760,245759,46081,46080,46079,1921,1920,1919]' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15 --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-07-scan-boundaries/round2.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-07-scan-boundaries/round2.md'
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
Run:  [1/9] scan_boundaries [Device=0 N=245761]
Pass: Cold: 0.023954ms GPU, 0.106427ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [2/9] scan_boundaries [Device=0 N=245760]
Pass: Cold: 0.024419ms GPU, 0.115518ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [3/9] scan_boundaries [Device=0 N=245759]
Pass: Cold: 0.022448ms GPU, 0.121565ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [4/9] scan_boundaries [Device=0 N=46081]
Pass: Cold: 0.022103ms GPU, 0.103101ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [5/9] scan_boundaries [Device=0 N=46080]
Pass: Cold: 0.024568ms GPU, 0.110359ms CPU, 0.02s total GPU, 0.28s total wall, 1000x 
Run:  [6/9] scan_boundaries [Device=0 N=46079]
Pass: Cold: 0.019936ms GPU, 0.101636ms CPU, 0.02s total GPU, 0.26s total wall, 1000x 
Run:  [7/9] scan_boundaries [Device=0 N=1921]
Pass: Cold: 0.021436ms GPU, 0.105822ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [8/9] scan_boundaries [Device=0 N=1920]
Pass: Cold: 0.023360ms GPU, 0.107229ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
Run:  [9/9] scan_boundaries [Device=0 N=1919]
Pass: Cold: 0.023415ms GPU, 0.102695ms CPU, 0.02s total GPU, 0.27s total wall, 1000x 
```

# Benchmark Results

## scan_boundaries

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

|   N    | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|--------|---------|------------|--------|-----------|--------|---------|--------------|--------|
| 245761 |   1000x | 106.427 us | 37.63% | 23.954 us | 58.11% | 10.260G |  82.077 GB/s | 32.06% |
| 245760 |   1000x | 115.518 us | 40.50% | 24.419 us | 68.80% | 10.064G |  80.516 GB/s | 31.45% |
| 245759 |   1000x | 121.565 us | 44.01% | 22.448 us | 69.72% | 10.948G |  87.582 GB/s | 34.21% |
|  46081 |   1000x | 103.101 us | 38.34% | 22.103 us | 82.49% |  2.085G |  16.679 GB/s |  6.51% |
|  46080 |   1000x | 110.359 us | 46.58% | 24.568 us | 88.27% |  1.876G |  15.005 GB/s |  5.86% |
|  46079 |   1000x | 101.636 us | 41.92% | 19.936 us | 78.76% |  2.311G |  18.491 GB/s |  7.22% |
|   1921 |   1000x | 105.822 us | 38.51% | 21.436 us | 83.65% | 89.615M | 716.916 MB/s |  0.28% |
|   1920 |   1000x | 107.229 us | 39.67% | 23.360 us | 89.95% | 82.191M | 657.528 MB/s |  0.26% |
|   1919 |   1000x | 102.695 us | 37.47% | 23.415 us | 85.56% | 81.957M | 655.659 MB/s |  0.26% |
