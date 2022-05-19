import sys

a = []
with open(sys.argv[1]) as f:
    for line in f:
        val = float(line.strip())
        a.append(val)
a.sort()

ps = [50, 90, 95, 99, 100]
for p in ps:
    idx = min(len(a) * 100 / p, len(a) - 1)
    print(p, a[idx])
