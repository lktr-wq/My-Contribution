# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 --stopping-criterion entropy --quiet --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-cub-reduce-sum-official-full-run2-turbo-sm89.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-05-cub-reduce-sum-official-full-run2-turbo-sm89.md'
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
Run:  [1/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.022622ms GPU, 0.156621ms CPU, 0.02s total GPU, 0.41s total wall, 1070x 
Run:  [2/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.026674ms GPU, 0.143473ms CPU, 0.02s total GPU, 0.26s total wall, 774x 
Run:  [3/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.101899ms GPU, 0.230426ms CPU, 0.06s total GPU, 0.24s total wall, 594x 
Run:  [4/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 1.379396ms GPU, 1.517893ms CPU, 1.03s total GPU, 1.26s total wall, 748x 
Run:  [5/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.021781ms GPU, 0.127989ms CPU, 0.01s total GPU, 0.18s total wall, 554x 
Run:  [6/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.021721ms GPU, 0.119663ms CPU, 0.01s total GPU, 0.11s total wall, 370x 
Run:  [7/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.103480ms GPU, 0.197674ms CPU, 0.05s total GPU, 0.17s total wall, 458x 
Run:  [8/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 1.388323ms GPU, 1.519097ms CPU, 1.01s total GPU, 1.22s total wall, 726x 
Run:  [9/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.021615ms GPU, 0.128895ms CPU, 0.01s total GPU, 0.21s total wall, 674x 
Run:  [10/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.023484ms GPU, 0.121067ms CPU, 0.01s total GPU, 0.15s total wall, 484x 
Run:  [11/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.194166ms GPU, 0.290817ms CPU, 0.09s total GPU, 0.21s total wall, 462x 
Run:  [12/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 2.728573ms GPU, 2.866478ms CPU, 2.81s total GPU, 3.13s total wall, 1030x 
Run:  [13/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.025218ms GPU, 0.131381ms CPU, 0.02s total GPU, 0.21s total wall, 650x 
Run:  [14/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.023861ms GPU, 0.122677ms CPU, 0.01s total GPU, 0.14s total wall, 468x 
Run:  [15/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.194470ms GPU, 0.293484ms CPU, 0.08s total GPU, 0.18s total wall, 410x 
Run:  [16/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 2.732929ms GPU, 2.870786ms CPU, 2.85s total GPU, 3.17s total wall, 1042x 
Run:  [17/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.020093ms GPU, 0.130784ms CPU, 0.01s total GPU, 0.15s total wall, 480x 
Run:  [18/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.034906ms GPU, 0.141640ms CPU, 0.02s total GPU, 0.19s total wall, 574x 
Run:  [19/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.367802ms GPU, 0.478221ms CPU, 0.27s total GPU, 0.46s total wall, 724x 
Run:  [20/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 5.387255ms GPU, 5.545121ms CPU, 5.95s total GPU, 6.34s total wall, 1104x 
Run:  [21/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^16]
Warn: GPU throttled below threshold (926.52 MHz / 2250.00 MHz) (41% < 75%) on sample 369. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.022309ms GPU, 0.138101ms CPU, 0.01s total GPU, 0.27s total wall, 646x 
Run:  [22/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.034112ms GPU, 0.133921ms CPU, 0.02s total GPU, 0.15s total wall, 490x 
Run:  [23/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.371163ms GPU, 0.508134ms CPU, 0.28s total GPU, 0.50s total wall, 744x 
Run:  [24/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 5.395641ms GPU, 5.560892ms CPU, 6.28s total GPU, 6.72s total wall, 1164x 
Run:  [25/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.023719ms GPU, 0.133153ms CPU, 0.01s total GPU, 0.15s total wall, 456x 
Run:  [26/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.056287ms GPU, 0.155835ms CPU, 0.03s total GPU, 0.18s total wall, 528x 
Run:  [27/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.711151ms GPU, 0.845568ms CPU, 0.43s total GPU, 0.61s total wall, 606x 
Run:  [28/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 10.828529ms GPU, 10.998133ms CPU, 13.06s total GPU, 13.56s total wall, 1206x 
Run:  [29/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.026545ms GPU, 0.126804ms CPU, 0.02s total GPU, 0.20s total wall, 656x 
Run:  [30/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.055800ms GPU, 0.159354ms CPU, 0.04s total GPU, 0.21s total wall, 628x 
Run:  [31/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.711742ms GPU, 0.820399ms CPU, 0.41s total GPU, 0.57s total wall, 578x 
Run:  [32/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 10.821465ms GPU, 10.997770ms CPU, 13.48s total GPU, 14.00s total wall, 1246x 
Run:  [33/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.020457ms GPU, 0.130542ms CPU, 0.01s total GPU, 0.19s total wall, 586x 
Run:  [34/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.109396ms GPU, 0.207094ms CPU, 0.09s total GPU, 0.30s total wall, 794x 
Run:  [35/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 1.406157ms GPU, 1.534700ms CPU, 1.02s total GPU, 1.23s total wall, 726x 
Run:  [36/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 21.473936ms GPU, 21.662679ms CPU, 14.71s total GPU, 15.02s total wall, 685x 
Run:  [37/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.026470ms GPU, 0.136191ms CPU, 0.02s total GPU, 0.25s total wall, 762x 
Run:  [38/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.109045ms GPU, 0.212651ms CPU, 0.05s total GPU, 0.18s total wall, 460x 
Run:  [39/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 1.397414ms GPU, 1.536244ms CPU, 1.37s total GPU, 1.67s total wall, 978x 
Run:  [40/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 21.491577ms GPU, 21.678361ms CPU, 14.70s total GPU, 15.01s total wall, 684x 
Run:  [41/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.023083ms GPU, 0.123920ms CPU, 0.01s total GPU, 0.18s total wall, 564x 
Run:  [42/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.034028ms GPU, 0.129103ms CPU, 0.01s total GPU, 0.13s total wall, 434x 
Run:  [43/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.370205ms GPU, 0.495393ms CPU, 0.19s total GPU, 0.34s total wall, 524x 
Run:  [44/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 5.403475ms GPU, 5.565604ms CPU, 6.03s total GPU, 6.44s total wall, 1116x 
Run:  [45/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.022324ms GPU, 0.127539ms CPU, 0.01s total GPU, 0.17s total wall, 544x 
Run:  [46/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.036969ms GPU, 0.152489ms CPU, 0.03s total GPU, 0.25s total wall, 748x 
Run:  [47/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.368182ms GPU, 0.485870ms CPU, 0.25s total GPU, 0.44s total wall, 678x 
Run:  [48/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 5.383528ms GPU, 5.546058ms CPU, 6.80s total GPU, 7.27s total wall, 1264x 
Run:  [49/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.023235ms GPU, 0.125986ms CPU, 0.01s total GPU, 0.18s total wall, 568x 
Run:  [50/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.057097ms GPU, 0.147219ms CPU, 0.03s total GPU, 0.18s total wall, 560x 
Run:  [51/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.714247ms GPU, 0.840654ms CPU, 0.54s total GPU, 0.76s total wall, 756x 
Run:  [52/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 10.805952ms GPU, 10.980968ms CPU, 14.44s total GPU, 15.01s total wall, 1336x 
Run:  [53/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.022206ms GPU, 0.126811ms CPU, 0.01s total GPU, 0.18s total wall, 566x 
Run:  [54/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.056778ms GPU, 0.147103ms CPU, 0.02s total GPU, 0.13s total wall, 390x 
Run:  [55/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.716988ms GPU, 0.827286ms CPU, 0.44s total GPU, 0.61s total wall, 614x 
Run:  [56/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 10.828945ms GPU, 11.002326ms CPU, 13.38s total GPU, 13.89s total wall, 1236x 
Run:  [57/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.021656ms GPU, 0.128603ms CPU, 0.02s total GPU, 0.25s total wall, 794x 
Run:  [58/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.059449ms GPU, 0.170588ms CPU, 0.03s total GPU, 0.16s total wall, 450x 
Run:  [59/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.718770ms GPU, 0.847753ms CPU, 0.48s total GPU, 0.67s total wall, 668x 
Run:  [60/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 10.817840ms GPU, 10.993163ms CPU, 14.45s total GPU, 15.00s total wall, 1336x 
Run:  [61/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.023156ms GPU, 0.128932ms CPU, 0.01s total GPU, 0.18s total wall, 548x 
Run:  [62/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.055089ms GPU, 0.170772ms CPU, 0.03s total GPU, 0.19s total wall, 516x 
Run:  [63/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.718166ms GPU, 0.833947ms CPU, 0.39s total GPU, 0.54s total wall, 540x 
Run:  [64/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 10.812146ms GPU, 10.987643ms CPU, 13.34s total GPU, 13.87s total wall, 1234x 
Run:  [65/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.020119ms GPU, 0.126673ms CPU, 0.01s total GPU, 0.16s total wall, 512x 
Run:  [66/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.025435ms GPU, 0.128311ms CPU, 0.01s total GPU, 0.16s total wall, 514x 
Run:  [67/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.193437ms GPU, 0.297652ms CPU, 0.09s total GPU, 0.21s total wall, 450x 
Run:  [68/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 2.713409ms GPU, 2.853849ms CPU, 2.81s total GPU, 3.13s total wall, 1034x 
Run:  [69/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.020638ms GPU, 0.130911ms CPU, 0.01s total GPU, 0.17s total wall, 532x 
Run:  [70/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.023939ms GPU, 0.133219ms CPU, 0.01s total GPU, 0.17s total wall, 524x 
Run:  [71/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.194397ms GPU, 0.305902ms CPU, 0.13s total GPU, 0.32s total wall, 666x 
Run:  [72/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 2.722450ms GPU, 2.876769ms CPU, 1.75s total GPU, 1.97s total wall, 644x 
Run:  [73/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.021485ms GPU, 0.126692ms CPU, 0.01s total GPU, 0.13s total wall, 424x 
Run:  [74/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.027741ms GPU, 0.129171ms CPU, 0.01s total GPU, 0.16s total wall, 516x 
Run:  [75/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.192519ms GPU, 0.303508ms CPU, 0.10s total GPU, 0.24s total wall, 510x 
Run:  [76/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 2.709387ms GPU, 2.847445ms CPU, 2.37s total GPU, 2.65s total wall, 874x 
Run:  [77/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.020692ms GPU, 0.135976ms CPU, 0.01s total GPU, 0.16s total wall, 472x 
Run:  [78/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.023958ms GPU, 0.139056ms CPU, 0.01s total GPU, 0.16s total wall, 480x 
Run:  [79/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.193476ms GPU, 0.299900ms CPU, 0.10s total GPU, 0.23s total wall, 504x 
Run:  [80/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 2.715582ms GPU, 2.854517ms CPU, 2.38s total GPU, 2.66s total wall, 876x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |   Elements{io}   |    Size     | Samples |  CPU Time  | Noise  |  GPU Time  |  Noise  |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|------------------|-------------|---------|------------|--------|------------|---------|----------|--------------|--------|
|    I8 |         I32 |     2^16 = 65536 |  64.000 KiB |   1070x | 156.621 us | 85.71% |  22.622 us | 137.14% |   2.897G |   2.897 GB/s |  1.13% |
|    I8 |         I32 |   2^20 = 1048576 |   1.000 MiB |    774x | 143.473 us | 79.25% |  26.674 us |  74.89% |  39.311G |  39.311 GB/s | 15.35% |
|    I8 |         I32 |  2^24 = 16777216 |  16.000 MiB |    594x | 230.426 us | 55.88% | 101.899 us |  11.27% | 164.645G | 164.645 GB/s | 64.31% |
|    I8 |         I32 | 2^28 = 268435456 | 256.000 MiB |    748x |   1.518 ms | 45.26% |   1.379 ms |  41.74% | 194.604G | 194.604 GB/s | 76.01% |
|    I8 |         I64 |     2^16 = 65536 |  64.000 KiB |    554x | 127.989 us | 94.47% |  21.781 us |  81.74% |   3.009G |   3.009 GB/s |  1.18% |
|    I8 |         I64 |   2^20 = 1048576 |   1.000 MiB |    370x | 119.663 us | 98.41% |  21.721 us |  77.66% |  48.275G |  48.275 GB/s | 18.86% |
|    I8 |         I64 |  2^24 = 16777216 |  16.000 MiB |    458x | 197.674 us | 61.80% | 103.480 us |  36.79% | 162.130G | 162.130 GB/s | 63.32% |
|    I8 |         I64 | 2^28 = 268435456 | 256.000 MiB |    726x |   1.519 ms | 46.48% |   1.388 ms |  41.31% | 193.352G | 193.352 GB/s | 75.52% |
|   I16 |         I32 |     2^16 = 65536 | 128.000 KiB |    674x | 128.895 us | 83.88% |  21.615 us |  74.77% |   3.032G |   6.064 GB/s |  2.37% |
|   I16 |         I32 |   2^20 = 1048576 |   2.000 MiB |    484x | 121.067 us | 93.04% |  23.484 us |  50.60% |  44.650G |  89.301 GB/s | 34.88% |
|   I16 |         I32 |  2^24 = 16777216 |  32.000 MiB |    462x | 290.817 us | 44.57% | 194.166 us |  19.75% |  86.407G | 172.813 GB/s | 67.50% |
|   I16 |         I32 | 2^28 = 268435456 | 512.000 MiB |   1030x |   2.866 ms | 42.09% |   2.729 ms |  40.85% |  98.379G | 196.759 GB/s | 76.85% |
|   I16 |         I64 |     2^16 = 65536 | 128.000 KiB |    650x | 131.381 us | 92.00% |  25.218 us | 190.29% |   2.599G |   5.198 GB/s |  2.03% |
|   I16 |         I64 |   2^20 = 1048576 |   2.000 MiB |    468x | 122.677 us | 84.47% |  23.861 us |  33.96% |  43.946G |  87.891 GB/s | 34.33% |
|   I16 |         I64 |  2^24 = 16777216 |  32.000 MiB |    410x | 293.484 us | 41.94% | 194.470 us |   8.16% |  86.271G | 172.543 GB/s | 67.39% |
|   I16 |         I64 | 2^28 = 268435456 | 512.000 MiB |   1042x |   2.871 ms | 42.17% |   2.733 ms |  40.62% |  98.223G | 196.445 GB/s | 76.73% |
|   I32 |         I32 |     2^16 = 65536 | 256.000 KiB |    480x | 130.784 us | 87.77% |  20.093 us |  89.74% |   3.262G |  13.047 GB/s |  5.10% |
|   I32 |         I32 |   2^20 = 1048576 |   4.000 MiB |    574x | 141.640 us | 89.22% |  34.906 us | 102.82% |  30.040G | 120.161 GB/s | 46.93% |
|   I32 |         I32 |  2^24 = 16777216 |  64.000 MiB |    724x | 478.221 us | 29.43% | 367.802 us |   5.17% |  45.615G | 182.459 GB/s | 71.26% |
|   I32 |         I32 | 2^28 = 268435456 |   1.000 GiB |   1104x |   5.545 ms | 35.49% |   5.387 ms |  34.64% |  49.828G | 199.312 GB/s | 77.85% |
|   I32 |         I64 |     2^16 = 65536 | 256.000 KiB |    646x | 138.101 us | 81.24% |  22.309 us | 164.01% |   2.938G |  11.751 GB/s |  4.59% |
|   I32 |         I64 |   2^20 = 1048576 |   4.000 MiB |    490x | 133.921 us | 80.05% |  34.112 us |  27.45% |  30.739G | 122.958 GB/s | 48.02% |
|   I32 |         I64 |  2^24 = 16777216 |  64.000 MiB |    744x | 508.134 us | 28.88% | 371.163 us |  11.30% |  45.202G | 180.807 GB/s | 70.62% |
|   I32 |         I64 | 2^28 = 268435456 |   1.000 GiB |   1164x |   5.561 ms | 36.04% |   5.396 ms |  35.23% |  49.750G | 199.002 GB/s | 77.73% |
|   I64 |         I32 |     2^16 = 65536 | 512.000 KiB |    456x | 133.153 us | 92.99% |  23.719 us | 191.03% |   2.763G |  22.104 GB/s |  8.63% |
|   I64 |         I32 |   2^20 = 1048576 |   8.000 MiB |    528x | 155.835 us | 77.45% |  56.287 us |  21.08% |  18.629G | 149.032 GB/s | 58.21% |
|   I64 |         I32 |  2^24 = 16777216 | 128.000 MiB |    606x | 845.568 us | 39.04% | 711.151 us |  28.06% |  23.592G | 188.733 GB/s | 73.71% |
|   I64 |         I32 | 2^28 = 268435456 |   2.000 GiB |   1206x |  10.998 ms | 27.33% |  10.829 ms |  27.51% |  24.790G | 198.317 GB/s | 77.46% |
|   I64 |         I64 |     2^16 = 65536 | 512.000 KiB |    656x | 126.804 us | 92.23% |  26.545 us | 220.61% |   2.469G |  19.751 GB/s |  7.71% |
|   I64 |         I64 |   2^20 = 1048576 |   8.000 MiB |    628x | 159.354 us | 72.80% |  55.800 us |  11.16% |  18.792G | 150.333 GB/s | 58.72% |
|   I64 |         I64 |  2^24 = 16777216 | 128.000 MiB |    578x | 820.399 us | 39.78% | 711.742 us |  27.43% |  23.572G | 188.577 GB/s | 73.65% |
|   I64 |         I64 | 2^28 = 268435456 |   2.000 GiB |   1246x |  10.998 ms | 27.36% |  10.821 ms |  27.55% |  24.806G | 198.447 GB/s | 77.51% |
|  I128 |         I32 |     2^16 = 65536 |   1.000 MiB |    586x | 130.542 us | 93.50% |  20.457 us |  60.98% |   3.204G |  51.258 GB/s | 20.02% |
|  I128 |         I32 |   2^20 = 1048576 |  16.000 MiB |    794x | 207.094 us | 58.92% | 109.396 us |  27.15% |   9.585G | 153.363 GB/s | 59.90% |
|  I128 |         I32 |  2^24 = 16777216 | 256.000 MiB |    726x |   1.535 ms | 45.31% |   1.406 ms |  41.23% |  11.931G | 190.900 GB/s | 74.56% |
|  I128 |         I32 | 2^28 = 268435456 |   4.000 GiB |    685x |  21.663 ms | 15.49% |  21.474 ms |  15.63% |  12.501G | 200.008 GB/s | 78.12% |
|  I128 |         I64 |     2^16 = 65536 |   1.000 MiB |    762x | 136.191 us | 88.94% |  26.470 us | 142.96% |   2.476G |  39.614 GB/s | 15.47% |
|  I128 |         I64 |   2^20 = 1048576 |  16.000 MiB |    460x | 212.651 us | 55.36% | 109.045 us |  11.62% |   9.616G | 153.856 GB/s | 60.09% |
|  I128 |         I64 |  2^24 = 16777216 | 256.000 MiB |    978x |   1.536 ms | 45.25% |   1.397 ms |  40.74% |  12.006G | 192.094 GB/s | 75.03% |
|  I128 |         I64 | 2^28 = 268435456 |   4.000 GiB |    684x |  21.678 ms | 15.44% |  21.492 ms |  15.61% |  12.490G | 199.844 GB/s | 78.05% |
|   F32 |         I32 |     2^16 = 65536 | 256.000 KiB |    564x | 123.920 us | 87.40% |  23.083 us |  74.81% |   2.839G |  11.357 GB/s |  4.44% |
|   F32 |         I32 |   2^20 = 1048576 |   4.000 MiB |    434x | 129.103 us | 84.86% |  34.028 us |  19.31% |  30.815G | 123.260 GB/s | 48.14% |
|   F32 |         I32 |  2^24 = 16777216 |  64.000 MiB |    524x | 495.393 us | 30.05% | 370.205 us |  10.44% |  45.319G | 181.275 GB/s | 70.80% |
|   F32 |         I32 | 2^28 = 268435456 |   1.000 GiB |   1116x |   5.566 ms | 35.49% |   5.403 ms |  34.63% |  49.678G | 198.713 GB/s | 77.61% |
|   F32 |         I64 |     2^16 = 65536 | 256.000 KiB |    544x | 127.539 us | 89.77% |  22.324 us | 173.22% |   2.936G |  11.743 GB/s |  4.59% |
|   F32 |         I64 |   2^20 = 1048576 |   4.000 MiB |    748x | 152.489 us | 80.94% |  36.969 us |  90.02% |  28.364G | 113.456 GB/s | 44.31% |
|   F32 |         I64 |  2^24 = 16777216 |  64.000 MiB |    678x | 485.870 us | 29.40% | 368.182 us |   6.16% |  45.568G | 182.271 GB/s | 71.19% |
|   F32 |         I64 | 2^28 = 268435456 |   1.000 GiB |   1264x |   5.546 ms | 34.06% |   5.384 ms |  33.26% |  49.862G | 199.449 GB/s | 77.90% |
|   F64 |         I32 |     2^16 = 65536 | 512.000 KiB |    568x | 125.986 us | 95.38% |  23.235 us | 182.82% |   2.821G |  22.565 GB/s |  8.81% |
|   F64 |         I32 |   2^20 = 1048576 |   8.000 MiB |    560x | 147.219 us | 74.03% |  57.097 us |  12.27% |  18.365G | 146.919 GB/s | 57.38% |
|   F64 |         I32 |  2^24 = 16777216 | 128.000 MiB |    756x | 840.654 us | 38.77% | 714.247 us |  27.60% |  23.489G | 187.915 GB/s | 73.40% |
|   F64 |         I32 | 2^28 = 268435456 |   2.000 GiB |   1336x |  10.981 ms | 27.24% |  10.806 ms |  27.33% |  24.841G | 198.732 GB/s | 77.62% |
|   F64 |         I64 |     2^16 = 65536 | 512.000 KiB |    566x | 126.811 us | 93.88% |  22.206 us |  71.94% |   2.951G |  23.611 GB/s |  9.22% |
|   F64 |         I64 |   2^20 = 1048576 |   8.000 MiB |    390x | 147.103 us | 76.47% |  56.778 us |  11.20% |  18.468G | 147.745 GB/s | 57.71% |
|   F64 |         I64 |  2^24 = 16777216 | 128.000 MiB |    614x | 827.286 us | 39.85% | 716.988 us |  28.19% |  23.400G | 187.197 GB/s | 73.11% |
|   F64 |         I64 | 2^28 = 268435456 |   2.000 GiB |   1236x |  11.002 ms | 27.15% |  10.829 ms |  27.32% |  24.789G | 198.310 GB/s | 77.46% |
|   C32 |         I32 |     2^16 = 65536 | 512.000 KiB |    794x | 128.603 us | 89.24% |  21.656 us |  68.46% |   3.026G |  24.210 GB/s |  9.46% |
|   C32 |         I32 |   2^20 = 1048576 |   8.000 MiB |    450x | 170.588 us | 83.52% |  59.449 us |  67.04% |  17.638G | 141.107 GB/s | 55.11% |
|   C32 |         I32 |  2^24 = 16777216 | 128.000 MiB |    668x | 847.753 us | 39.74% | 718.770 us |  28.57% |  23.342G | 186.733 GB/s | 72.93% |
|   C32 |         I32 | 2^28 = 268435456 |   2.000 GiB |   1336x |  10.993 ms | 27.40% |  10.818 ms |  27.54% |  24.814G | 198.513 GB/s | 77.53% |
|   C32 |         I64 |     2^16 = 65536 | 512.000 KiB |    548x | 128.932 us | 96.07% |  23.156 us | 172.81% |   2.830G |  22.642 GB/s |  8.84% |
|   C32 |         I64 |   2^20 = 1048576 |   8.000 MiB |    516x | 170.772 us | 73.40% |  55.089 us |  10.57% |  19.034G | 152.273 GB/s | 59.47% |
|   C32 |         I64 |  2^24 = 16777216 | 128.000 MiB |    540x | 833.947 us | 40.11% | 718.166 us |  29.31% |  23.361G | 186.889 GB/s | 72.99% |
|   C32 |         I64 | 2^28 = 268435456 |   2.000 GiB |   1234x |  10.988 ms | 27.46% |  10.812 ms |  27.58% |  24.827G | 198.618 GB/s | 77.58% |
|   F16 |         I32 |     2^16 = 65536 | 128.000 KiB |    512x | 126.673 us | 90.24% |  20.119 us |  79.47% |   3.257G |   6.515 GB/s |  2.54% |
|   F16 |         I32 |   2^20 = 1048576 |   2.000 MiB |    514x | 128.311 us | 88.42% |  25.435 us | 148.96% |  41.225G |  82.450 GB/s | 32.20% |
|   F16 |         I32 |  2^24 = 16777216 |  32.000 MiB |    450x | 297.652 us | 43.41% | 193.437 us |   6.76% |  86.732G | 173.464 GB/s | 67.75% |
|   F16 |         I32 | 2^28 = 268435456 | 512.000 MiB |   1034x |   2.854 ms | 42.41% |   2.713 ms |  40.51% |  98.929G | 197.858 GB/s | 77.28% |
|   F16 |         I64 |     2^16 = 65536 | 128.000 KiB |    532x | 130.911 us | 86.48% |  20.638 us |  79.81% |   3.176G |   6.351 GB/s |  2.48% |
|   F16 |         I64 |   2^20 = 1048576 |   2.000 MiB |    524x | 133.219 us | 86.78% |  23.939 us |  59.21% |  43.802G |  87.605 GB/s | 34.22% |
|   F16 |         I64 |  2^24 = 16777216 |  32.000 MiB |    666x | 305.902 us | 43.86% | 194.397 us |   5.62% |  86.304G | 172.608 GB/s | 67.42% |
|   F16 |         I64 | 2^28 = 268435456 | 512.000 MiB |    644x |   2.877 ms | 42.96% |   2.722 ms |  41.28% |  98.601G | 197.201 GB/s | 77.02% |
|  BF16 |         I32 |     2^16 = 65536 | 128.000 KiB |    424x | 126.692 us | 95.34% |  21.485 us |  62.11% |   3.050G |   6.101 GB/s |  2.38% |
|  BF16 |         I32 |   2^20 = 1048576 |   2.000 MiB |    516x | 129.171 us | 89.78% |  27.741 us | 191.24% |  37.798G |  75.597 GB/s | 29.53% |
|  BF16 |         I32 |  2^24 = 16777216 |  32.000 MiB |    510x | 303.508 us | 44.71% | 192.519 us |   4.28% |  87.146G | 174.291 GB/s | 68.07% |
|  BF16 |         I32 | 2^28 = 268435456 | 512.000 MiB |    874x |   2.847 ms | 42.88% |   2.709 ms |  40.95% |  99.076G | 198.152 GB/s | 77.39% |
|  BF16 |         I64 |     2^16 = 65536 | 128.000 KiB |    472x | 135.976 us | 88.09% |  20.692 us |  77.91% |   3.167G |   6.334 GB/s |  2.47% |
|  BF16 |         I64 |   2^20 = 1048576 |   2.000 MiB |    480x | 139.056 us | 85.45% |  23.958 us |  48.48% |  43.766G |  87.533 GB/s | 34.19% |
|  BF16 |         I64 |  2^24 = 16777216 |  32.000 MiB |    504x | 299.900 us | 45.13% | 193.476 us |   8.89% |  86.715G | 173.429 GB/s | 67.74% |
|  BF16 |         I64 | 2^28 = 268435456 | 512.000 MiB |    876x |   2.855 ms | 42.72% |   2.716 ms |  40.83% |  98.850G | 197.700 GB/s | 77.22% |
