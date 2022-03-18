#!/bin/bash -e

rm -rf exp

sizes=(128 256 512 1024)
indexes=(50 51 52 53)
for i in {0..3}; do
  size=${sizes[$i]}

  echo "Processing size: $size"
  sed -i "'s/ColState = 5/ColState = ${indexes[$i]}/g'" core/store/src/db.rs
  sed -i "'s/ColState${size}MIB = ${indexes[$i]}/ColState${size}MIB = 5/g'" core/store/src/db.rs
  cargo build -p neard --release

  time sudo perf record -F500 -g --call-graph=dwarf,65528 target/release/neard --home /home/ubuntu/.near view_state apply_range --shard-id=1 --start-index 58883720 --end-index 58884220 --sequential

  output_dir="exp/${size}"
  mkdir -p $output_dir
  mv perf.data $output_dir
  time perf script -F +pid > $output_dir/perfbench.script &

  git checkout core/store/src/db.rs
done
