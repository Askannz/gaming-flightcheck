## Description

Your Systemd file limit is high enough for Esync.

Esync is a patch that improves CPU performance. It is enabled by default in Proton, but can cause crashes if the file limit is not properly set.

You can check the file limit yourself with `ulimit -Hn`. The number needs to be at least 524288 for Esync to work properly.
