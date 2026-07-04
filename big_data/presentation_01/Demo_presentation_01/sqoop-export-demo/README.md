# Apache Sqoop Export Demo

This project demonstrates how Apache Sqoop exports data from Hadoop HDFS back to PostgreSQL.

## Demo Flow

```text
HDFS → Apache Sqoop Export → PostgreSQL
```

## Technologies

- Apache Hadoop 3.3.6
- Apache Sqoop 1.4.7
- PostgreSQL 16
- Docker
- Docker Compose

## Project Structure

```text
sqoop-export-demo/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .gitignore
├── postgres/
│   └── init.sql
├── scripts/
│   ├── start-hdfs.sh
│   ├── prepare-hdfs-data.sh
│   └── sqoop-export.sh
```

## Quick Start

### 1. Start containers

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

Expected containers:

```text
pg-sqoop-demo
hadoop-sqoop
```

### 2. Enter Hadoop/Sqoop container

```bash
docker exec -it hadoop-sqoop bash
```

### 3. Start HDFS

Inside the `hadoop-sqoop` container, run:

```bash
/root/scripts/start-hdfs.sh
```

Expected output includes:

```text
NameNode
DataNode
Jps
```

### 4. Prepare source data in HDFS

```bash
/root/scripts/prepare-hdfs-data.sh
```

This script creates a CSV file and uploads it to HDFS:

```text
/user/root/export_demo/students_export_data.csv
```

Sample data:

```text
1,Nguyen Van A,Information Technology,3.40
2,Tran Thi B,Data Science,3.70
3,Le Van C,Computer Science,3.20
```

### 5. Run Sqoop Export

```bash
/root/scripts/sqoop-export.sh
```

This command exports data from HDFS to PostgreSQL table:

```text
students_export
```

### 6. Verify result in PostgreSQL

Open another terminal and run:

```bash
docker exec -it pg-sqoop-demo psql -U postgres -d sqoop_demo
```

Then run:

```sql
SELECT * FROM students_export;
```

Expected result:

```text
 id |     name     |         major          | gpa
----+--------------+------------------------+------
  1 | Nguyen Van A | Information Technology | 3.40
  2 | Tran Thi B   | Data Science           | 3.70
  3 | Le Van C     | Computer Science       | 3.20
```

## Hadoop Web UI

Open:

```text
http://localhost:9870
```

If running Docker inside a virtual machine, open from Windows using the Ubuntu VM IP:

```text
http://<ubuntu-vm-ip>:9870
```

Example:

```text
http://192.168.118.128:9870
```

Go to:

```text
Utilities → Browse the file system
```

Check HDFS path:

```text
/user/root/export_demo
```

## DBeaver PostgreSQL Connection

If PostgreSQL is running inside Ubuntu VM Docker, connect from Windows DBeaver using:

```text
Host: <ubuntu-vm-ip>
Port: 5433
Database: sqoop_demo
Username: postgres
Password: 123456
```

Example:

```text
Host: 192.168.118.128
Port: 5433
Database: sqoop_demo
Username: postgres
Password: 123456
```

## Reset demo data

To clear PostgreSQL data and Docker volume:

```bash
docker compose down -v
docker compose up -d --build
```

## Vietnamese Explanation

Apache Sqoop Export dùng để chuyển dữ liệu từ Hadoop HDFS về lại cơ sở dữ liệu quan hệ.

Trong demo này:

```text
HDFS → Apache Sqoop Export → PostgreSQL
```

Dữ liệu nguồn ban đầu nằm trong HDFS tại:

```text
/user/root/export_demo
```

Sau đó, Sqoop Export sẽ đọc dữ liệu từ HDFS và ghi vào bảng PostgreSQL:

```text
students_export
```

Khi chạy:

```sql
SELECT * FROM students_export;
```

Nếu thấy dữ liệu xuất hiện trong PostgreSQL, nghĩa là quá trình Sqoop Export đã thành công.

## Sample CSV Data

The source CSV file is located at:

```text
data/students_export_data.csv
```
