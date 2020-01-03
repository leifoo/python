# try/except is about 10% slower than without it, but faster than an explicit if as long as the condition is not met.

import timeit

statements=["""\
try:
    b = 10/a
except ZeroDivisionError:
    pass""",
"""\
if a:
    b = 10/a""",
"b = 10/a"]

for a in (1,0):
    for s in statements:
        t = timeit.Timer(stmt=s, setup='a={}'.format(a))
        print("a = {}\n{}".format(a,s))
        print("%.3f usec/pass\n" % (1000000 * t.timeit(number=100000)/100000))
