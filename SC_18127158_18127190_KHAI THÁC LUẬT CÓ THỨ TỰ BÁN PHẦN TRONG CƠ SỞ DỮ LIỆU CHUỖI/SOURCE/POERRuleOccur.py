class POERRuleOccur:
    episode = None
    intervals = None
    def __init__(self, episode, intervals):
        self.setEpisode(episode)
        self.setIntervals(intervals)
    def getEpisode(self):
        return self.episode
    def setEpisode(self, episode):
        self.episode = episode
    def getIntervals(self):
        return self.intervals
    def setIntervals(self,intervals):
        self.intervals =intervals
    def __repr__(self):
        return "episode" + str(self.episode) + " " + "intervals: " + str(self.intervals)