class ResultConverter :
    def subconvert(self, mapItemIDtoStringValue,  outputFile,  outputFileConverted) :
        writer = open(outputFileConverted,"w", encoding="UTF-8")
        with open(outputFile, "r", encoding="UTF-8") as myInputResult:
            lines = myInputResult.readlines()
            firstLine = True
            for line in lines:
                noItemsLeft = False
                if line != "":
                    if firstLine:
                        firstLine = False
                    else:
                        writer.write("\n")
                    split = line.split(" ")
                    for i in range(len(split)):
                        token = split[i]
                        if token.startswith("#") or noItemsLeft:
                            noItemsLeft = True
                            writer.write(token.rstrip('\n'))
                        else:
                            itemID = self.isInteger(token)
                            if itemID == None:
                                if token.find(",") >= 0:
                                    parts = token.split(",")
                                    for m in range(len(parts)):
                                        item = int(parts[m])
                                        stringRepresentation = mapItemIDtoStringValue.get(item)
                                        writer.write(stringRepresentation.rstrip('\n'))
                                        if m < len(parts) - 1:
                                            writer.write(",".rstrip('\n'))
                                else:
                                    writer.write(token.rstrip('\n'))
                            else:
                                name = mapItemIDtoStringValue.get(itemID)
                                if name == None:
                                    writer.write(str(itemID).rstrip('\n'))
                                else:
                                    writer.write(mapItemIDtoStringValue.get(itemID).rstrip('\n'))
                        if i != len(split) - 1:
                            writer.write(" ")
        writer.close()
    def convert(self, inputDB,  outputFile,  outputFileConverted):
        mapItemIDtoStringValue =  dict()
        with open(inputDB, "r", encoding="UTF-8") as myInputDB:
            lines = myInputDB.readlines()
            for line in lines:
                if line.startswith("@ITEM"):
                    line = line[6:]
                    index = line.index("=")
                    itemID = int(line[0:index])
                    stringValue= line[index+1:]
                    mapItemIDtoStringValue[itemID] = stringValue
        self.subconvert(mapItemIDtoStringValue, outputFile, outputFileConverted)
    def  isInteger(self, string) :
        result = None
        try :
            result = int(string)
        except :
            return None
        return result