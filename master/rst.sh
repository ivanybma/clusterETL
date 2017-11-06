stop-hbase.sh
$SPARK_HOME/sbin/stop-all.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh stop historyserver
$HADOOP_HOME/sbin/stop-yarn.sh
$HADOOP_HOME/sbin/stop-dfs.sh

$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver
$SPARK_HOME/sbin/start-all.sh
start-hbase.sh
