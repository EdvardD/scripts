import sys

a = []
with open(sys.argv[1]) as f:
    for line in f:
        val = float(line.strip())
        a.append(val)
a.sort()

ps = [1, 5, 10, 50, 90, 95, 99, 100]
for p in ps:
    idx = min(len(a) * p // 100, len(a) - 1)
    print("{0:3}p".format(p), a[idx])
