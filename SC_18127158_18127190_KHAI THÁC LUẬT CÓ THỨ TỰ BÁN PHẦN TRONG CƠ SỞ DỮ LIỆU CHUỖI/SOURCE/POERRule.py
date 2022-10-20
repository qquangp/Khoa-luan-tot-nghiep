class POERRule:
    antiEpisode = None
    conseEpisode = None
    intervals = None
    antiCount = 0
    confidence = 0
    def __init__(self, antiEpisode, conseEpisode, intervals, antiCount, confident):
        self.setAntiEpisode(antiEpisode)
        self.setConseEpisode(conseEpisode)
        self.setIntervals(intervals)
        self.setAntiCount(antiCount)
        self.setConfident(confident)
    def match(self, antecedent):
        intersection = []
        intersection.extend(self.antiEpisode)
        otherList = []
        nowItemSet = []
        for j in range(len(antecedent)):
            nowItemSet.append(antecedent[j])
            for k in range(len(nowItemSet)):
                otherList.append(nowItemSet[k])
        #improve
        intersection = [ i for i in intersection if i in otherList]
        if (len(intersection) == len(self.antiEpisode)):
            return len(self.antiEpisode)
        else:
            return 0
    def __repr__(self):
        episodeRule = ""
        antiEpisode = self.getAntiEpisode()
        conseEpisode = self.getConseEpisode()
        for anti in antiEpisode:
            episodeRule += str(anti) + " "
        episodeRule += "==> "
        for conse in conseEpisode:
            episodeRule += str(conse) + " "
        return "rule: " + episodeRule + "#SUP: " + str(self.getRuleCount()) + "#CONF: " + str(round((self.getRuleCount()/self.getAntiCount()),4))
    def compareTo (self,o):
        compare = self.antiCount - o.antiCount
        if (compare > 0):
            return 1
        elif (compare < 0):
            return -1
        else:
            return 0
    def  getAntiEpisode(self) :
        return self.antiEpisode
    def setAntiEpisode(self, antiEpisode) :
        self.antiEpisode = antiEpisode
    def  getConseEpisode(self) :
        return self.conseEpisode
    def setConseEpisode(self, conseEpisode) :
        self.conseEpisode = conseEpisode
    def  getIntervals(self) :
        return self.intervals
    def setIntervals(self, intervals) :
        self.intervals = intervals
    def  getRuleCount(self) :
        return self.confidence
    def setConfident(self, confident) :
        self.confidence = confident
    def  getAntiCount(self) :
        return self.antiCount
    def setAntiCount(self, antiCount) :
        self.antiCount = antiCount



