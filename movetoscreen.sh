#!/bin/sh
eval $(xdotool getactivewindow getwindowgeometry --shell)
DEST=$1
SCREEN=$(($X/1920))
X=$(($X-($SCREEN-$DEST)*1920))
echo $Y
Y=$(($Y-26)) # fix some weird bug
echo $X $Y
xdotool getactivewindow windowmove $X $Y
