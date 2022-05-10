import re, subprocess, os.path, glob

def get_column(file_number):
    filename = '/home/ubuntu/.near/data/data/' + file_number + '.sst'
    if not os.path.exists(filename):
        return "unknown"
    output = subprocess.check_output(["../scripts/du_rocksdb_fast/rocksdb/build/tools/sst_dump", '--file=' + filename, '--show_properties']).decode('utf-8')
    for line in output.split('\n'):
        if "column family name" in line:
            return line.split(' ')[-1]
    return "incorrect"

z = dict()
files = glob.glob('/home/ubuntu/.near/data/data/*.sst')
for i, f in enumerate(files):
    p = i * 100 // len(files)
    pn = (i + 1) * 100 // len(files)
    if p != pn:
        print("processed:", str(p)  + "%")
    number = f.split('/')[-1].split('.')[0]
    column = get_column(number)
    if not column in z:
        z[column] = 0
    z[column] += 1
print("file count per column:")
for x, y in z:
    print(x, y)
