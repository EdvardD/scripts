# Compute per column RocksDB size

Build sst_dump:
```
du_rocksdb_fast/build.sh
```

Run the tool:
```
du_rocksdb_fast/run.py --rocksdb-data=~/.near/data
```

If you already have a built sst_dump tool you can skip the first step and specify the path to sst_dump:
```
du_rocksdb_fast/run.py --rocksdb-data=~/.near/data --sst-dump=~/rocksdb/build/tools/sst_dump
```
