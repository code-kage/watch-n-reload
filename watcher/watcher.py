import subprocess
import os
import time

from logger import Logger
from watchdog.observers import Observer

logger = Logger()
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
        logger.message("Running Scripts")
        for i in scripts:
            os.system(i)

    def setProcess(self,process):
        self.process = process

    def dispatch(self, event):
        logger.message(f"event type : {event.event_type}")
        logger.message(f"file : {event.src_path}")
        logger.warning("reloading",)
        self.proc.stop()
        self.proc.start()
        
class HandleAny(object):
    process = None
    def __init__(self,proc,files):
        self.proc = proc
        self.files = files
        
    def _runscripts(self,scripts):
        logger.message("Running Scripts")
        for i in scripts:
            os.system(i)        

    def setProcess(self,process):
        self.process = process

    def dispatch(self, event):
        logger.message(f"event type : {event.event_type}",)
        logger.message(f"file : {event.src_path}")
        if sum(map(lambda x:x in event.src_path,self.files)):
            logger.warning("reloading")
            self.proc.stop()
            self.proc.start()
        else:
            logger.warning("not reloading")
        

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
        logger.message("Running Scripts")
        for i in scripts:
            os.system(i)

    def start(self,):
        logger.message(f"Started Watching {self.proc}")
        self.proc.start()    


    def observe(self,):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.error("Killing Process, Exiting Loop")
            self.proc.stop()
            self.observer.stop()
        self.observer.join()

