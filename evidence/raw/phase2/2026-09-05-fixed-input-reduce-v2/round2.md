# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/build/fixed_input_reduce' -d 0 -a 'Elements{io}=[2949121,2949120,2949119,2949116,2949088,2947072,2945024]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/round2.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/round2.md' --stopping-criterion sample-count --target-samples 1000 --cold-warmup-runs 20 --timeout 15
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
Run:  [1/7] fixed_input_reduce [Device=0 Elements{io}=2949121]
Pass: Cold: 0.079415ms GPU, 0.162746ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [2/7] fixed_input_reduce [Device=0 Elements{io}=2949120]
Pass: Cold: 0.075264ms GPU, 0.159493ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [3/7] fixed_input_reduce [Device=0 Elements{io}=2949119]
Pass: Cold: 0.077898ms GPU, 0.175578ms CPU, 0.08s total GPU, 0.34s total wall, 1000x 
Run:  [4/7] fixed_input_reduce [Device=0 Elements{io}=2949116]
Pass: Cold: 0.077627ms GPU, 0.154466ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [5/7] fixed_input_reduce [Device=0 Elements{io}=2949088]
Pass: Cold: 0.078476ms GPU, 0.156290ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
Run:  [6/7] fixed_input_reduce [Device=0 Elements{io}=2947072]
Pass: Cold: 0.076743ms GPU, 0.159535ms CPU, 0.08s total GPU, 0.32s total wall, 1000x 
Run:  [7/7] fixed_input_reduce [Device=0 Elements{io}=2945024]
Pass: Cold: 0.075822ms GPU, 0.157268ms CPU, 0.08s total GPU, 0.31s total wall, 1000x 
```

# Benchmark Results

## fixed_input_reduce

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Elements{io} |    Size    | Samples |  CPU Time  | Noise  | GPU Time  | Noise  | Elem/s  | GlobalMem BW | BWUtil |
|--------------|------------|---------|------------|--------|-----------|--------|---------|--------------|--------|
|      2949121 | 11.250 MiB |   1000x | 162.746 us | 50.32% | 79.415 us | 29.96% | 37.136G | 148.542 GB/s | 58.02% |
|      2949120 | 11.250 MiB |   1000x | 159.493 us | 49.76% | 75.264 us |  9.30% | 39.184G | 156.735 GB/s | 61.22% |
|      2949119 | 11.250 MiB |   1000x | 175.578 us | 50.15% | 77.898 us |  9.96% | 37.859G | 151.436 GB/s | 59.15% |
|      2949116 | 11.250 MiB |   1000x | 154.466 us | 51.96% | 77.627 us | 15.26% | 37.991G | 151.963 GB/s | 59.35% |
|      2949088 | 11.250 MiB |   1000x | 156.290 us | 51.05% | 78.476 us | 25.96% | 37.580G | 150.319 GB/s | 58.71% |
|      2947072 | 11.242 MiB |   1000x | 159.535 us | 50.77% | 76.743 us | 19.73% | 38.402G | 153.606 GB/s | 60.00% |
|      2945024 | 11.234 MiB |   1000x | 157.268 us | 50.25% | 75.822 us |  8.76% | 38.841G | 155.365 GB/s | 60.68% |
