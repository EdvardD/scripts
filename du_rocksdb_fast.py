#!/usr/bin/python3
# Command to compile sst_dump: cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DWITH_LZ4=1 -DWITH_ZSTD=1 -DWITH_SNAPPY=1 -DCMAKE_TOOLCHAIN_FILE=/home/edvard/vcpkg/scripts/buildsystems/vcpkg.cmake .. && make -j8 sst_dump ldb

import os, sys, subprocess
from threading import Thread
from time import sleep
from pathlib import Path

def process_files(files, results, tindex):
    print("Got", len(files), "to process")
    results[tindex] = [0] * 60
    for i in range(len(files)):
        filename = files[i]
        output = subprocess.check_output(['../rocksdb/build/tools/sst_dump', '--file=' + str(filename), '--show_properties']).decode('utf-8')
        for line in output.split('\n'):
            if "column family ID" in line:
                index = int(line.split(' ')[-1]) - 1
                results[tindex][index] += os.path.getsize(filename)
                print("processed:", str(filename), "index:", index, "progress:", str(round(i / len(files) * 100, 1)) + "%")

if __name__ == "__main__":
    files = [file for file in Path(sys.argv[1]).glob("*.sst")]

    THREADS = 8
    threads = []
    results = [None] * THREADS
    block = (len(files) + THREADS - 1) // THREADS
    print(len(files))
    for i in range(THREADS):
        cfiles = files[block * i : min(block * (i + 1), len(files))]
        threads.append(Thread(target = process_files, args = (cfiles, results, i, )))
        threads[-1].start()

    for thread in threads:
        thread.join();

    result = [0] * len(results[0])
    for j in range(len(result)):
        for i in range(len(results)):
            if results[i]:
                result[j] += results[i][j]
        print(j, result[j])
