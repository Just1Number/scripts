#/bin/bash
import -window root /tmp/lock.png
convert /tmp/lock.png  -spread 2 -blur 1 /tmp/lock.png
i3lock -i /tmp/lock.png
