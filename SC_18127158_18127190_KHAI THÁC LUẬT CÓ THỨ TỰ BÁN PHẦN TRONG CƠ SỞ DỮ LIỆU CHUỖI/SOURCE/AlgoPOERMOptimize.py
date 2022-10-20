import math
from POERParas import POERParas
from MemoryLogger import MemoryLogger
from Interval import Interval
from EventSetAppear import EventSetAppear
from RuleInterval import RuleInterval
from POERRule import POERRule
from POERRuleOccur import POERRuleOccur
import time
class AlgoPOERMOptimize:
    inputFile = None
    # thời gian bắt đầu chương trình chạy
    startTime = 0
    # thời gian kết thúc chương trình chạy
    endTime = 0
    # thời gian chạy của ct
    deltaTime = 0
    def getDeltaTime(self):
        return self.deltaTime
    # thời gian kết thúc của database sequence
    end = 0
    # type: POERParas
    parameter = None
    # một chuỗi loại bỏ tất cả các sự kiện có số lần xuất hiện ít hơn minsup từ tập dữ liệu đầu vào
    # key : int và value [int]
    XFreS = None
    # một chuỗi loại bỏ tất cả các sự kiện có số lần xuất hiện ít hơn minsup * minconf khỏi tập dữ liệu đầu vào
    # key : int và value [int]
    YFreS = None
    # ghi lại item và khoảng thời gian xuất hiện của nó
    # key : int, value : Interval
    thisAppear = None
    # [EventSetAppear] -> xEventSet
    XFreAppear = None
    # [EventSetAppear] -> xEventSet
    YFreAppear = None
    # [POERRule] -> valid poerm rule
    ruleAppear = None
    # Bộ nhớ tối đa được sử dụng trong lần thực thi cuối cùng
    maxMemory = 0.0
    instance = MemoryLogger(0)
    def BubbleSort(self,arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j].end > arr[j+1].end:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                elif arr[j].end == arr[j+1].end:
                    if arr[j].start > arr[j+1].start:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
    def runAlgorithm(self, inputFile, minSupport, xSpan, ySpan, minConfidence, xySpan, selfIncrement):
        self.XFreS = dict()
        self.YFreS = dict()
        self.thisAppear = dict()
        self.XFreAppear = []
        self.YFreAppear = []
        self.ruleAppear = []
        self.inputFile = inputFile
        self.parameter = POERParas(minSupport, xSpan, ySpan, minConfidence, xySpan, selfIncrement)
        self.instance.reset()
        self.startTime = time.time() * 1000
        self.preProcess(self.inputFile)
        self.miningXEventSet()
        self.findRule(self.YFreS, self.parameter.getYSpan(), self.parameter.getXYSpan())
        self.endTime = time.time() * 1000
        self.deltaTime = round(self.endTime - self.startTime,4)
        self.instance.checkMemory()
        self.maxMemory = self.instance.getMaxMemory()
        #print(self.ruleAppear)
    '''
    Đọc dataset. Chuyển item trong dataset tshành các con số và xây dựng 1 map cho nó.
	Ghi lại thời gian xuất hiện của từng item
	Loại bỏ tất cả các sự kiện có số lần xuất hiện bé hơn minsup khỏi tập dữ liệu đầu vào để thu được chuỗi XFres
	và số lần xuất hiện bé hơn minsup * minconf để có được chuỗi YFres
	Lọc ra frequent-1 item trong XFreAppear và YFreAppear.
    '''
    def preProcess(self, input):
        eventSet = dict()
        line = None
        timestamp = 1
        num = None
        preTimestamp = -1
        if (self.parameter.isSelfIncrement() == True) :
            with open(input, "r", encoding="UTF-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line == "" or line[0] == '#' or line[0] == '%' or line[0] == '@' :
                        continue
                    array = line.split(" ")
                    if '\n' in array:
                        array.remove("\n")
                    eSet = []
                    eSet2 = []
                    for event in array:
                        # Chuyển item trong dataset thành các số và xây dựng 1 map cho nó
                        num = int(event)
                        support = eventSet.get(num)
                        if (support != None) :
                            eventSet[num] = support + 1
                            #self.thisAppear[num] = Interval(timestamp, timestamp)
                            self.thisAppear[num].append(Interval(timestamp, timestamp))
                        else:
                            eventSet[num] = 1
                            interval = []
                            interval.append(Interval(timestamp, timestamp))
                            self.thisAppear[num] = interval
                        # sử dụng list lưu data trong timestamp này
                        eSet.append(num)
                        eSet2.append(num)
                    
                    if (len(eSet) > 0):
                        # sử dụng dict lưu dữ liệu trong timestamp này
                        self.XFreS[timestamp] = eSet2
                    timestamp += 1
        else:
            with open(input, "r", encoding="UTF-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line == "" or line[0] == '#' or line[0] == '%' or line[0] == '@' :
                        continue
                    lineSplited = line.split("|")
                    timestamp = int(lineSplited[1])
                    array = lineSplited[0].split(" ")
                    eSet = []
                    eSet2 = []
                    for event in array:
                        num = int(event)
                        support = eventSet.get(num)
                        if (support != None) :
                            eventSet[num] = support + 1
                            self.thisAppear[num].append(Interval(timestamp, timestamp))
                        else:
                            eventSet[num] = 1
                            interval = []
                            interval.append(Interval(timestamp, timestamp))
                            self.thisAppear[num] = interval
                        eSet.append(num)
                        eSet2.append(num)
                    
                    if (len(eSet) > 0):
                        self.XFreS[timestamp] = eSet2
        self.instance.checkMemory()
        self.loadFrequent(eventSet)
    '''
    loại bỏ tất cả events có số lần xuất hiện nhỏ hơn minsup từ dữ liệu đầu vào để đạt được chuỗi XFres
	và số lần xuất hiện nhỏ hơn minsup*minconf để đạt được chuỗi YFres
	lọc ra frequent-1 item trong XFreAppear và YFreAppear
    '''
    def loadFrequent(self, eventSet):
        for key,eSet in self.XFreS.items():
            XnewList = []
            YnewList = []
            for e in eSet:
                support = eventSet.get(e)
                if (support >= self.parameter.getMinSupport()*self.parameter.getMinConfidence()):
                    YnewList.append(e)
                    if (support >= self.parameter.getMinSupport()):
                        XnewList.append(e)
            self.XFreS[key] = XnewList
            self.YFreS[key] = YnewList
        for key, val in eventSet.items():
            numKey =[]
            numKey.append(key)
            if (float(val) >= float(self.parameter.getMinSupport()) * self.parameter.getMinConfidence()):
                value = self.thisAppear.get(key)
                self.YFreAppear.append(EventSetAppear(numKey,value))
                if (val >= self.parameter.getMinSupport()):
                    self.XFreAppear.append(EventSetAppear(numKey,value))
        self.instance.checkMemory()
    # Tìm tất cả XEventSet mà có thể là anti episode của POER
    def miningXEventSet(self):
        index = 0
        end = len(self.XFreAppear)
        while index < end:
            self.thisAppear.clear()
            episodeAppear = self.XFreAppear[index]
            index += 1
            # Frequent-i item
            episode = episodeAppear.getEventSet()
            compareKey = episode[len(episode) - 1]
            appear = episodeAppear.getIntervals()
            for interval in appear :
                intStart = interval.start
                intEnd = interval.end
                '''
                for a frequent-i itemset and its time intervals[interval.start,interval.end)
				Search the time intervals [interval.end - XSpan + 1, interval.start)
				to add each event set F ∪ {e} such that e > frequent-i itemset's lastItem
				and its occurrences in the map fresMap
                '''
                for j in range (intEnd - self.parameter.getXSpan() + 1,intStart):
                    if j not in self.XFreS.keys():
                        continue
                    eventSet = self.XFreS.get(j)
                    for eventItem in eventSet:
                        '''
                        add each event set F U {e}
						such that e > frequent-i itemset's lastItem
						and its occurrences in the map fresMap
                        '''
                        if eventItem > compareKey:
                            if eventItem in self.thisAppear.keys():
                                self.thisAppear[eventItem].append(Interval(j,intEnd))
                            else :
                                appearTime = []
                                appearTime.append(Interval(j,intEnd))
                                self.thisAppear[eventItem]= appearTime
                
                # Search the time intervals [interval.end + 1, interval.start + XSpan)
                #j = intEnd + 1
                for j in range(intEnd+1,intStart + self.parameter.getXSpan()):
                    if j not in self.XFreS.keys():
                        continue
                    eventSet = self.XFreS.get(j)
                    for eventItem in eventSet:
                        if eventItem > compareKey:
                            if eventItem in self.thisAppear.keys():
                                self.thisAppear[eventItem].append(Interval(intStart,j))
                            else :
                                appearTime = []
                                appearTime.append(Interval(intStart,j))
                                self.thisAppear[eventItem]= appearTime
                # Search the time intervals [intStart, intEnd]
                #j = intStart
                for j in range(intStart, intEnd+1):
                    if j not in self.XFreS.keys():
                        continue
                    eventSet = self.XFreS.get(j)
                    for eventItem in eventSet:
                        if eventItem > compareKey:
                            if eventItem in self.thisAppear.keys():
                                self.thisAppear[eventItem].append(Interval(intStart,intEnd))
                            else :
                                appearTime = []
                                appearTime.append(Interval(intStart,intEnd))
                                self.thisAppear[eventItem]= appearTime
            # Add each pair of fresMap such that |value|≥minsup into XFreAppear
            for key, value in self.thisAppear.items():
                value = sorted(sorted(value, key = lambda x : x.start), key = lambda x : x.end)
                #self.BubbleSort(value)
                newValue = []
                for i in range (0,len(value)):
                    if i == 0 or value[i].equal(newValue[len(newValue)-1])== False:
                        newValue.append(value[i])
                #newValue = [value[i] for i in range(0,len(value)) if i==0 or value[i].equal(newValue[len(newValue)-1])== False]
                if (len(newValue) >= self.parameter.getMinSupport()):
                    newKey = list(episode)
                    newKey.append(key)
                    self.XFreAppear.append(EventSetAppear(newKey,newValue))
            end = len(self.XFreAppear)
            self.instance.checkMemory()
    # Tìm kiếm các event set (consequents) mà có thể được kết hợp với những antecedents để tạo ra POERs hợp lệ
    def findRule(self, itemFres, window_size, span):
        conseRecodeMap = dict()
        for anitemset in self.XFreAppear:
            # cho một tập anit và các khoảng thời gian xuất hiện của nó
            anitKey = anitemset.getEventSet()
            anitValues = anitemset.getIntervals()
            anitStart = -1
            anitCount = 0
            # nếu thời gián xuất hiện của anit episode < MinSupport, skip nó
            for anitValue in anitValues:
                if anitValue.start <= anitStart:
                    continue
                anitCount += 1
                anitStart = anitValue.end
            if anitCount < self.parameter.getMinSupport():
                continue
            conseRecodeMap.clear()
            # Scan each timestamp of YFres in anit episode OccurrenceList to
            # obtain a map conseMap that records each event e and its occurrence list
            for anitValue in anitValues:
                for i in range (1+ anitValue.end, span + anitValue.end + window_size):
                    if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                        continue
                    thisInterval = RuleInterval(anitValue.start, anitValue.end, i, i)
                    itemSet = itemFres.get(i)
                    for item in itemSet:
                        if item in conseRecodeMap.keys():
                            conseRecodeMap[item].append(thisInterval)
                        else:
                            intervalList = []
                            intervalList.append(thisInterval)
                            conseRecodeMap[item] = intervalList
            '''
            Scan conseRecodeMap and put the pair (x−→e, OccurrenceList) in a queuecandidateRuleQueue
			note: infrequent rules are kept because event e may be extended to obtain some frequent rules
            '''
            for key, occurList in conseRecodeMap.items():
                ruleOccur = []
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
                conseEpi = []
                conseEpi.append(key)
                if realRuleCount >= anitCount * self.parameter.getMinConfidence() and anitKey!=conseEpi:
                    self.ruleAppear.append(POERRule(anitKey, conseEpi, None, anitCount, realRuleCount))
                tempRuleMap = dict()
                # extend a rule with i-item to rules with i+1-item
                for occur in occurList :
                    intervalStart = max(occur.antiEnd + 1, occur.end - self.parameter.getYSpan() + 1)
                    # search [intervalStart, occur.start) to extend the rule
                    for i in range(intervalStart, occur.start):
                        if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                            continue
                        eventSet = itemFres.get(i)
                        ruleInterval = RuleInterval(occur.antiStart, occur.antiEnd, i, occur.end)
                        for eventItem in eventSet:
                            if eventItem > key :
                                if eventItem in tempRuleMap.keys():
                                    tempRuleMap[eventItem].append(ruleInterval)
                                else :
                                    appearTime = []
                                    appearTime.append(ruleInterval)
                                    tempRuleMap[eventItem] = appearTime
                    # search [occur.start, occur.end] to extend the rule
                    for i in range(occur.start, occur.end + 1):
                        if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                            continue
                        eventSet = itemFres.get(i)
                        ruleInterval = RuleInterval(occur.antiStart, occur.antiEnd, occur.start, occur.end)
                        for eventItem in eventSet:
                            if eventItem > key :
                                if eventItem in tempRuleMap.keys():
                                    tempRuleMap[eventItem].append(ruleInterval)
                                else :
                                    appearTime = []
                                    appearTime.append(ruleInterval)
                                    tempRuleMap[eventItem] = appearTime
                    intervalEnd = min(occur.antiEnd + span + window_size, occur.start + window_size)
                    # search [occur.end + 1, intervalEnd) to extend the rule
                    for i in range(occur.end + 1, intervalEnd):
                        if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                            continue
                        eventSet = itemFres.get(i)
                        ruleInterval = RuleInterval(occur.antiStart, occur.antiEnd,occur.start, i)
                        for eventItem in eventSet:
                            if eventItem > key :
                                if eventItem in tempRuleMap.keys():
                                    tempRuleMap[eventItem].append(ruleInterval)
                                else :
                                    appearTime = []
                                    appearTime.append(ruleInterval)
                                    tempRuleMap[eventItem] = appearTime
                # scan tempRuleMap and put vaild rule in ruleAppear, and possible rule in ruleOccur
                for tempRuleMapKey, tempRuleMapInterval in tempRuleMap.items():
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
                    if tempRealRuleCount >= anitCount * self.parameter.getMinConfidence() and anitKey!=conseEpisode:
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
                    oneOccurRuleInters = oneOccurRule.getIntervals()
                    for oneOccurRuleInter in oneOccurRuleInters :
                        intervalStart = max ( oneOccurRuleInter.antiEnd + 1, oneOccurRuleInter.end - self.parameter.getYSpan() + 1)
                        for i in range (intervalStart, oneOccurRuleInter.start):
                            if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                                continue
                            eventSet = itemFres.get(i)
                            ruleInterval = RuleInterval(oneOccurRuleInter.antiStart, oneOccurRuleInter.antiEnd, i, oneOccurRuleInter.end)
                            for eventItem in eventSet :
                                if eventItem > compareKey:
                                    if eventItem in tempRuleMap.keys():
                                        tempRuleMap.get(eventItem).append(ruleInterval)
                                    else :
                                        appearTime = []
                                        appearTime.append(ruleInterval)
                                        tempRuleMap[eventItem] = appearTime
                        # search [oneOccurRuleInter.start, oneOccurRuleInter.end] to extend the rule
                        for i in range (oneOccurRuleInter.start,oneOccurRuleInter.end +1 ):
                            if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                                continue
                            eventSet = itemFres.get(i)
                            ruleInterval = RuleInterval(oneOccurRuleInter.antiStart, oneOccurRuleInter.antiEnd, oneOccurRuleInter.start, oneOccurRuleInter.end)
                            for eventItem in eventSet :
                                if eventItem > compareKey:
                                    if eventItem in tempRuleMap.keys():
                                        tempRuleMap.get(eventItem).append(ruleInterval)
                                    else :
                                        appearTime = []
                                        appearTime.append(ruleInterval)
                                        tempRuleMap[eventItem] = appearTime
                        # search [oneOccurRuleInter.end + 1, intervalEnd) to extend the rule
                        intervalEnd = min (oneOccurRuleInter.antiEnd + span + window_size, oneOccurRuleInter.start + window_size)
                        for i in range( oneOccurRuleInter.end +1, intervalEnd):
                            if i not in itemFres.keys() or len(itemFres.get(i)) == 0:
                                continue
                            eventSet = itemFres.get(i)
                            ruleInterval = RuleInterval(oneOccurRuleInter.antiStart, oneOccurRuleInter.antiEnd,oneOccurRuleInter.start, i)
                            for eventItem in eventSet :
                                if eventItem > compareKey:
                                    if eventItem in tempRuleMap.keys():
                                        tempRuleMap.get(eventItem).append(ruleInterval)
                                    else :
                                        appearTime = []
                                        appearTime.append(ruleInterval)
                                        tempRuleMap[eventItem] = appearTime
                    # scan tempRuleMap and put vaild rule in ruleAppear, and possible rule in ruleOccur
                    for tempRuleMapKey, tempRuleMapInterval in tempRuleMap.items():
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
                        conseEpisode.append(episode)
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

