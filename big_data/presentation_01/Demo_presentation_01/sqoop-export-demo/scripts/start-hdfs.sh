#!/usr/bin/env bash
set -e

echo "Starting HDFS..."

if [ ! -d /data/hdfs/namenode/current ]; then
  echo "Formatting NameNode..."
  hdfs namenode -format -force
fi

hdfs --daemon start namenode || true
hdfs --daemon start datanode || true

echo "Checking Java processes..."
jps

echo "Checking HDFS root..."
hdfs dfs -ls / || true

echo "HDFS started successfully."