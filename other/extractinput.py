import sys

try:
    filename = sys.argv[1]
except:
    print('Wrong usage!!!')
    print('Correct usage: python extractinput.py file.txt')
    sys.exit(1)

count = 0

file = open(filename, "r")
outputname = filename[:-4]+'_input.txt'
output = open(outputname, 'w')
        
for i,row in enumerate(file):
    if 'm_inputFileNames' in row:
        data = row.split()
        output.write(data[2]+'\n')
        print(count, data[2])
        count += 1

print(filename, ' contains ', count, ' input files')

file.close()
output.close()