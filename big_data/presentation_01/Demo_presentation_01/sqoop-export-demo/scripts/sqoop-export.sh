#!/usr/bin/env bash
set -e

DB_URL="jdbc:postgresql://postgres:5432/sqoop_demo"
DB_USER="postgres"
DB_PASSWORD="123456"
TABLE_NAME="students_export"
HDFS_EXPORT_DIR="/user/root/export_demo"
CLASS_NAME="StudentsExport"

echo "Cleaning PostgreSQL target table..."

sqoop eval \
--connect "$DB_URL" \
--username "$DB_USER" \
--password "$DB_PASSWORD" \
--driver org.postgresql.Driver \
--query "TRUNCATE TABLE $TABLE_NAME"

echo "Generating Sqoop ORM class and JAR..."

rm -rf /root/libjars /tmp/sqoop-src
mkdir -p /root/libjars /tmp/sqoop-src

sqoop codegen \
--connect "$DB_URL" \
--username "$DB_USER" \
--password "$DB_PASSWORD" \
--table "$TABLE_NAME" \
--driver org.postgresql.Driver \
--class-name "$CLASS_NAME" \
--bindir /root/libjars \
--outdir /tmp/sqoop-src

cp /root/libjars/${CLASS_NAME}.jar /opt/sqoop/lib/${CLASS_NAME}.jar

export HADOOP_CLASSPATH="/root/libjars/${CLASS_NAME}.jar:/opt/sqoop/lib/${CLASS_NAME}.jar:/opt/sqoop/lib/*:$HADOOP_CLASSPATH"
export CLASSPATH="/root/libjars/${CLASS_NAME}.jar:/opt/sqoop/lib/${CLASS_NAME}.jar:/opt/sqoop/lib/*:$CLASSPATH"

echo "Running Sqoop Export..."

sqoop export \
-D mapreduce.job.user.classpath.first=true \
-libjars /root/libjars/${CLASS_NAME}.jar \
--connect "$DB_URL" \
--username "$DB_USER" \
--password "$DB_PASSWORD" \
--table "$TABLE_NAME" \
--export-dir "$HDFS_EXPORT_DIR" \
--input-fields-terminated-by ',' \
--driver org.postgresql.Driver \
--class-name "$CLASS_NAME" \
--jar-file /root/libjars/${CLASS_NAME}.jar \
--m 1

echo "Sqoop Export completed."
echo "Check PostgreSQL with:"
echo "SELECT * FROM students_export;"