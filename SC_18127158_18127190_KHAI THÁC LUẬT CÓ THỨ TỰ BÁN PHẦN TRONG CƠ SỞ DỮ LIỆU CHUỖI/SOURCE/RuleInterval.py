class RuleInterval:
    antiStart = 0
    antiEnd = 0
    start = 0
    end = 0
    def __init__(self, antiStart, antiEnd, start, end):
        self.antiStart = antiStart
        self.antiEnd = antiEnd
        self.start = start
        self.end = end
    def equal(self, other):
        if ( self.antiStart == other.antiStart and self.antiEnd == other.antiEnd and self.start == other.start and self.end == other.end):
            return True
        return False
    def __repr__(self):
        return str(self.antiStart) + " " + str(self.antiEnd) + " " + str(self.start) + " " + str(self.end)
        
