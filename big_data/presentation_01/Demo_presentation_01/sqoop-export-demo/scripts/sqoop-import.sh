#!/usr/bin/env bash
set -e

DB_URL="jdbc:postgresql://pg-sqoop-demo:5432/sqoop_demo"
DB_USER="postgres"
DB_PASSWORD="p@ssw0rd"

echo "======================================"
echo "    BẮT ĐẦU DEMO SQOOP IMPORT"
echo "======================================"

rm -rf /root/libjars /tmp/sqoop-src
mkdir -p /root/libjars /tmp/sqoop-src

echo "[1/2] Import bảng 'class' từ Postgres lên HDFS..."

sqoop codegen \
  --connect "$DB_URL" \
  --username "$DB_USER" \
  --password "$DB_PASSWORD" \
  --table class \
  --class-name ClassTable \
  --driver org.postgresql.Driver \
  --bindir /root/libjars \
  --outdir /tmp/sqoop-src

cp /root/libjars/ClassTable.jar /opt/sqoop/lib/ClassTable.jar
export HADOOP_CLASSPATH="/root/libjars/ClassTable.jar:/opt/sqoop/lib/ClassTable.jar:/opt/sqoop/lib/*:$HADOOP_CLASSPATH"

sqoop import \
  -D mapreduce.job.user.classpath.first=true \
  -libjars /root/libjars/ClassTable.jar \
  --connect "$DB_URL" \
  --username "$DB_USER" \
  --password "$DB_PASSWORD" \
  --table class \
  --class-name ClassTable \
  --target-dir hdfs://localhost:9000/demo/class \
  --delete-target-dir \
  --num-mappers 1 \
  --driver org.postgresql.Driver

echo "--> Xác nhận dữ liệu 'class' đã lên HDFS:"
hdfs dfs -ls /demo/class
hdfs dfs -cat /demo/class/part-m-00000

echo ""
echo "[2/2] Import bảng 'teacher' từ Postgres lên HDFS..."

sqoop codegen \
  --connect "$DB_URL" \
  --username "$DB_USER" \
  --password "$DB_PASSWORD" \
  --table teacher \
  --class-name TeacherTable \
  --driver org.postgresql.Driver \
  --bindir /root/libjars \
  --outdir /tmp/sqoop-src

cp /root/libjars/TeacherTable.jar /opt/sqoop/lib/TeacherTable.jar
export HADOOP_CLASSPATH="/root/libjars/TeacherTable.jar:/opt/sqoop/lib/TeacherTable.jar:/opt/sqoop/lib/*:$HADOOP_CLASSPATH"

sqoop import \
  -D mapreduce.job.user.classpath.first=true \
  -libjars /root/libjars/TeacherTable.jar \
  --connect "$DB_URL" \
  --username "$DB_USER" \
  --password "$DB_PASSWORD" \
  --table teacher \
  --class-name TeacherTable \
  --target-dir hdfs://localhost:9000/demo/teacher \
  --delete-target-dir \
  --num-mappers 1 \
  --driver org.postgresql.Driver

echo "--> Xác nhận dữ liệu 'teacher' đã lên HDFS:"
hdfs dfs -ls /demo/teacher
hdfs dfs -cat /demo/teacher/part-m-00000

echo "======================================"
echo "    SQOOP IMPORT HOÀN TẤT!"
echo "======================================"
