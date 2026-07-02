FROM eclipse-temurin:8-jdk-focal

ENV HADOOP_VERSION=3.3.6
ENV SQOOP_VERSION=1.4.7
ENV HADOOP_HOME=/opt/hadoop
ENV SQOOP_HOME=/opt/sqoop
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SQOOP_HOME/bin

RUN echo "deb http://archive.ubuntu.com/ubuntu focal universe" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    curl \
    tar \
    procps \
    net-tools \
    nano \
    libpostgresql-jdbc-java \
    libcommons-lang-java \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    -o /tmp/hadoop.tar.gz \
    && tar -xzf /tmp/hadoop.tar.gz -C /opt \
    && ln -s /opt/hadoop-${HADOOP_VERSION} /opt/hadoop \
    && rm -f /tmp/hadoop.tar.gz

RUN curl -L https://archive.apache.org/dist/sqoop/${SQOOP_VERSION}/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0.tar.gz \
    -o /tmp/sqoop.tar.gz \
    && tar -xzf /tmp/sqoop.tar.gz -C /opt \
    && ln -s /opt/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0 /opt/sqoop \
    && rm -f /tmp/sqoop.tar.gz

RUN cp /usr/share/java/postgresql.jar /opt/sqoop/lib/postgresql.jar && \
    cp /usr/share/java/commons-lang.jar /opt/sqoop/lib/commons-lang.jar

RUN mkdir -p /data/hdfs/namenode /data/hdfs/datanode

RUN printf '%s\n' \
    '<configuration>' \
    '  <property>' \
    '    <name>fs.defaultFS</name>' \
    '    <value>hdfs://localhost:9000</value>' \
    '  </property>' \
    '</configuration>' \
    > /opt/hadoop/etc/hadoop/core-site.xml

RUN printf '%s\n' \
    '<configuration>' \
    '  <property>' \
    '    <name>dfs.replication</name>' \
    '    <value>1</value>' \
    '  </property>' \
    '  <property>' \
    '    <name>dfs.namenode.name.dir</name>' \
    '    <value>file:/data/hdfs/namenode</value>' \
    '  </property>' \
    '  <property>' \
    '    <name>dfs.datanode.data.dir</name>' \
    '    <value>file:/data/hdfs/datanode</value>' \
    '  </property>' \
    '</configuration>' \
    > /opt/hadoop/etc/hadoop/hdfs-site.xml

RUN printf '%s\n' \
    '<configuration>' \
    '  <property>' \
    '    <name>mapreduce.framework.name</name>' \
    '    <value>local</value>' \
    '  </property>' \
    '</configuration>' \
    > /opt/hadoop/etc/hadoop/mapred-site.xml

RUN echo "export JAVA_HOME=/opt/java/openjdk" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

COPY data /root/data
COPY scripts /root/scripts
RUN chmod +x /root/scripts/*.sh

WORKDIR /root

CMD ["bash"]