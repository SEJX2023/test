import time

from bokeh.server.tornado import psutil
from numpy import random

class Sender:
    def sendMessage(self,message):
        print(message)

class ActivityRecognizer:

    def __init__(self):
        self.refresh()

    def refresh(self):
        self.pids = psutil.pids()

    def getActibityType(self):
        self.refresh()
        index=random.randint(0,len(self.pids)-1)
        pid=self.pids[index]
        process=psutil.Process(pid)
        return process.name()

class PowerC:
    def __init__(self):
        self.flag="off"

    def getState(self):
        return self.flag

    def on(self):
        self.flag="on"

    def off(self):
        self.flag="off"

class Application:
    def __init__(self):
        self.sender=Sender()
        self.activityRecognizer=ActivityRecognizer()
        self.powerC=PowerC()
        self.powerC.on()

    def run(self):
        while 1:
            time.sleep(0.5)
            message="PC is "+self.powerC.getState()+", application '"+self.activityRecognizer.getActibityType()+"' is running."
            self.sender.sendMessage(message)

a=Application()
a.run()