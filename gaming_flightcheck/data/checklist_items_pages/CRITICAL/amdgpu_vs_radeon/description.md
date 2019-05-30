## Description

At least one of your GPUs is using the old `radeon` kernel driver, even though it supports the more recent `amdgpu` driver. This usually happens with AMD cards using the GCN 1.0 or 2.0 architectures, suxh as the R5/R7/R9 series and some older cards.

Kernel developper chose to default to the oldest driver for stability reasons, however it does not have all the features and performance improvements of `amdgpu`, and in particular it lacks Vulkan support. Vulkan is required by DXVK and thus by SteamPlay/Proton to run DX10 and DX11 games. Without `amdgpu`, those games will fail to launch unless you manually disable DXVK (which will severely impact performance and also compatibility).

## Fix

To force your kernel to use `amdgpu`, you need to set the following kernel parameters :

```
radeon.si_support=0 amdgpu.si_support=1 radeon.cik_support=0 amdgpu.cik_support=1
```

To learn how to set a kernel parameter, see https://wiki.archlinux.org/index.php/kernel_parameters#Configuration.

The method depends on the bootloader used by your distribution. Ubuntu uses GRUB for instance, but Pop!_OS uses systemd-boot.
