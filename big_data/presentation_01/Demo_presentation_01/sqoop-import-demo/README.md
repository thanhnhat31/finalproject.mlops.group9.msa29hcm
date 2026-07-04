# Apache Sqoop Import Demo

This project demonstrates how Apache Sqoop import data from PostgreSQL to Hadoop HDFS

## Demo Flow

```text
PostgreSQL → Apache Sqoop → HDFS
```

## Technologies

- Apache Hadoop 3.4.3
- Apache Sqoop 1.4.7
- PostgreSQL 15
- Docker
- Docker Compose

## Project Structure

```text
sqoop-import-demo/
├── postgres/
│   ├── class.sql
│   └── teacher.sql
├── scripts/
│   └── start-namenode.sh
├── .env
├── .env.example
├── DEMO_COMMANDS.md
├── docker-compose.yml
├── postgresql-42.7.12.jar
└── README.md
```

## Quick Start

### 1.  Set up the environment and reset all old data
```bash
cd sqoop-import-demo
docker compose down -v
docker compose up -d
docker compose ps
```
### 2. Check source data in Postgres
```bash
docker exec -it postgres psql -U postgres -d studentdb -c "SELECT * FROM class ORDER BY id;"
docker exec -it postgres psql -U postgres -d studentdb -c "SELECT * FROM teacher ORDER BY id;"
```

### 3. Import table `class` from Postgres to HDFS.
```bash
docker exec -it sqoop sqoop import \
  --connect "jdbc:postgresql://postgres:5432/studentdb" --username postgres --password p@ssw0rd --table class --target-dir hdfs://namenode:8020/demo/class --delete-target-dir --num-mappers 1
```
### 4. Verify data `class` on HDFS.
```bash
docker exec -it namenode hdfs dfs -ls /demo/class
docker exec -it namenode hdfs dfs -cat /demo/class/part-m-00000
```
### 5. Import table `teacher` from Postgres to HDFS.
```bash
docker exec -it sqoop sqoop import \
  --connect "jdbc:postgresql://postgres:5432/studentdb" --username postgres --password p@ssw0rd --table teacher --target-dir hdfs://namenode:8020/demo/teacher --delete-target-dir --num-mappers 1
```
### 6. Verify data `teacher` on HDFS.
```bash
docker exec -it namenode hdfs dfs -ls /demo/teacher
docker exec -it namenode hdfs dfs -cat /demo/teacher/part-m-00000
```





