start = "/home/ubuntu/nearcore/in"
end = "/home/ubuntu/nearcore/out"
a = []
zero_count = 0
count = 0
opened = False
z = dict()
sz = 0
ssts = 0
with open("output.txt") as f:
    index = 0
    for line in f:
        if ".sst" in line:
            ssts += 1

        if start in line:
            assert not opened
            assert count == 0, "overlapping segments: {}".format(index)
            count = 0
            opened = True
        elif end in line:
            assert opened
            opened = False
            if not count in z:
                z[count] = 0
            z[count] += 1
            sz += 1
            count = 0
        else:
            if opened:
                count += 1
        index += 1

print("total RocksDB.get calls:", sz)
print("total files opened:", ssts)
for i in range(0, 10):
    if i in z:
        print(z[i], "get calls opened", i, "files")
