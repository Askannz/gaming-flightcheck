## Description

Your CPU is not using the "performance" governor even though it is available. This may cause CPU-bound games to run worse than they could, particularly with AMD processors.

## Fix

The recommended way to change your frequency governor is to install the tool `cpupower` (normally available in your distribution repository), then run 

```
sudo cpupower frequency-set -g performance
```

Alternatively, the following command achieves the same result without `cpupower` :

```
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```
