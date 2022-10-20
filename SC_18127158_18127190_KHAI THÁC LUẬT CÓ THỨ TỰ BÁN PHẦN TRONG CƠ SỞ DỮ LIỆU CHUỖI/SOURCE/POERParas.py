class POERParas:
    # Constructor
    minSupport      = 0
    xSpan           = 0
    ySpan           = 0
    xySpan          = 0
    minConfidence   = 0.0
    selfIncrement   = False
    def __init__(self, minSupport,xSpan, ySpan, minConfidence, xySpan, selfIncrement):
        self.minSupport     =  minSupport
        self.xSpan          =  xSpan
        self.ySpan          =  ySpan
        self.minConfidence  =  minConfidence
        self.xySpan         =  xySpan
        self.selfIncrement  =  selfIncrement
    def isSelfIncrement(self):
        return self.selfIncrement
    def setSelfIncrement(self, selfIncrement):
        self.selfIncrement = selfIncrement
    def getMinSupport(self):
        return self.minSupport
    def setMinSupport(self, minSupport):
        self.minSupport = minSupport
    def  getXSpan(self) :
        return self.xSpan
    def setXSpan(self, xSpan) :
        self.xSpan = xSpan
    def  getYSpan(self) :
        return self.ySpan
    def setYSpan(self, ySpan) :
        self.ySpan = ySpan
    def  getMinConfidence(self) :
        return self.minConfidence
    def setMinConfidence(self, minConfidence) :
        self.minConfidence = minConfidence
    def  getXYSpan(self) :
        return self.xySpan
    def  getWinlen(self) :
        return self.xySpan
    def setXYSpan(self, xySpan) :
        self.xySpan = xySpan

