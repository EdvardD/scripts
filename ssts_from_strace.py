import re, subprocess, os.path

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
regex = re.compile("^\d+ (\d{2}:\d{2}:\d{2}).*\/(\d+)\.sst.*$")
with open("output.txt") as f:
    for line in f:
        match = regex.match(line.strip())
        if match:
            number = match.groups()[1]
            column = get_column(number)
            if not column in z:
                z[column] = 0
            z[column] += 1
print("files opens:")
print(z)
