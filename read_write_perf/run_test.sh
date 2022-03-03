#!/bin/bash -e

export CARGO_PROFILE_RELEASE_LTO=fat
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
cargo build --release -p runtime-params-estimator --features required
# target/release/runtime-params-estimator --metric time --costs RocksDbReadValueByte,RocksDbInsertValueByte --home ~/.near
python3 run_perf_tests_in_parallel.py
