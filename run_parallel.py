#!/usr/bin/python3

import sys, subprocess, argparse, logging
from threading import Thread

def process_tasks(tasks, results, start, end):
    logging.info("processing task range: ({}, {})".format(start, end))
    for i in range(start, end):
        results[i] = subprocess.check_output(tasks[i]["command"].split()).decode('utf-8').strip()
        logging.info("processed task: {}".format(i))

def main(thread_count):
    tasks = []
    for line in sys.stdin:
        meta = line.rstrip()
        command = sys.stdin.readline().rstrip()
        tasks.append({"meta": meta, "command": command})

    threads = []
    results = [""] * len(tasks)
    block = (len(tasks) + thread_count - 1) // thread_count
    logging.info("total tasks: {}".format(len(tasks)))

    for i in range(thread_count):
        threads.append(Thread(target = process_tasks, args = (tasks, results, block * i, min(block * (i + 1), len(tasks)), )))
        threads[-1].start()

    for thread in threads:
        thread.join();

    for i in range(len(tasks)):
        print(tasks[i]["meta"], results[i])

if __name__ == "__main__":
    logging.basicConfig(\
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO)

    parser = argparse.ArgumentParser(description='TBD')
    parser.add_argument("--threads", help="number of threads for processing", default=8)
    args = parser.parse_args()

    main(int(args.threads))
