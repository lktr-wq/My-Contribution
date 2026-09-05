# Command Line

```
'/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/build/fixed_input_reduce' -d 0 -a 'Elements{io}=[2945024,2947072,2949088,2949116,2949119,2949120,2949121]' --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/trace.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-fixed-input-reduce-v2/trace.md' --profile
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
Pass: Cold: 0.099328ms GPU, 0.795883ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [2/7] fixed_input_reduce [Device=0 Elements{io}=2947072]
Pass: Cold: 0.120832ms GPU, 0.164849ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [3/7] fixed_input_reduce [Device=0 Elements{io}=2949088]
Pass: Cold: 0.136992ms GPU, 0.170169ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [4/7] fixed_input_reduce [Device=0 Elements{io}=2949116]
Pass: Cold: 0.152320ms GPU, 0.190106ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [5/7] fixed_input_reduce [Device=0 Elements{io}=2949119]
Pass: Cold: 0.105472ms GPU, 0.149621ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [6/7] fixed_input_reduce [Device=0 Elements{io}=2949120]
Pass: Cold: 0.099200ms GPU, 0.164839ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
Run:  [7/7] fixed_input_reduce [Device=0 Elements{io}=2949121]
Pass: Cold: 0.123904ms GPU, 0.165840ms CPU, 0.00s total GPU, 0.00s total wall, 1x 
```

# Benchmark Results

## fixed_input_reduce

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| Elements{io} |    Size    | Samples |  CPU Time  | Noise |  GPU Time  | Noise | Elem/s  | GlobalMem BW | BWUtil |
|--------------|------------|---------|------------|-------|------------|-------|---------|--------------|--------|
|      2945024 | 11.234 MiB |      1x | 795.883 us |  inf% |  99.328 us |  inf% | 29.649G | 118.598 GB/s | 46.32% |
|      2947072 | 11.242 MiB |      1x | 164.849 us |  inf% | 120.832 us |  inf% | 24.390G |  97.559 GB/s | 38.10% |
|      2949088 | 11.250 MiB |      1x | 170.169 us |  inf% | 136.992 us |  inf% | 21.527G |  86.110 GB/s | 33.63% |
|      2949116 | 11.250 MiB |      1x | 190.106 us |  inf% | 152.320 us |  inf% | 19.361G |  77.445 GB/s | 30.25% |
|      2949119 | 11.250 MiB |      1x | 149.621 us |  inf% | 105.472 us |  inf% | 27.961G | 111.845 GB/s | 43.68% |
|      2949120 | 11.250 MiB |      1x | 164.839 us |  inf% |  99.200 us |  inf% | 29.729G | 118.916 GB/s | 46.45% |
|      2949121 | 11.250 MiB |      1x | 165.840 us |  inf% | 123.904 us |  inf% | 23.802G |  95.207 GB/s | 37.19% |
