#!/usr/bin/env python3

import watcher

config = {
    "proc":watcher.PROCESS,
    "trigger":["py","test.py"],
    "mode":0,
    "path":"./",
    "files":[
        ".build"
    ],
    "postscript":[
        "rm -rf dist",
        "rm -rf build",
        "rm -rf watcher_codekage.egg-info"
    ]
}

watch = watcher.Watcher(**config)
watch.start()
watch.observe()
