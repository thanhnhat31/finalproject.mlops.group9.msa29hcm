#!/usr/bin/env bash
set -euo pipefail

NAME_DIR="/tmp/hadoop-root/dfs/name"

mkdir -p "${NAME_DIR}"

if [ ! -f "${NAME_DIR}/current/VERSION" ]; then
  echo "Formatting NameNode metadata directory..."
  hdfs namenode -format -force -nonInteractive
fi

exec hdfs namenode
