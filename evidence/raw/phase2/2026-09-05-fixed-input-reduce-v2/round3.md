# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/build/fixed_input_reduce' -d 0 -a 'Elements{io}=[2949116,2949119,2949120,2949121,2945024,2947072,2949088]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/round3.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/round3.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/7] fixed_input_reduce [Device=0 Elements{io}=2949116]
Pass: Cold: 0.077978ms GPU, 0.165503ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [2/7] fixed_input_reduce [Device=0 Elements{io}=2949119]
Pass: Cold: 0.078244ms GPU, 0.155509ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [3/7] fixed_input_reduce [Device=0 Elements{io}=2949120]
Pass: Cold: 0.075151ms GPU, 0.168183ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [4/7] fixed_input_reduce [Device=0 Elements{io}=2949121]
Pass: Cold: 0.077587ms GPU, 0.170129ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [5/7] fixed_input_reduce [Device=0 Elements{io}=2945024]
Pass: Cold: 0.076812ms GPU, 0.160360ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [6/7] fixed_input_reduce [Device=0 Elements{io}=2947072]
Pass: Cold: 0.077284ms GPU, 0.154533ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [7/7] fixed_input_reduce [Device=0 Elements{io}=2949088]
Pass: Cold: 0.077560ms GPU, 0.167059ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
```

# Benchmark Results

## fixed_input_reduce

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Elements{io} |    Size    | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|--------------|------------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|      2949116 | 11.250 MiB |   1000x | 165.503 us | 49.57% | 77.978 us | 11.02% | 37.820G | 151.279 GB/s | 59.09% |
|      2949119 | 11.250 MiB |   1000x | 155.509 us | 49.90% | 78.244 us | 11.76% | 37.691G | 150.765 GB/s | 58.89% |
|      2949120 | 11.250 MiB |   1000x | 168.183 us | 51.49% | 75.151 us | 10.39% | 39.242G | 156.970 GB/s | 61.31% |
|      2949121 | 11.250 MiB |   1000x | 170.129 us | 47.77% | 77.587 us | 17.57% | 38.010G | 152.042 GB/s | 59.38% |
|      2945024 | 11.234 MiB |   1000x | 160.360 us | 49.63% | 76.812 us | 12.50% | 38.341G | 153.364 GB/s | 59.90% |
|      2947072 | 11.242 MiB |   1000x | 154.533 us | 48.36% | 77.284 us | 14.73% | 38.133G | 152.532 GB/s | 59.58% |
|      2949088 | 11.250 MiB |   1000x | 167.059 us | 49.86% | 77.560 us |  8.94% | 38.023G | 152.093 GB/s | 59.40% |
