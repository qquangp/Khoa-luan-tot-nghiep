import os, psutil

class MemoryLogger:
    maxMemory = 0.0
    def getInstance():
        return MemoryLogger.instance
    def getMaxMemory(self):
        return self.maxMemory
    def reset(self):
        self.maxMemory=0
    def checkMemory(self):
        currentMemory = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
        if (currentMemory > self.maxMemory) :
            self.maxMemory = currentMemory
    def __init__(self, maxMemory):
        self.maxMemory = maxMemory


