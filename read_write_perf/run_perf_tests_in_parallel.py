#!/usr/bin/python3

import os, sys, subprocess
from threading import Thread
from time import sleep
from pathlib import Path

def process_files(tindex):
    for i in range(2):
        output = subprocess.check_output(['/home/edvard/nearcore/target/release/runtime-params-estimator', '--metric', 'time', '--costs', 'RocksDbReadValueByte,RocksDbInsertValueByte', '--home', '/home/edvard/.near']).decode('utf-8')
        print(output)

if __name__ == "__main__":
    THREADS = 4
    threads = []
    for i in range(THREADS):
        threads.append(Thread(target = process_files, args = (i, )))
        threads[-1].start()

    for thread in threads:
        thread.join();
