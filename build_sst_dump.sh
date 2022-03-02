#!/bin/bash -e

pushd $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ ! -d vcpkg ]; then
  git clone https://github.com/microsoft/vcpkg.git
  ./vcpkg/bootstrap-vcpkg.sh
  ./vcpkg/vcpkg install zstd lz4 snappy
fi

if [ ! -d rocksdb ]; then
  git clone https://github.com/facebook/rocksdb.git
fi

mkdir -p rocksdb/build
pushd rocksdb/build
cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DWITH_LZ4=1 -DWITH_ZSTD=1 -DWITH_SNAPPY=1 -DCMAKE_TOOLCHAIN_FILE=../../vcpkg/scripts/buildsystems/vcpkg.cmake ..
make -j8 sst_dump ldb
