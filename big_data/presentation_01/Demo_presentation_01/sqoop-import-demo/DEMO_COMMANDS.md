# DEMO COMMANDS

Setup môi trường và reset sạch dữ liệu cũ.
```bash
cd "/Users/minhtuan25/Desktop/MinhTuanCode/MasterAI/Big Data/presentation_01"
cp .env.example .env
curl -L -o postgresql-42.7.12.jar https://jdbc.postgresql.org/download/postgresql-42.7.12.jar
docker compose down -v
docker compose up -d
docker compose ps
```

Kiểm tra dữ liệu nguồn trong Postgres.
```bash
docker exec -it postgres psql -U postgres -d studentdb -c "SELECT * FROM class ORDER BY id;"
docker exec -it postgres psql -U postgres -d studentdb -c "SELECT * FROM teacher ORDER BY id;"
```

Import bảng `class` từ Postgres sang HDFS.
```bash
docker exec -it sqoop sqoop import \
  --connect "jdbc:postgresql://postgres:5432/studentdb" \
  --username postgres \
  --password 123456 \
  --table class \
  --target-dir hdfs://namenode:8020/demo/class \
  --delete-target-dir \
  --num-mappers 1
```

Xác nhận dữ liệu `class` đã lên HDFS.
```bash
docker exec -it namenode hdfs dfs -ls /demo/class
docker exec -it namenode hdfs dfs -cat /demo/class/part-m-00000
```

Import bảng `teacher` từ Postgres sang HDFS.
```bash
docker exec -it sqoop sqoop import \
  --connect "jdbc:postgresql://postgres:5432/studentdb" \
  --username postgres \
  --password 123456 \
  --table teacher \
  --target-dir hdfs://namenode:8020/demo/teacher \
  --delete-target-dir \
  --num-mappers 1
```

Xác nhận dữ liệu `teacher` đã lên HDFS.
```bash
docker exec -it namenode hdfs dfs -ls /demo/teacher
docker exec -it namenode hdfs dfs -cat /demo/teacher/part-m-00000
```

Dừng toàn bộ services sau khi demo.
```bash
docker compose down
```

