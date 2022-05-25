#!/usr/bin/python3

import os, sys, subprocess, argparse, random
from threading import Thread
from time import sleep
from pathlib import Path

def process_files(files, sst_dump, results, tindex):
    print("Got", len(files), "to process")
    results[tindex] = [None] * 60
    for i in range(len(results[tindex])):
        results[tindex][i] = []
    for i in range(len(files)):
        filename = files[i]
        try:
            output = subprocess.check_output([sst_dump, '--file=' + str(filename), '--show_properties']).decode('utf-8')
        except:
            print("can't get properties of file:", filename)
            continue
        key_count = -1
        for line in output.split('\n'):
            if "entries:" in line:
                key_count = int(line.split(' ')[-1])
        assert key_count != -1, "Can't find key_count for file: {}".format(str(filename))
        for line in output.split('\n'):
            if "column family ID" in line:
                index = int(line.split(' ')[-1]) - 1
                results[tindex][index].append(key_count)
                print("processed:", str(filename), "index:", index, "progress:", str(round(i / len(files) * 100, 1)) + "%")

def main(rocksdb_data, sst_dump, thread_count):
    files = [file for file in Path(rocksdb_data).expanduser().glob("*.sst")]
    random.shuffle(files)

    threads = []
    results = [None] * thread_count
    block = (len(files) + thread_count - 1) // thread_count
    print(len(files))
    for i in range(thread_count):
        cfiles = files[block * i : min(block * (i + 1), len(files))]
        threads.append(Thread(target = process_files, args = (cfiles, sst_dump, results, i, )))
        threads[-1].start()

    for thread in threads:
        thread.join();

    print("Key count in SST per column")
    for j in range(len(results[0])):
        column = []
        for i in range(len(results)):
            for x in results[i][j]:
                column.append(x)
        if not column:
            continue

        column.sort()

        s = ""
        for i in [50, 90, 95, 99, 100]:
            index = min(len(column) * i // 100, len(column) - 1)
            assert index < len(column), ":( {} {}".format(index, len(column))
            s += " ({}, {})".format(str(i), column[index])
        s = "Column {}:{}".format(j, s)
        print(s)

if __name__ == "__main__":
    default_sst_dump = os.path.dirname(os.path.realpath(__file__)) + '/rocksdb/build/tools/sst_dump'

    parser = argparse.ArgumentParser(description='Computes RocksDB column sizes using several threads')
    parser.add_argument("--rocksdb-data", help="path to rocksdb sst files directory", required=True)
    parser.add_argument("--sst-dump", help="filename of an existing sst_dump binary", default=default_sst_dump)
    parser.add_argument("--threads", help="number of threads for processing", default=8)
    args = parser.parse_args()

    main(args.rocksdb_data, args.sst_dump, int(args.threads))
