#!/bin/bash

git checkout core/store/src/db.rs

column_names=("ColState4KBBlockSize" "ColState8KBBlockSize" "ColState" "ColState32KBBlockSize")
column_ids=(51 52 5 53)
for i in {0..3}; do
  column_name=${column_names[$i]}
  column_id=${column_ids[$i]}

  echo "Processing column: $column_name"
  sed -i "s/ColState = 5/ColState = $column_id/g" core/store/src/db.rs
  sed -i "s/$column_name = $column_id/$column_name = 5/g" core/store/src/db.rs
  git diff

  make neard
  for j in {1..10}; do
        echo "Run: $j"
	{ time target/release/neard view_state apply_range --shard-id=1 --start-index 58883720 --end-index 58884220 --sequential; } 2>&1 | grep "real\|sys" >> exp/$column_name.txt
        echo "End"
  done

  git checkout core/store/src/db.rs
done
