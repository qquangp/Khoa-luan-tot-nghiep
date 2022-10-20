from Interval import Interval
class EventSetAppear:
    eventSet = None
    intervals = None
    key = 0.0
    def getEventSet(self):
        return self.eventSet
    def setEventSet(self, eventSet):
        self.eventSet = eventSet
    def getIntervals(self):
        return self.intervals
    def setIntervals(self,intervals):
        self.intervals = intervals
    def __repr__(self):
        return "eventSet:" + str(self.eventSet) + " " +"intervals:" + str(self.intervals)
    def __init__(self,episode,intervals,key):
        self.setEventSet(episode)
        self.setIntervals(intervals)
        self.key = key
    def __init__(self,episode,intervals):
        self.setEventSet(episode)
        self.setIntervals(intervals)