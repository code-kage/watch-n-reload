#!/usr/bin/env python3

from watcher import *

config = {
    "proc":PROCESS,
    "trigger":["python3","test.py"],
    "mode":0,
    "path":"./",
    "files":[
        ".build"
    ],
}

watch = Watcher(**config)
watch.start()
watch.observe()