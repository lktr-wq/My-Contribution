# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce/build/fixed_input_reduce' -d 0 -a 'Elements{io}=[2945024,2947072,2949088,2949116,2949119,2949120,2949121]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce/trace.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce/trace.md' --profile
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
Pass: Cold: 0.080896ms GPU, 0.679610ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [2/7] fixed_input_reduce [Device=0 Elements{io}=2947072]
Pass: Cold: 0.110592ms GPU, 0.143129ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [3/7] fixed_input_reduce [Device=0 Elements{io}=2949088]
Pass: Cold: 0.141312ms GPU, 0.197380ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [4/7] fixed_input_reduce [Device=0 Elements{io}=2949116]
Pass: Cold: 0.128000ms GPU, 0.159639ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [5/7] fixed_input_reduce [Device=0 Elements{io}=2949119]
Pass: Cold: 0.110592ms GPU, 0.146505ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [6/7] fixed_input_reduce [Device=0 Elements{io}=2949120]
Pass: Cold: 0.121888ms GPU, 0.167955ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [7/7] fixed_input_reduce [Device=0 Elements{io}=2949121]
Pass: Cold: 0.126880ms GPU, 0.171351ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
```

# Benchmark Results

## fixed_input_reduce

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Elements{io} |    Size    | Samples |  CPU Time  | Noise |  GPU Time  | Noise | Elem/s  | GlobalMem BW | BWUtil |
|--------------|------------|---------|------------|-------|------------|-------|---------|--------------|--------|
|      2945024 | 11.234 MiB |      1x | 679.610 us |  inf% |  80.896 us |  inf% | 36.405G | 145.620 GB/s | 56.88% |
|      2947072 | 11.242 MiB |      1x | 143.129 us |  inf% | 110.592 us |  inf% | 26.648G | 106.593 GB/s | 41.63% |
|      2949088 | 11.250 MiB |      1x | 197.380 us |  inf% | 141.312 us |  inf% | 20.869G |  83.477 GB/s | 32.60% |
|      2949116 | 11.250 MiB |      1x | 159.639 us |  inf% | 128.000 us |  inf% | 23.040G |  92.160 GB/s | 36.00% |
|      2949119 | 11.250 MiB |      1x | 146.505 us |  inf% | 110.592 us |  inf% | 26.667G | 106.667 GB/s | 41.66% |
|      2949120 | 11.250 MiB |      1x | 167.955 us |  inf% | 121.888 us |  inf% | 24.195G |  96.781 GB/s | 37.80% |
|      2949121 | 11.250 MiB |      1x | 171.351 us |  inf% | 126.880 us |  inf% | 23.243G |  92.974 GB/s | 36.31% |
