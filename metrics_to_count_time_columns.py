# Usage: curl -X GET localhost:4040/metrics | grep "near_database_op_latency_by_op_and_column_sum\|near_database_op_latency_by_op_and_column_count" | perl -n -e'/.*"(.*)",op.* (.*)/ && print "$1 $2\n"' > x && python3 b.py x y
import sys

z = dict()
with open(sys.argv[1]) as f:
    for line in f:
        tokens = line.rstrip().split(' ')
        tokens2 = f.readline().rstrip().split(' ')
        assert tokens[0] == tokens2[0], "different columns: {} {}".format(tokens[0], tokens2[0])
        z[tokens[0]] = [tokens[1], tokens2[1]]

for j in range(0, 2):
    print("count" if j == 1 else "time")
    with open(sys.argv[2]) as f:
        for line in f:
            col = line.rstrip()
            if col in z:
                print(z[col][j])
            else:
                print("")
