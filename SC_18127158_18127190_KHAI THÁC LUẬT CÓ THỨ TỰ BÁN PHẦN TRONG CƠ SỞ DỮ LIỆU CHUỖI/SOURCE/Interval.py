class Interval:
    start   = 0
    end     = 0
    def __init__(self,start,end):
        self.start  = start
        self.end    = end
    def equal(self, other):
        if (self.start == other.start and self.end == other.end):
            return True
        return False
    def __repr__(self):
        return str(self.start) + " " + str(self.end)

def  isInteger(string) :
        result = None
        try :
            result = int(string)
        except :
            return None
        # only got here if we didn't return false
        return result