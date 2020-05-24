import sys
import subprocess
import os
import time
import logger as  l

from watchdog.observers import Observer

logger = l.Logger()

config = {
    "trigger":[],
    "trigger_type":"process",
    "mode":1,
    "path":"./",
    "prescript":[

    ],
    "postscript":[

    ]
}

FILES_ERROR = r"Supply Files To Watch ¯\_༼ ಥ ‿ ಥ ༽_/¯ "

class HandleAll(object):
    process = None
    def __init__(self,proc):
        self.proc = proc

    def _runscripts(self,scripts):
        logger.log("Running Scripts",l.MESSAGE)
        for i in scripts:
            os.system(i)

    def setProcess(self,process):
        self.process = process

    def dispatch(self, event):
        logger.log(f"event type : {event.event_type}",l.MESSAGE)
        logger.log(f"file : {event.src_path}",l.MESSAGE)
        logger.log("reloading",l.WARNING)
      
        
class HandleAny(object):
    process = None
    def __init__(self,proc,files):
        self.proc = proc
        self.files = files
        

    def _runscripts(self,scripts):
        logger.log("Running Scripts",l.MESSAGE)
        for i in scripts:
            os.system(i)        

    def setProcess(self,process):
        self.process = process

    def dispatch(self, event):
        logger.log(f"event type : {event.event_type}",l.MESSAGE)
        logger.log(f"file : {event.src_path}",l.MESSAGE)
        if sum(map(lambda x:x in event.src_path,self.files)):
            logger.log("reloading",l.WARNING)
        else:
            logger.log("not reloading",l.WARNING)


class BUILD(object):
    def __init__(
                self,
                trigger,
                prescript,
                postscript
            ):

        self.trigger = trigger
        self.prescript = prescript
        self.postscript = postscript

    def __repr__(self):
        return self.trigger.__str__()

class PROCESS(object):
    def __init__(
                self,
                trigger,
                prescript,
                **kwargs
            ):

        self.prescript = prescript
        self.trigger = trigger

    def start(self,):
        self.proc = subprocess.Popen(self.trigger)

    def __repr__(self):
        return self.trigger.__str__()

    def stop(self,):
        self.proc.kill()

class Watcher:
    """
    mode : 0 - Any | 1 - All
    """
    def __init__(
                self,
                proc=PROCESS,
                trigger=None,
                files=None,
                mode=0,
                path='.',
                prescript=[],
                postscript=[],
            ):

        
        self.proc = proc(trigger,prescript = prescript,postscript = postscript)

        if mode:
            self.event_handler = HandleAll(self.proc)
        else:
            assert files, FILES_ERROR
            self.event_handler = HandleAny(self.proc,files)

        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=True)

    def runscripts(self,scripts):
        logger.log("Running Scripts",l.MESSAGE)
        for i in scripts:
            os.system(i)

    def start(self,):
        logger.log(f"Started Watching {self.proc}",l.MESSAGE)
        self.proc.start()    


    def observe(self,):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.log("Killing Process, Exiting Loop",l.ERROR)
            self.proc.stop()
            self.observer.stop()
        self.observer.join()

