#!/usr/bin/env bash
set -e

echo "Uploading CSV file to HDFS..."

hdfs dfs -mkdir -p /user/root/export_demo
hdfs dfs -put -f /root/data/students_export_data.csv /user/root/export_demo/

echo "Listing HDFS directory..."
hdfs dfs -ls /user/root/export_demo

echo "Reading HDFS file content..."
hdfs dfs -cat /user/root/export_demo/students_export_data.csv

echo "HDFS source data is ready."