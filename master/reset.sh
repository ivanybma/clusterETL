#this is to reset the hadoop&spark configuration file whenever my cluster is restarted
#request for new cluster dns:
echo Master=?
read master
echo Worker1=?
read worker1
echo Worker2=?
read worker2

#all notes need:
sed -i -e "2s/\(HostName \).*/\1$master/" ~/.ssh/config
sed -i -e "6s/\(HostName \).*/\1$worker1/" ~/.ssh/config
sed -i -e "10s/\(HostName \).*/\1$worker2/" ~/.ssh/config

sed -i -e "22s/\(<value>hdfs:\/\/\).*/\1$master\:9000<\/value\>/" $HADOOP_CONF_DIR/core-site.xml
sed -i -e "26s/\(<value>\).*/\1$master\<\/value\>/" $HADOOP_CONF_DIR/yarn-site.xml
sed -i -e "22s/\(<value>\).*/\1$master\:54311<\/value\>/" $HADOOP_CONF_DIR/mapred-site.xml

sed -i -e "24s/\".*\"/\"$master\"/" $SPARK_HOME/conf/spark-env.sh

sudo sed -i -e "s/.*192-168-109-152/$master 192-168-109-152/" /etc/hosts
sudo sed -i -e "s/.*192-168-109-151/$worker1 192-168-109-151/" /etc/hosts
sudo sed -i -e "s/.*192-168-109-153/$worker2 192-168-109-153/" /etc/hosts

sed -i -e "1s/.*/$worker1/" $SPARK_HOME/conf/slaves
sed -i -e "2s/.*/$worker2/" $SPARK_HOME/conf/slaves

sed -i -e "26s/\(<value>hdfs:\/\/\).*/\1$master\:9000<\/value\>/" $HBASE_HOME/conf/hbase-site.xml
sed -i -e "34s/\(<value>hdfs:\/\/\).*/\1$master\:9000\/zookeeper<\/value\>/" $HBASE_HOME/conf/hbase-site.xml
iplst=$master,' '$worker1,' '$worker2
sed -i -e "38s/\(<value>\).*/\1$iplst<\/value\>/" $HBASE_HOME/conf/hbase-site.xml
