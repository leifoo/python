import csv
import sys


#filename = "buildlog_20190917111401"
INT_MAX = sys.maxsize  
linenumber = INT_MAX
testresult = []

class Test:
    def __init__(self, directory, runtime, result):
        self.name   = directory
        self.time   = runtime
        self.status = result

try:
    filename = sys.argv[1]
except:
    print "Wrong usage!!!"
    print "Correct usage: python readresult.py buildlog"
    sys.exit(1)

# need quotes ("")
#filename = input("Enter build file name:") 

file = open(filename, "r")

for i, row in enumerate(file):
    if "Total time taken" in row:
        linenumber = i + 2
        print row
        
    if i >= linenumber:
        data = row.split()
        if data[2] == '(s)':
            print data
            if data[3] == 'OK':
                s = data[3]
            if len(data) == 5 and data[4] == 'FAILED':
                s = data[4]
            test = Test(data[0], data[1], s)
            testresult.append(test)

testresultsort = sorted(testresult, key=lambda x: x.name)

with open(filename+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for elem in testresultsort:
        writer.writerow([elem.name, elem.status, elem.time])


file.close()
