# Command Line

```
/home/lktr/src/cccl/build/cub-benchmark/bin/cub.bench.reduce.sum.base -d 0 --stopping-criterion entropy --quiet --json '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-04-cub-reduce-sum-official-full-run1-turbo-sm89.json' --md '/mnt/d/Projects/Open-Source Contribution/evidence/raw/phase2/2026-09-04-cub-reduce-sum-official-full-run1-turbo-sm89.md'
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
Pass: Cold: 0.025138ms GPU, 0.136727ms CPU, 0.02s total GPU, 0.29s total wall, 834x 
Run:  [2/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^20]
Warn: GPU throttled below threshold (1617.52 MHz / 2250.00 MHz) (72% < 75%) on sample 251. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.024239ms GPU, 0.133312ms CPU, 0.01s total GPU, 0.19s total wall, 404x 
Run:  [3/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.102927ms GPU, 0.201347ms CPU, 0.04s total GPU, 0.15s total wall, 410x 
Run:  [4/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 1.386510ms GPU, 1.515497ms CPU, 0.85s total GPU, 1.03s total wall, 614x 
Run:  [5/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.021832ms GPU, 0.140619ms CPU, 0.01s total GPU, 0.20s total wall, 596x 
Run:  [6/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.020121ms GPU, 0.135500ms CPU, 0.01s total GPU, 0.22s total wall, 688x 
Run:  [7/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.103698ms GPU, 0.197426ms CPU, 0.06s total GPU, 0.20s total wall, 550x 
Run:  [8/80] base [Device=0 T{ct}=I8 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 1.385613ms GPU, 1.519870ms CPU, 0.80s total GPU, 0.97s total wall, 576x 
Run:  [9/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.019505ms GPU, 0.139935ms CPU, 0.02s total GPU, 0.42s total wall, 1262x 
Run:  [10/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.023300ms GPU, 0.124083ms CPU, 0.01s total GPU, 0.15s total wall, 504x 
Run:  [11/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.193815ms GPU, 0.291164ms CPU, 0.10s total GPU, 0.23s total wall, 514x 
Run:  [12/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 2.723222ms GPU, 2.854756ms CPU, 2.26s total GPU, 2.51s total wall, 830x 
Run:  [13/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.020882ms GPU, 0.138207ms CPU, 0.01s total GPU, 0.21s total wall, 624x 
Run:  [14/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.024849ms GPU, 0.142716ms CPU, 0.01s total GPU, 0.13s total wall, 406x 
Run:  [15/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.192626ms GPU, 0.322920ms CPU, 0.07s total GPU, 0.17s total wall, 342x 
Run:  [16/80] base [Device=0 T{ct}=I16 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 2.716818ms GPU, 2.865285ms CPU, 2.86s total GPU, 3.21s total wall, 1052x 
Run:  [17/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.023238ms GPU, 0.128559ms CPU, 0.02s total GPU, 0.22s total wall, 698x 
Run:  [18/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.036990ms GPU, 0.129832ms CPU, 0.03s total GPU, 0.21s total wall, 686x 
Run:  [19/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.367943ms GPU, 0.480396ms CPU, 0.23s total GPU, 0.40s total wall, 628x 
Run:  [20/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 5.375240ms GPU, 5.533582ms CPU, 6.05s total GPU, 6.46s total wall, 1126x 
Run:  [21/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.023228ms GPU, 0.131632ms CPU, 0.02s total GPU, 0.26s total wall, 830x 
Run:  [22/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.036383ms GPU, 0.141394ms CPU, 0.01s total GPU, 0.11s total wall, 328x 
Run:  [23/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.371024ms GPU, 0.494561ms CPU, 0.25s total GPU, 0.45s total wall, 682x 
Run:  [24/80] base [Device=0 T{ct}=I32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 5.401218ms GPU, 5.556763ms CPU, 6.52s total GPU, 6.95s total wall, 1208x 
Run:  [25/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^16]
Warn: GPU throttled below threshold (1457.32 MHz / 2250.00 MHz) (65% < 75%) on sample 114. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.026042ms GPU, 0.133339ms CPU, 0.02s total GPU, 0.35s total wall, 926x 
Run:  [26/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.060613ms GPU, 0.166868ms CPU, 0.04s total GPU, 0.25s total wall, 714x 
Run:  [27/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.720440ms GPU, 0.842319ms CPU, 0.51s total GPU, 0.71s total wall, 704x 
Run:  [28/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I32 Elements{io}=2^28]
Warn: GPU throttled below threshold (0.00 MHz / 2250.00 MHz) (0% < 75%) on sample 1003. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 10.807500ms GPU, 10.973655ms CPU, 14.42s total GPU, 15.01s total wall, 1334x 
Run:  [29/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.020677ms GPU, 0.126121ms CPU, 0.02s total GPU, 0.26s total wall, 830x 
Run:  [30/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.057092ms GPU, 0.165699ms CPU, 0.03s total GPU, 0.17s total wall, 492x 
Run:  [31/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.720404ms GPU, 0.846357ms CPU, 0.55s total GPU, 0.77s total wall, 758x 
Run:  [32/80] base [Device=0 T{ct}=I64 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 10.825720ms GPU, 10.998226ms CPU, 14.46s total GPU, 15.00s total wall, 1336x 
Run:  [33/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.022823ms GPU, 0.129783ms CPU, 0.02s total GPU, 0.22s total wall, 688x 
Run:  [34/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.107603ms GPU, 0.205720ms CPU, 0.05s total GPU, 0.17s total wall, 450x 
Run:  [35/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 1.401076ms GPU, 1.528835ms CPU, 1.02s total GPU, 1.23s total wall, 730x 
Run:  [36/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 21.486127ms GPU, 21.672970ms CPU, 14.70s total GPU, 15.00s total wall, 684x 
Run:  [37/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.022187ms GPU, 0.130294ms CPU, 0.01s total GPU, 0.12s total wall, 386x 
Run:  [38/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.107986ms GPU, 0.211987ms CPU, 0.06s total GPU, 0.23s total wall, 586x 
Run:  [39/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 1.408782ms GPU, 1.552431ms CPU, 1.96s total GPU, 2.39s total wall, 1390x 
Run:  [40/80] base [Device=0 T{ct}=I128 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 21.493788ms GPU, 21.677135ms CPU, 14.70s total GPU, 15.00s total wall, 684x 
Run:  [41/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^16]
Warn: GPU throttled below threshold (1672.72 MHz / 2250.00 MHz) (74% < 75%) on sample 574. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.023020ms GPU, 0.126023ms CPU, 0.02s total GPU, 0.31s total wall, 844x 
Run:  [42/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.034297ms GPU, 0.128759ms CPU, 0.02s total GPU, 0.15s total wall, 486x 
Run:  [43/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.368671ms GPU, 0.483058ms CPU, 0.16s total GPU, 0.27s total wall, 428x 
Run:  [44/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 5.378252ms GPU, 5.547491ms CPU, 5.67s total GPU, 6.06s total wall, 1054x 
Run:  [45/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.024668ms GPU, 0.129865ms CPU, 0.02s total GPU, 0.29s total wall, 904x 
Run:  [46/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.036056ms GPU, 0.129440ms CPU, 0.02s total GPU, 0.15s total wall, 500x 
Run:  [47/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.370425ms GPU, 0.491344ms CPU, 0.22s total GPU, 0.39s total wall, 606x 
Run:  [48/80] base [Device=0 T{ct}=F32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 5.412481ms GPU, 5.567829ms CPU, 5.74s total GPU, 6.12s total wall, 1060x 
Run:  [49/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.021149ms GPU, 0.139125ms CPU, 0.01s total GPU, 0.21s total wall, 616x 
Run:  [50/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.056530ms GPU, 0.151678ms CPU, 0.02s total GPU, 0.13s total wall, 384x 
Run:  [51/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.720728ms GPU, 0.838836ms CPU, 0.59s total GPU, 0.82s total wall, 822x 
Run:  [52/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 10.817931ms GPU, 10.984610ms CPU, 14.24s total GPU, 14.77s total wall, 1316x 
Run:  [53/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.019857ms GPU, 0.131270ms CPU, 0.02s total GPU, 0.25s total wall, 770x 
Run:  [54/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.057445ms GPU, 0.148403ms CPU, 0.04s total GPU, 0.22s total wall, 670x 
Run:  [55/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.713929ms GPU, 0.848463ms CPU, 0.64s total GPU, 0.91s total wall, 898x 
Run:  [56/80] base [Device=0 T{ct}=F64 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 10.839361ms GPU, 11.016811ms CPU, 12.81s total GPU, 13.31s total wall, 1182x 
Run:  [57/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.022778ms GPU, 0.126542ms CPU, 0.02s total GPU, 0.27s total wall, 864x 
Run:  [58/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.058713ms GPU, 0.156555ms CPU, 0.04s total GPU, 0.25s total wall, 756x 
Run:  [59/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.711887ms GPU, 0.827960ms CPU, 0.43s total GPU, 0.59s total wall, 604x 
Run:  [60/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 10.822727ms GPU, 10.989552ms CPU, 14.46s total GPU, 14.99s total wall, 1336x 
Run:  [61/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.019067ms GPU, 0.124805ms CPU, 0.01s total GPU, 0.13s total wall, 428x 
Run:  [62/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.056834ms GPU, 0.158093ms CPU, 0.04s total GPU, 0.21s total wall, 624x 
Run:  [63/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.712715ms GPU, 0.832071ms CPU, 0.51s total GPU, 0.72s total wall, 718x 
Run:  [64/80] base [Device=0 T{ct}=C32 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 10.813571ms GPU, 10.983418ms CPU, 14.46s total GPU, 15.00s total wall, 1337x 
Run:  [65/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.024669ms GPU, 0.131089ms CPU, 0.02s total GPU, 0.27s total wall, 838x 
Run:  [66/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.026298ms GPU, 0.136095ms CPU, 0.01s total GPU, 0.12s total wall, 378x 
Run:  [67/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.193768ms GPU, 0.299028ms CPU, 0.13s total GPU, 0.32s total wall, 686x 
Run:  [68/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 2.732786ms GPU, 2.865135ms CPU, 1.97s total GPU, 2.20s total wall, 722x 
Run:  [69/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^16]
Warn: GPU throttled below threshold (1405.10 MHz / 2250.00 MHz) (62% < 75%) on sample 430. Discarding previous trial and pausing for 0.050s.
Pass: Cold: 0.024313ms GPU, 0.128438ms CPU, 0.02s total GPU, 0.25s total wall, 638x 
Run:  [70/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.027398ms GPU, 0.129179ms CPU, 0.02s total GPU, 0.20s total wall, 634x 
Run:  [71/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.198057ms GPU, 0.329339ms CPU, 0.10s total GPU, 0.25s total wall, 506x 
Run:  [72/80] base [Device=0 T{ct}=F16 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 2.727855ms GPU, 2.901026ms CPU, 1.93s total GPU, 2.20s total wall, 708x 
Run:  [73/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^16]
Pass: Cold: 0.020918ms GPU, 0.136011ms CPU, 0.01s total GPU, 0.22s total wall, 676x 
Run:  [74/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^20]
Pass: Cold: 0.024091ms GPU, 0.149067ms CPU, 0.02s total GPU, 0.29s total wall, 852x 
Run:  [75/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^24]
Pass: Cold: 0.195498ms GPU, 0.296112ms CPU, 0.16s total GPU, 0.38s total wall, 822x 
Run:  [76/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I32 Elements{io}=2^28]
Pass: Cold: 2.708513ms GPU, 2.854552ms CPU, 2.47s total GPU, 2.77s total wall, 912x 
Run:  [77/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^16]
Pass: Cold: 0.018875ms GPU, 0.148968ms CPU, 0.02s total GPU, 0.32s total wall, 902x 
Run:  [78/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^20]
Pass: Cold: 0.026213ms GPU, 0.128758ms CPU, 0.01s total GPU, 0.18s total wall, 562x 
Run:  [79/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^24]
Pass: Cold: 0.193173ms GPU, 0.296538ms CPU, 0.07s total GPU, 0.16s total wall, 342x 
Run:  [80/80] base [Device=0 T{ct}=BF16 OffsetT{ct}=I64 Elements{io}=2^28]
Pass: Cold: 2.733410ms GPU, 2.885391ms CPU, 3.27s total GPU, 3.68s total wall, 1198x 
```

# Benchmark Results

## base

### [0] NVIDIA GeForce RTX 4060 Laptop GPU

| T{ct} | OffsetT{ct} |   Elements{io}   |    Size     | Samples |  CPU Time  |  Noise  |  GPU Time  |  Noise  |  Elem/s  | GlobalMem BW | BWUtil |
|-------|-------------|------------------|-------------|---------|------------|---------|------------|---------|----------|--------------|--------|
|    I8 |         I32 |     2^16 = 65536 |  64.000 KiB |    834x | 136.727 us |  96.34% |  25.138 us | 151.87% |   2.607G |   2.607 GB/s |  1.02% |
|    I8 |         I32 |   2^20 = 1048576 |   1.000 MiB |    404x | 133.312 us | 101.87% |  24.239 us | 176.09% |  43.259G |  43.259 GB/s | 16.90% |
|    I8 |         I32 |  2^24 = 16777216 |  16.000 MiB |    410x | 201.347 us |  62.44% | 102.927 us |  11.08% | 163.001G | 163.001 GB/s | 63.66% |
|    I8 |         I32 | 2^28 = 268435456 | 256.000 MiB |    614x |   1.515 ms |  45.89% |   1.387 ms |  41.03% | 193.605G | 193.605 GB/s | 75.62% |
|    I8 |         I64 |     2^16 = 65536 |  64.000 KiB |    596x | 140.619 us |  92.82% |  21.832 us |  91.93% |   3.002G |   3.002 GB/s |  1.17% |
|    I8 |         I64 |   2^20 = 1048576 |   1.000 MiB |    688x | 135.500 us |  88.99% |  20.121 us |  88.11% |  52.115G |  52.115 GB/s | 20.35% |
|    I8 |         I64 |  2^24 = 16777216 |  16.000 MiB |    550x | 197.426 us |  62.01% | 103.698 us |  37.86% | 161.790G | 161.790 GB/s | 63.19% |
|    I8 |         I64 | 2^28 = 268435456 | 256.000 MiB |    576x |   1.520 ms |  46.13% |   1.386 ms |  41.89% | 193.730G | 193.730 GB/s | 75.67% |
|   I16 |         I32 |     2^16 = 65536 | 128.000 KiB |   1262x | 139.935 us |  83.59% |  19.505 us | 182.92% |   3.360G |   6.720 GB/s |  2.62% |
|   I16 |         I32 |   2^20 = 1048576 |   2.000 MiB |    504x | 124.083 us |  84.12% |  23.300 us |  62.12% |  45.004G |  90.008 GB/s | 35.16% |
|   I16 |         I32 |  2^24 = 16777216 |  32.000 MiB |    514x | 291.164 us |  43.22% | 193.815 us |   4.92% |  86.563G | 173.126 GB/s | 67.62% |
|   I16 |         I32 | 2^28 = 268435456 | 512.000 MiB |    830x |   2.855 ms |  42.36% |   2.723 ms |  40.81% |  98.573G | 197.145 GB/s | 77.00% |
|   I16 |         I64 |     2^16 = 65536 | 128.000 KiB |    624x | 138.207 us |  88.67% |  20.882 us |  83.30% |   3.138G |   6.277 GB/s |  2.45% |
|   I16 |         I64 |   2^20 = 1048576 |   2.000 MiB |    406x | 142.716 us |  85.40% |  24.849 us | 169.94% |  42.199G |  84.397 GB/s | 32.96% |
|   I16 |         I64 |  2^24 = 16777216 |  32.000 MiB |    342x | 322.920 us |  41.67% | 192.626 us |   8.93% |  87.097G | 174.195 GB/s | 68.04% |
|   I16 |         I64 | 2^28 = 268435456 | 512.000 MiB |   1052x |   2.865 ms |  43.29% |   2.717 ms |  41.94% |  98.805G | 197.610 GB/s | 77.18% |
|   I32 |         I32 |     2^16 = 65536 | 256.000 KiB |    698x | 128.559 us |  88.21% |  23.238 us |  64.06% |   2.820G |  11.281 GB/s |  4.41% |
|   I32 |         I32 |   2^20 = 1048576 |   4.000 MiB |    686x | 129.832 us |  96.88% |  36.990 us | 123.03% |  28.348G | 113.391 GB/s | 44.29% |
|   I32 |         I32 |  2^24 = 16777216 |  64.000 MiB |    628x | 480.396 us |  29.46% | 367.943 us |   6.14% |  45.597G | 182.389 GB/s | 71.24% |
|   I32 |         I32 | 2^28 = 268435456 |   1.000 GiB |   1126x |   5.534 ms |  34.83% |   5.375 ms |  34.17% |  49.939G | 199.757 GB/s | 78.02% |
|   I32 |         I64 |     2^16 = 65536 | 256.000 KiB |    830x | 131.632 us |  83.99% |  23.228 us |  94.02% |   2.821G |  11.286 GB/s |  4.41% |
|   I32 |         I64 |   2^20 = 1048576 |   4.000 MiB |    328x | 141.394 us |  83.61% |  36.383 us | 126.72% |  28.821G | 115.283 GB/s | 45.03% |
|   I32 |         I64 |  2^24 = 16777216 |  64.000 MiB |    682x | 494.561 us |  31.65% | 371.024 us |  15.96% |  45.219G | 180.875 GB/s | 70.65% |
|   I32 |         I64 | 2^28 = 268435456 |   1.000 GiB |   1208x |   5.557 ms |  37.19% |   5.401 ms |  36.63% |  49.699G | 198.796 GB/s | 77.65% |
|   I64 |         I32 |     2^16 = 65536 | 512.000 KiB |    926x | 133.339 us |  90.99% |  26.042 us | 187.10% |   2.517G |  20.133 GB/s |  7.86% |
|   I64 |         I32 |   2^20 = 1048576 |   8.000 MiB |    714x | 166.868 us |  67.39% |  60.613 us |  22.64% |  17.299G | 138.396 GB/s | 54.05% |
|   I64 |         I32 |  2^24 = 16777216 | 128.000 MiB |    704x | 842.319 us |  38.12% | 720.440 us |  28.54% |  23.287G | 186.300 GB/s | 72.76% |
|   I64 |         I32 | 2^28 = 268435456 |   2.000 GiB |   1334x |  10.974 ms |  27.25% |  10.808 ms |  27.42% |  24.838G | 198.703 GB/s | 77.61% |
|   I64 |         I64 |     2^16 = 65536 | 512.000 KiB |    830x | 126.121 us |  87.59% |  20.677 us |  68.83% |   3.170G |  25.357 GB/s |  9.90% |
|   I64 |         I64 |   2^20 = 1048576 |   8.000 MiB |    492x | 165.699 us |  74.62% |  57.092 us |  66.70% |  18.367G | 146.932 GB/s | 57.39% |
|   I64 |         I64 |  2^24 = 16777216 | 128.000 MiB |    758x | 846.357 us |  38.68% | 720.404 us |  29.75% |  23.289G | 186.309 GB/s | 72.77% |
|   I64 |         I64 | 2^28 = 268435456 |   2.000 GiB |   1336x |  10.998 ms |  27.48% |  10.826 ms |  27.72% |  24.796G | 198.369 GB/s | 77.48% |
|  I128 |         I32 |     2^16 = 65536 |   1.000 MiB |    688x | 129.783 us |  89.05% |  22.823 us |  79.76% |   2.871G |  45.945 GB/s | 17.94% |
|  I128 |         I32 |   2^20 = 1048576 |  16.000 MiB |    450x | 205.720 us |  56.77% | 107.603 us |   9.48% |   9.745G | 155.918 GB/s | 60.90% |
|  I128 |         I32 |  2^24 = 16777216 | 256.000 MiB |    730x |   1.529 ms |  45.89% |   1.401 ms |  41.47% |  11.975G | 191.592 GB/s | 74.83% |
|  I128 |         I32 | 2^28 = 268435456 |   4.000 GiB |    684x |  21.673 ms |  15.50% |  21.486 ms |  15.62% |  12.493G | 199.895 GB/s | 78.07% |
|  I128 |         I64 |     2^16 = 65536 |   1.000 MiB |    386x | 130.294 us |  90.01% |  22.187 us | 200.29% |   2.954G |  47.261 GB/s | 18.46% |
|  I128 |         I64 |   2^20 = 1048576 |  16.000 MiB |    586x | 211.987 us |  58.90% | 107.986 us |  11.63% |   9.710G | 155.365 GB/s | 60.68% |
|  I128 |         I64 |  2^24 = 16777216 | 256.000 MiB |   1390x |   1.552 ms |  44.85% |   1.409 ms |  41.00% |  11.909G | 190.544 GB/s | 74.42% |
|  I128 |         I64 | 2^28 = 268435456 |   4.000 GiB |    684x |  21.677 ms |  15.59% |  21.494 ms |  15.70% |  12.489G | 199.824 GB/s | 78.05% |
|   F32 |         I32 |     2^16 = 65536 | 256.000 KiB |    844x | 126.023 us |  88.63% |  23.020 us |  92.03% |   2.847G |  11.388 GB/s |  4.45% |
|   F32 |         I32 |   2^20 = 1048576 |   4.000 MiB |    486x | 128.759 us |  93.45% |  34.297 us |  23.53% |  30.573G | 122.292 GB/s | 47.76% |
|   F32 |         I32 |  2^24 = 16777216 |  64.000 MiB |    428x | 483.058 us |  29.77% | 368.671 us |   5.33% |  45.507G | 182.029 GB/s | 71.10% |
|   F32 |         I32 | 2^28 = 268435456 |   1.000 GiB |   1054x |   5.547 ms |  34.90% |   5.378 ms |  34.11% |  49.911G | 199.645 GB/s | 77.98% |
|   F32 |         I64 |     2^16 = 65536 | 256.000 KiB |    904x | 129.865 us |  89.38% |  24.668 us | 207.76% |   2.657G |  10.627 GB/s |  4.15% |
|   F32 |         I64 |   2^20 = 1048576 |   4.000 MiB |    500x | 129.440 us |  92.06% |  36.056 us | 102.63% |  29.082G | 116.328 GB/s | 45.43% |
|   F32 |         I64 |  2^24 = 16777216 |  64.000 MiB |    606x | 491.344 us |  31.13% | 370.425 us |  11.76% |  45.292G | 181.167 GB/s | 70.76% |
|   F32 |         I64 | 2^28 = 268435456 |   1.000 GiB |   1060x |   5.568 ms |  35.36% |   5.412 ms |  34.74% |  49.596G | 198.383 GB/s | 77.48% |
|   F64 |         I32 |     2^16 = 65536 | 512.000 KiB |    616x | 139.125 us |  85.30% |  21.149 us | 164.93% |   3.099G |  24.791 GB/s |  9.68% |
|   F64 |         I32 |   2^20 = 1048576 |   8.000 MiB |    384x | 151.678 us |  75.66% |  56.530 us |  24.21% |  18.549G | 148.393 GB/s | 57.96% |
|   F64 |         I32 |  2^24 = 16777216 | 128.000 MiB |    822x | 838.836 us |  39.75% | 720.728 us |  28.62% |  23.278G | 186.225 GB/s | 72.74% |
|   F64 |         I32 | 2^28 = 268435456 |   2.000 GiB |   1316x |  10.985 ms |  27.19% |  10.818 ms |  27.34% |  24.814G | 198.511 GB/s | 77.53% |
|   F64 |         I64 |     2^16 = 65536 | 512.000 KiB |    770x | 131.270 us |  89.52% |  19.857 us |  95.23% |   3.300G |  26.403 GB/s | 10.31% |
|   F64 |         I64 |   2^20 = 1048576 |   8.000 MiB |    670x | 148.403 us |  78.12% |  57.445 us |  21.11% |  18.254G | 146.030 GB/s | 57.04% |
|   F64 |         I64 |  2^24 = 16777216 | 128.000 MiB |    898x | 848.463 us |  39.23% | 713.929 us |  27.09% |  23.500G | 187.999 GB/s | 73.43% |
|   F64 |         I64 | 2^28 = 268435456 |   2.000 GiB |   1182x |  11.017 ms |  27.27% |  10.839 ms |  27.42% |  24.765G | 198.119 GB/s | 77.38% |
|   C32 |         I32 |     2^16 = 65536 | 512.000 KiB |    864x | 126.542 us |  91.57% |  22.778 us | 140.86% |   2.877G |  23.018 GB/s |  8.99% |
|   C32 |         I32 |   2^20 = 1048576 |   8.000 MiB |    756x | 156.555 us |  81.24% |  58.713 us |  54.05% |  17.859G | 142.874 GB/s | 55.80% |
|   C32 |         I32 |  2^24 = 16777216 | 128.000 MiB |    604x | 827.960 us |  39.80% | 711.887 us |  27.37% |  23.567G | 188.538 GB/s | 73.64% |
|   C32 |         I32 | 2^28 = 268435456 |   2.000 GiB |   1336x |  10.990 ms |  27.60% |  10.823 ms |  27.74% |  24.803G | 198.424 GB/s | 77.50% |
|   C32 |         I64 |     2^16 = 65536 | 512.000 KiB |    428x | 124.805 us |  92.46% |  19.067 us |  58.58% |   3.437G |  27.498 GB/s | 10.74% |
|   C32 |         I64 |   2^20 = 1048576 |   8.000 MiB |    624x | 158.093 us |  73.46% |  56.834 us |  27.69% |  18.450G | 147.599 GB/s | 57.65% |
|   C32 |         I64 |  2^24 = 16777216 | 128.000 MiB |    718x | 832.071 us |  39.14% | 712.715 us |  27.97% |  23.540G | 188.319 GB/s | 73.55% |
|   C32 |         I64 | 2^28 = 268435456 |   2.000 GiB |   1337x |  10.983 ms |  27.41% |  10.814 ms |  27.61% |  24.824G | 198.592 GB/s | 77.57% |
|   F16 |         I32 |     2^16 = 65536 | 128.000 KiB |    838x | 131.089 us |  91.05% |  24.669 us | 101.52% |   2.657G |   5.313 GB/s |  2.08% |
|   F16 |         I32 |   2^20 = 1048576 |   2.000 MiB |    378x | 136.095 us |  85.50% |  26.298 us | 166.17% |  39.872G |  79.745 GB/s | 31.15% |
|   F16 |         I32 |  2^24 = 16777216 |  32.000 MiB |    686x | 299.028 us |  45.39% | 193.768 us |   5.59% |  86.584G | 173.168 GB/s | 67.64% |
|   F16 |         I32 | 2^28 = 268435456 | 512.000 MiB |    722x |   2.865 ms |  42.77% |   2.733 ms |  41.07% |  98.228G | 196.455 GB/s | 76.73% |
|   F16 |         I64 |     2^16 = 65536 | 128.000 KiB |    638x | 128.438 us |  82.25% |  24.313 us | 198.40% |   2.696G |   5.391 GB/s |  2.11% |
|   F16 |         I64 |   2^20 = 1048576 |   2.000 MiB |    634x | 129.179 us |  88.08% |  27.398 us | 131.18% |  38.271G |  76.543 GB/s | 29.90% |
|   F16 |         I64 |  2^24 = 16777216 |  32.000 MiB |    506x | 329.339 us |  41.15% | 198.057 us |   8.16% |  84.709G | 169.418 GB/s | 66.17% |
|   F16 |         I64 | 2^28 = 268435456 | 512.000 MiB |    708x |   2.901 ms |  43.08% |   2.728 ms |  41.51% |  98.405G | 196.811 GB/s | 76.87% |
|  BF16 |         I32 |     2^16 = 65536 | 128.000 KiB |    676x | 136.011 us |  83.30% |  20.918 us |  79.00% |   3.133G |   6.266 GB/s |  2.45% |
|  BF16 |         I32 |   2^20 = 1048576 |   2.000 MiB |    852x | 149.067 us |  83.32% |  24.091 us |  52.45% |  43.525G |  87.051 GB/s | 34.00% |
|  BF16 |         I32 |  2^24 = 16777216 |  32.000 MiB |    822x | 296.112 us |  46.09% | 195.498 us |  20.85% |  85.818G | 171.636 GB/s | 67.04% |
|  BF16 |         I32 | 2^28 = 268435456 | 512.000 MiB |    912x |   2.855 ms |  42.41% |   2.709 ms |  40.65% |  99.108G | 198.216 GB/s | 77.42% |
|  BF16 |         I64 |     2^16 = 65536 | 128.000 KiB |    902x | 148.968 us |  83.68% |  18.875 us | 173.85% |   3.472G |   6.944 GB/s |  2.71% |
|  BF16 |         I64 |   2^20 = 1048576 |   2.000 MiB |    562x | 128.758 us |  92.85% |  26.213 us | 138.08% |  40.002G |  80.004 GB/s | 31.25% |
|  BF16 |         I64 |  2^24 = 16777216 |  32.000 MiB |    342x | 296.538 us |  43.48% | 193.173 us |   4.93% |  86.851G | 173.702 GB/s | 67.84% |
|  BF16 |         I64 | 2^28 = 268435456 | 512.000 MiB |   1198x |   2.885 ms |  42.72% |   2.733 ms |  41.14% |  98.205G | 196.411 GB/s | 76.71% |
