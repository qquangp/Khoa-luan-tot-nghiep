from ResultConverter import ResultConverter
class MainTestResultConverter:
    def main( args) :
        inputDB = "fruithut.txt"
        inputResult = "./Output2/Out_fruithut.txt"
        outputFile = "./Output2/Out_fruithutConv.txt"
        converter = ResultConverter()
        converter.convert(inputDB, inputResult, outputFile)

if __name__=="__main__":
    MainTestResultConverter.main([])
           
           