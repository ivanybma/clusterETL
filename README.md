# clusterETL
two workers, one master cluster linking another machine with mysql to simulate the etl extracting info from input json to mysql
this project include:
1. reset.sh  all nodes
6. rst.sh all nodes
3. streamfile.py master
4. command_list to install hadoop automatically
5. spark_install to install spark automatically  ----> note: this script is to install the spark 1.6, to install a newer version, we need to change the script to let it get the newer version instead
9. spark_upgrade  to upgrade the spark in case we want to upgrade

10. streamfile.py  etl doing json file parsing and then write info to mysql in other machine
