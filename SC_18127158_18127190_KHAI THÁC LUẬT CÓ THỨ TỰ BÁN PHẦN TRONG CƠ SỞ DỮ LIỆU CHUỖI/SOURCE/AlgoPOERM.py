import math
from POERParas import POERParas
from MemoryLogger import MemoryLogger
from Interval import Interval
from EventSetAppear import EventSetAppear
from RuleInterval import RuleInterval
from POERRule import POERRule
from POERRuleOccur import POERRuleOccur
import numpy as np
import time
class AlgoPOERM:
    inputFile = None
    startTime = 0
    endTime = 0
    deltaTime = 0
    def getDeltaTime(self):
        return self.deltaTime
    end = 0
    parameter = None
    XFreS = dict()
    YFreS = dict()
    thisAppear = dict()
    XFreAppear = list()
    YFreAppear = list()
    ruleAppear = list()
    maxMemory = 0.0
    instance = MemoryLogger(0)
    def runAlgorithm(self, inputFile, minSupport, xSpan, ySpan, minConfidence, xySpan, selfIncrement):
        '''
        self.XFreS = {}
        self.YFreS = {}
        self.thisAppear = {}
        self.XFreAppear = []
        self.YFreAppear = []
        self.ruleAppear = []
        '''
        self.inputFile = inputFile
        self.parameter = POERParas(minSupport, xSpan, ySpan, minConfidence, xySpan, selfIncrement)
        self.instance.reset()
        self.startTime = time.time() * 1000
        self.preProcess(self.inputFile)
        self.miningXEventSet()
        self.findRule(self.YFreS, self.parameter.getYSpan(), self.parameter.getXYSpan())
        self.endTime = time.time() * 1000
        self.deltaTime = self.endTime - self.startTime
        self.instance.checkMemory()
        self.maxMemory = self.instance.getMaxMemory()
    def preProcess(self, input):
        eventSet = dict()
        timestamp = 1
        if (self.parameter.isSelfIncrement() == True):
            with open(input, "r", encoding="UTF-8") as file:
                lst = file.readlines()
                lines = np.asarray(lst)
                for line in lines:
                    if line == "" or line[0] == '#' or line[0] == '%' or line[0] == '@' :
                        continue
                    Array = line.split(" ")
                    if '\n' in Array:
                        Array.remove("\n")
                    array = np.asarray(Array)
                    eSet = []
                    eSet2 = []
                    for event in array:
                        num = int(event)
                        support = eventSet.get(num)
                        if support != None:
                            eventSet[num] = support +1
                            self.thisAppear[num].append(Interval(timestamp,timestamp))
                        else:
                            eventSet[num] = 1
                            self.thisAppear[num] = [Interval(timestamp,timestamp)]
                        #self.thisAppear[num] = np.asarray(self.thisAppear[num])
                        eSet.append(num)
                        eSet2.append(num)
                    if len(eSet) > 0:
                        self.XFreS[timestamp]= eSet2
                    timestamp += 1
        else:
            with open(input, "r", encoding="UTF-8") as file:
                lst = file.readlines()
                lines = np.asarray(lst)
                for line in lines:
                    if line == "" or line[0] == '#' or line[0]== '%' or line[0] == '@':
                        continue
                    lineSplited = line.split("|")
                    timestamp = int(lineSplited[1])
                    array = np.asarray(lineSplited[0].split(" "))
                    eSet = []
                    eSet2 = []
                    for event in array:
                        num = int(event)
                        support = eventSet.get(num)
                        if support != None:
                            eventSet[num] = support + 1
                            self.thisAppear[num].append(Interval(timestamp,timestamp))
                        else:
                            eventSet[num] = 1
                            self.thisAppear[num] = [Interval(timestamp,timestamp)]
                        #self.thisAppear[num] = np.asarray(self.thisAppear[num])
                        eSet.append(num)
                        eSet2.append(num)
                    if len(eSet) > 0 :
                        self.XFreS[timestamp] = eSet2
        self.instance.checkMemory()
        self.loadFrequent(eventSet)
    def loadFrequent(self, eventSet):
        for key, entry in self.XFreS.items():
            eSet = np.asarray(entry)
            XnewList = []
            YnewList = []
            for e in eSet:
                support = eventSet.get(e)
                if support >= self.parameter.getMinSupport()*self.parameter.getMinConfidence():
                    YnewList.append(e)
                    if support >= self.parameter.getMinSupport():
                        XnewList.append(e)
            self.XFreS[key] = np.asarray(XnewList)
            self.YFreS[key] = np.asarray(YnewList)
        for key, val in eventSet.items():
            numKey = np.asarray([key])
            if float(val) >= float(self.parameter.getMinSupport() * self.parameter.getMinConfidence()):
                value = np.asarray(self.thisAppear.get(key))
                self.YFreAppear.append(EventSetAppear(numKey,value))
                if val >= self.parameter.getMinSupport():
                    self.XFreAppear.append(EventSetAppear(numKey, value))
        self.instance.checkMemory()
    def miningXEventSet(self):
        index = 0
        end = len(self.XFreAppear)
        while index < end:
            self.thisAppear.clear()
            episodeAppear = self.XFreAppear[index]
            index += 1
            episode = np.asarray(episodeAppear.getEventSet())
            compareKey = episode[len(episode) - 1]
            appear = np.asarray(episodeAppear.getIntervals())
            for interval in appear:
                intStart = interval.start
                intEnd = interval.end
                for j in range(intEnd - self.parameter.getXSpan() + 1,intStart):
                    if j not in self.XFreS.keys():
                        continue
                    eventSet = np.asarray(self.XFreS.get(j))
                    for eventItem in eventSet:
                        if eventItem > compareKey:
                            if eventItem in self.thisAppear.keys():
                                self.thisAppear[eventItem].append(Interval(j,intEnd))
                            else:
                                self.thisAppear[eventItem] = [Interval(j,intEnd)]
                for j in range(intEnd+1,intStart + self.parameter.getXSpan()):
                    if j not in self.XFreS.keys():
                        continue
                    eventSet = np.asarray(self.XFreS.get(j))
                    for eventItem in eventSet:
                        if eventItem > compareKey:
                            if eventItem in self.thisAppear.keys():
                                self.thisAppear[eventItem].append(Interval(intStart,j))
                            else :
                                self.thisAppear[eventItem]= [Interval(intStart,j)]
                for j in range(intStart, intEnd+1):
                    if j not in self.XFreS.keys():
                        continue
                    eventSet = np.asarray(self.XFreS.get(j))
                    for eventItem in eventSet:
                        if eventItem > compareKey:
                            if eventItem in self.thisAppear.keys():
                                self.thisAppear[eventItem].append(Interval(intStart,intEnd))
                            else :
                                self.thisAppear[eventItem]= [Interval(intStart,intEnd)]
            for key, Value in self.thisAppear.items():
                Value.sort(key=lambda x: (x.end, x.start))
                value = np.asarray(Value)
                #newValue = [value[i] for i in range(len(value)) if i==0 or value[i].equal(newValue[len(newValue)-1])== False]
                newValue = []
                for i in range (len(value)):
                    if i == 0 or value[i].equal(newValue[len(newValue)-1])== False:
                        newValue.append(value[i])
                #NewValue = np.asarray(newValue)
                if len(newValue) >= self.parameter.getMinSupport():
                    newKey = list(episode)
                    newKey.append(key)
                    #NewKey = np.asarray(newKey)
                    self.XFreAppear.append(EventSetAppear(newKey,np.asarray(newValue)))  
            end = len(self.XFreAppear)
            self.instance.checkMemory()
    def findRule(self,itemFres, window_size, span):
        conseRecodeMap = dict()
        for anitemset in self.XFreAppear:
            anitKey = anitemset.getEventSet()
            anitValues = np.asarray(anitemset.getIntervals())
            anitStart = -1
            anitCount = 0
            for anitValue in anitValues:
                if anitValue.start <= anitStart:
                    continue
                anitCount += 1
                anitStart = anitValue.end
            if anitCount < self.parameter.getMinSupport():
                continue
            conseRecodeMap.clear()
            for anitValue in anitValues:
                for i in range (1+ anitValue.end, span + anitValue.end + window_size):
                    if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                        continue
                    thisInterval = RuleInterval(anitValue.start, anitValue.end, i, i)
                    itemSet = np.asarray(itemFres.get(i))
                    for item in itemSet:
                        if item in conseRecodeMap.keys():
                            conseRecodeMap[item].append(thisInterval)
                        else:
                            conseRecodeMap[item] = [thisInterval]
            for key, OccurList in conseRecodeMap.items():
                ruleOccur = []
                occurList = np.asarray(OccurList)
                if len(occurList) < anitCount * self.parameter.getMinConfidence():
                    continue
                possibleRuleStart = -1
                possibleRuleCount = 0
                realRuleStart = -1
                realRuleCount = 0
                for occur in occurList:
                    if occur.antiStart > realRuleStart and occur.start - occur.antiEnd <= span:
                        realRuleCount += 1
                        realRuleStart = occur.end
                    if occur.antiStart > possibleRuleStart:
                        possibleRuleCount += 1
                        possibleRuleStart = occur.end
                if possibleRuleCount < anitCount * self.parameter.getMinConfidence():
                    continue
                conseEpi = [key]
                if realRuleCount >= anitCount * self.parameter.getMinConfidence() and anitKey!=conseEpi:
                    self.ruleAppear.append(POERRule(anitKey, conseEpi, None, anitCount, realRuleCount))
                tempRuleMap = dict()
                for occur in occurList:
                    intervalStart = max(occur.antiEnd + 1, occur.end - self.parameter.getYSpan() + 1)
                    for i in range(intervalStart, occur.start):
                        if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                            continue
                        eventSet = np.asarray(itemFres.get(i))
                        ruleInterval = RuleInterval(occur.antiStart, occur.antiEnd, i, occur.end)
                        for eventItem in eventSet:
                            if eventItem > key :
                                if eventItem in tempRuleMap.keys():
                                    tempRuleMap[eventItem].append(ruleInterval)
                                else :
                                    tempRuleMap[eventItem] = [ruleInterval]
                    for i in range(occur.start, occur.end + 1):
                        if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                            continue
                        eventSet = np.asarray(itemFres.get(i))
                        ruleInterval = RuleInterval(occur.antiStart, occur.antiEnd, occur.start, occur.end)
                        for eventItem in eventSet:
                            if eventItem > key :
                                if eventItem in tempRuleMap.keys():
                                    tempRuleMap[eventItem].append(ruleInterval)
                                else :
                                    tempRuleMap[eventItem] = [ruleInterval]
                    intervalEnd = min(occur.antiEnd + span + window_size, occur.start + window_size)
                    for i in range(occur.end + 1, intervalEnd):
                        if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                            continue
                        eventSet = np.asarray(itemFres.get(i))
                        ruleInterval = RuleInterval(occur.antiStart, occur.antiEnd,occur.start, i)
                        for eventItem in eventSet:
                            if eventItem > key :
                                if eventItem in tempRuleMap.keys():
                                    tempRuleMap[eventItem].append(ruleInterval)
                                else :
                                    tempRuleMap[eventItem] = [ruleInterval]
                for tempRuleMapKey, TempRuleMapInterval in tempRuleMap.items():
                    tempRuleMapInterval = np.asarray(TempRuleMapInterval)
                    if len(tempRuleMapInterval) < anitCount* self.parameter.getMinConfidence():
                        continue
                    tempPossibleRuleStart = -1
                    tempPossibleRuleCount = 0
                    tempRealRuleStart = -1
                    tempRealRuleCount = 0
                    for tempRuleMapInter in tempRuleMapInterval:
                        if tempRuleMapInter.antiStart > tempRealRuleStart and tempRuleMapInter.start - tempRuleMapInter.antiEnd <= span:
                            tempRealRuleCount += 1
                            tempRealRuleStart = tempRuleMapInter.end
                        if tempRuleMapInter.antiStart > tempPossibleRuleStart:
                            tempPossibleRuleCount += 1
                            tempPossibleRuleStart = tempRuleMapInter.end
                    if tempPossibleRuleCount < anitCount* self.parameter.getMinConfidence():
                        continue
                    conseEpisode = []
                    conseEpisode.append(key)
                    conseEpisode.append(tempRuleMapKey)
                    check = False
                    if len(anitKey) != len(conseEpisode):
                        check = True
                        if tempRealRuleCount >= anitCount * self.parameter.getMinConfidence()and check:
                            self.ruleAppear.append(POERRule(anitKey, conseEpisode, None, anitCount, tempRealRuleCount))
                    else:
                        if tempRealRuleCount >= anitCount * self.parameter.getMinConfidence()and (anitKey!=conseEpisode):
                            self.ruleAppear.append(POERRule(anitKey, conseEpisode, None, anitCount, tempRealRuleCount))
                    ruleOccur.append(POERRuleOccur(conseEpisode, tempRuleMapInterval))
                    self.instance.checkMemory()
                breadthSearthStart = 0
                breadthSearthEnd = len(ruleOccur)
                # extend a rule with i-item to rules with i+1-item
                while breadthSearthStart < breadthSearthEnd:
                    tempRuleMap.clear()
                    oneOccurRule = ruleOccur[breadthSearthStart]
                    breadthSearthStart += 1
                    episode = oneOccurRule.getEpisode()
                    compareKey = episode[len(episode) -1]
                    oneOccurRuleInters = np.asarray(oneOccurRule.getIntervals())
                    for oneOccurRuleInter in oneOccurRuleInters :
                        intervalStart = max ( oneOccurRuleInter.antiEnd + 1, oneOccurRuleInter.end - self.parameter.getYSpan() + 1)
                        for i in range (intervalStart, oneOccurRuleInter.start):
                            if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                                continue
                            eventSet = np.asarray(itemFres.get(i))
                            ruleInterval = RuleInterval(oneOccurRuleInter.antiStart, oneOccurRuleInter.antiEnd, i, oneOccurRuleInter.end)
                            for eventItem in eventSet :
                                if eventItem > compareKey:
                                    if eventItem in tempRuleMap.keys():
                                        tempRuleMap.get(eventItem).append(ruleInterval)
                                    else :
                                        tempRuleMap[eventItem] = [ruleInterval]
                        # search [oneOccurRuleInter.start, oneOccurRuleInter.end] to extend the rule
                        for i in range (oneOccurRuleInter.start,oneOccurRuleInter.end +1 ):
                            if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                                continue
                            eventSet = np.asarray(itemFres.get(i))
                            ruleInterval = RuleInterval(oneOccurRuleInter.antiStart, oneOccurRuleInter.antiEnd, oneOccurRuleInter.start, oneOccurRuleInter.end)
                            for eventItem in eventSet :
                                if eventItem > compareKey:
                                    if eventItem in tempRuleMap.keys():
                                        tempRuleMap.get(eventItem).append(ruleInterval)
                                    else :
                                        tempRuleMap[eventItem] = [ruleInterval]
                        # search [oneOccurRuleInter.end + 1, intervalEnd) to extend the rule
                        intervalEnd = min (oneOccurRuleInter.antiEnd + span + window_size, oneOccurRuleInter.start + window_size)
                        for i in range( oneOccurRuleInter.end +1, intervalEnd):
                            if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                                continue
                            eventSet = np.asarray(itemFres.get(i))
                            ruleInterval = RuleInterval(oneOccurRuleInter.antiStart, oneOccurRuleInter.antiEnd,oneOccurRuleInter.start, i)
                            for eventItem in eventSet :
                                if eventItem > compareKey:
                                    if eventItem in tempRuleMap.keys():
                                        tempRuleMap.get(eventItem).append(ruleInterval)
                                    else :
                                        tempRuleMap[eventItem] = [ruleInterval]
                    for tempRuleMapKey, TempRuleMapInterval in tempRuleMap.items():
                        tempRuleMapInterval = np.asarray(TempRuleMapInterval)
                        if len(tempRuleMapInterval) < anitCount * self.parameter.getMinConfidence():
                            continue
                        tempPossibleRuleStart = -1
                        tempPossibleRuleCount = 0
                        tempRealRuleStart = -1
                        tempRealRuleCount = 0
                        for tempRuleMapInter in tempRuleMapInterval:
                            if tempRuleMapInter.antiStart > tempRealRuleStart and tempRuleMapInter.start - tempRuleMapInter.antiEnd <= span:
                                tempRealRuleCount += 1
                                tempRealRuleStart = tempRuleMapInter.end
                            if tempRuleMapInter.antiStart > tempPossibleRuleStart:
                                tempPossibleRuleCount += 1
                                tempPossibleRuleStart = tempRuleMapInter.end
                        if tempPossibleRuleCount < anitCount * self.parameter.getMinConfidence():
                            continue
                        conseEpisode = []
                        #check lai cho nay
                        conseEpisode.extend(episode)
                        conseEpisode.append(tempRuleMapKey)
                        if tempRealRuleCount >= anitCount * self.parameter.getMinConfidence() and anitKey!=(conseEpisode):
                            self.ruleAppear.append(POERRule(anitKey, conseEpisode, None, anitCount, tempRealRuleCount))
                        ruleOccur.append(POERRuleOccur(conseEpisode, tempRuleMapInterval))
                    self.instance.checkMemory()
                    breadthSearthEnd = len(ruleOccur)
    def printRule(self):
        for poerrule in self.ruleAppear:
            episodeRule = ""
            antiEpisode = poerrule.getAntiEpisode()
            conseEpisode = poerrule.getConseEpisode()
            for anti in antiEpisode:
                episodeRule += str(anti) + " "
            episodeRule += "==> "
            for conse in conseEpisode:
                episodeRule += str(conse) + " "
            print("rule: " + episodeRule + "#SUP:" + str(poerrule.getAntiCount()) + " #CONF: " + str(poerrule.getRuleCount() / float(poerrule.getAntiCount())))
    def writeRuletoFile(self, filename):
        self.instance.checkMemory()
        with open(filename, "w") as file:
            for poerrule in self.ruleAppear:
                buffer =""
                for anti in poerrule.getAntiEpisode():
                    buffer += str(anti)
                    buffer += " "
                buffer += "==> "
                for conse in poerrule.getConseEpisode():
                    buffer += str(conse)
                    buffer += " "
                buffer += "#SUP: "
                buffer += str(poerrule.getAntiCount())
                buffer += " #CONF: "
                buffer += str(poerrule.getRuleCount() / float(poerrule.getAntiCount()))
                buffer += "\n"
                file.write(str(buffer))
    def printStats(self):
        print(" Rule count : " + str(len(self.ruleAppear)))
        print(" Maximum memory usage : " + str(self.maxMemory) + " mb")
        print(" Total time ~ : " + str(self.deltaTime) + " ms")
        print("===================================================")