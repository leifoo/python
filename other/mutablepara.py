def reassign(myList):
    myList = [1, 2, 3]

# elem = elem * 2 reassign the identifier elem to a newly constructed value; it does not change formal parameters  
def scale(myList):
    for elem in myList:
        elem = elem * 2

# *= does change formal parameters
def scale2(myList):
    for i in range(len(myList)):
        myList[i] *= 2

initList = [2, 2, 2]
print('initList = ', initList)
reassign(initList)
print('initList = ', initList)

scale(initList)
print('initList = ', initList)

scale2(initList)
print('initList = ', initList)
