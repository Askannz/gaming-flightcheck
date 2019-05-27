## Description

Your current desktop session is running on an Nvidia GPU which uses the open-source driver `nouveau`. This driver is not recommended for gaming, since it performs much worse than the official proprietary driver `nvidia` and has no Vulkan support.

If you are already aware of that situation and want your GPU to use the open-source driver, or if you know your GPU is too old to be still supported by the proprietary driver, you can safely ignore this message.

## Fix

Install the proprietary driver provided by Nvidia. **DO NOT** download and install the driver straight from the Nvidia website : the script they provide is intended for distribution maintainers and will cause issues if installed manually. Instead, use packages provided by your distribution repositories, or trusted third-party repositories (such as the [Proprietary GPU Drivers PPA](https://launchpad.net/~graphics-drivers/+archive/ubuntu/ppa) for Ubuntu).
