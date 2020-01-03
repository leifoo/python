import time 

count = 0
max_value = 10**8

print("try except")

start_time = time.time()

while count < max_value:
    try:
        count += 1
    except:
        pass

elapsed_time = time.time() - start_time

print("count = ", count, ", max_value = ", max_value)
print("Elapsed Time: {0:.4f} s".format(elapsed_time))


count = 0

start_time = time.time()

while count < max_value:
    count += 1

elapsed_time = time.time() - start_time

print("count = ", count, ", max_value = ", max_value)
print("Elapsed Time: {0:.4f} s".format(elapsed_time))


"""
Result: try except is about 10% slower than without it, but faster than an explicit if as long as the condition is not met.

try except
count =  100000000 , max_value =  100000000
Elapsed Time: 8.1864 s
count =  100000000 , max_value =  100000000
Elapsed Time: 7.3490 s
"""