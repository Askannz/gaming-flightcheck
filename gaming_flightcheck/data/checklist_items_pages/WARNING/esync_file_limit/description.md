## Description

Your Systemd file limit is too low. This can cause crashes in Proton and Wine if Esync is enabled.

Esync is a patch that improves CPU performance. It is enabled by default in Proton, but can cause crashes if the file limit is not properly set.

You can check the file limit yourself with `ulimit -Hn`. The number needs to be at least 524288 for Esync to work properly.

## Fix

You need to edit both `/etc/systemd/system.conf` and `/etc/systemd/user.conf` (as root) and add `DefaultLimitNOFILE=524288`.

If there is already a `#DefaultLimitNOFILE=` line, simply remove the `#` and append `524288`.

Reboot for the change to take effect.
