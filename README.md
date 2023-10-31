# Wiki
Code Wiki

## Example file "ffmpeg/chopTime.txt"

```
# ffmpeg
# chop time
	
ffmpeg -ss 00:00:00.0 -i INPUT.mkv -c copy -t 00:13:17.0 OUTPUT.mk
	
## ss start
## t duration
```

1. line: program or language
2. line: description	
3. -end line: code and explanation (must start with "##")

## Feature
If a line startes with "#c", the following command is copied onto the clipboard and stays there till after you exited the program. In the terminal you can paste the command via the assigned paste shortcut.

## Requirements
``` python
import time,os,copy
import textwrap
import subprocess
import pyperclip
```
