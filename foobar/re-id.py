def solution(i):
    start, end = 4, 10
    string = '23'
    label = [False, False, True, True]

    while len(string) < i+5 :
        new_string, label = findPrimes(start, end, label)
        string += new_string
        start = end
        end += 100 

    for i, elem in enumerate(label):
        if elem:
            print(i)
    return string[i:i+5]

# search for prime numbers less than a non-negative number n 
def findPrimes(start, end, label):
    string = ''
    label = label + [True] * (end - start)
    limit = int(end**0.5) + 1

    for i in range(2, limit):
        if label[i]:
            startIndex = max(i**2, start // i  * i)
            print('startIndex=', startIndex, end)
            for j in range(startIndex, end, i):
                label[j] = False

    for i in range(start, end):
        if label[i]:
            string += str(i)
  
    return string, label
    

print(solution(100))