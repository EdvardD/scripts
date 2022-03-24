import re, sys, subprocess

sst_dump = '/home/ubuntu/scripts/du_rocksdb_fast/rocksdb/build/tools/sst_dump'

def get_column_id(filename):
    output = subprocess.check_output([sst_dump, '--file=' + str(filename), '--show_properties']).decode('utf-8')
    for line in output.split('\n'):
        if "column family name" in line:
            return line.split(' ')[-1]
    return "unknown"

regex = re.compile("^\d+ (\d{2}:\d{2}:\d{2}).*\/(\d+)\.sst.*$")

occ = dict()
total_opens = 0
with open("output.txt") as f:
    for line in f:
        match = regex.match(line.strip())
        if match:
            total_opens += 1
            time = match.groups()[0]
            number = int(match.groups()[1])
            if not number in occ:
                occ[number] = 1
            else:
                occ[number] += 1

#for key, value in occ.items():
#    if value > 200:
#        print(key, value, "column_id:", get_column_id("/home/ubuntu/.near/data/{}.sst".format(key)))
#
#sys.exit(0)

res = dict()

for key, value in occ.items():
    if not value in res:
        res[value] = 1
    else:
        res[value] += 1

res = [(occurences, number_of_files) for occurences, number_of_files in res.items()]
res.sort()

for occurences, number_of_files in res:
    print(number_of_files, "files were opened", occurences, "times")
print("Total file open count:", total_opens)
print("Total unique files opened:", len(occ))
