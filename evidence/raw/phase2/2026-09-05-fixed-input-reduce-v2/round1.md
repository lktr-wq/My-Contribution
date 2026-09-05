# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/build/fixed_input_reduce' -d 0 -a 'Elements{io}=[2945024,2947072,2949088,2949116,2949119,2949120,2949121]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/round1.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/round1.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/7] fixed_input_reduce [Device=0 Elements{io}=2945024]
Pass: Cold: 0.089349ms GPU, 0.179436ms CPU, 0.09s total GPU, 0.36s total wall, 1000x 
Run:  [2/7] fixed_input_reduce [Device=0 Elements{io}=2947072]
Pass: Cold: 0.079893ms GPU, 0.164593ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [3/7] fixed_input_reduce [Device=0 Elements{io}=2949088]
Pass: Cold: 0.079266ms GPU, 0.159555ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [4/7] fixed_input_reduce [Device=0 Elements{io}=2949116]
Pass: Cold: 0.078526ms GPU, 0.156692ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [5/7] fixed_input_reduce [Device=0 Elements{io}=2949119]
Pass: Cold: 0.078400ms GPU, 0.160883ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [6/7] fixed_input_reduce [Device=0 Elements{io}=2949120]
Pass: Cold: 0.075583ms GPU, 0.167969ms CPU, 0.08s total GPU, 0.33s total wall, 1000x 
Run:  [7/7] fixed_input_reduce [Device=0 Elements{io}=2949121]
Pass: Cold: 0.076953ms GPU, 0.160400ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
```

# Benchmark Results

## fixed_input_reduce

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Elements{io} |    Size    | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|--------------|------------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|      2945024 | 11.234 MiB |   1000x | 179.436 us | 48.19% | 89.349 us | 14.99% | 32.961G | 131.843 GB/s | 51.49% |
|      2947072 | 11.242 MiB |   1000x | 164.593 us | 50.76% | 79.893 us | 13.14% | 36.888G | 147.551 GB/s | 57.63% |
|      2949088 | 11.250 MiB |   1000x | 159.555 us | 48.59% | 79.266 us | 24.58% | 37.205G | 148.819 GB/s | 58.13% |
|      2949116 | 11.250 MiB |   1000x | 156.692 us | 51.30% | 78.526 us | 22.46% | 37.556G | 150.224 GB/s | 58.67% |
|      2949119 | 11.250 MiB |   1000x | 160.883 us | 50.21% | 78.400 us | 11.54% | 37.616G | 150.465 GB/s | 58.77% |
|      2949120 | 11.250 MiB |   1000x | 167.969 us | 48.77% | 75.583 us | 25.12% | 39.019G | 156.074 GB/s | 60.96% |
|      2949121 | 11.250 MiB |   1000x | 160.400 us | 50.80% | 76.953 us | 28.03% | 38.324G | 153.295 GB/s | 59.87% |
