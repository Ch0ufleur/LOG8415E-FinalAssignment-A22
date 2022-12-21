#!/bin/bash

#We ask the user for the appropriate IP where the MySQL service is situated
#For this project, the user can enter the Ip of the cluster, or the Ip of the standalone instance. This will allow the user, after two runs, to compare metrics.
echo 'Please enter MySQL service IP below:'
read ip
sudo sysbench /usr/share/sysbench/oltp_read_write.lua --table-size=1000000 --mysql-host=$ip --mysql-db=sakila --mysql-user=finaltp --mysql-password='' prepare
sudo sysbench /usr/share/sysbench/oltp_read_write.lua --threads=6 --time=60 --max-requests=0 --mysql-host=$ip --mysql-db=sakila --mysql-user='finaltp' --mysql-password='' run
sudo sysbench /usr/share/sysbench/oltp_read_write.lua --threads=6 --time=60 --max-requests=0 --mysql-host=$ip --mysql-db=sakila --mysql-user='finaltp' --mysql-password='' cleanup
echo 'Benchmark is complete. The results are above.'