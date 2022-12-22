Instructions to run the code  
After configuring system-wide AWS credentials, appropriate AWS instances can be configured by running the following commands in the terraform-aws/ folder:  

* terraform init  
* terraform apply  

When the instances are up and running, 4 of them are to be configured as a cluster and another one has to be configured as the standalone server (see the tutorials mentioned in report for a how-to). Once the configuration is done, one can rule the benchmark script with the following command (which asks for the IP addresses):  

* bash ./scripts/benchmark.sh  

Now, for the proxy part, there is no code to `run', just a server to start with the appropriate python script. The script flask-proxy.py and the ssh key used to configure the instances of the cluster have to be put in the instance allocated to run the proxy. Then, the appropriate python libraries have to be installed on the instance (flask, sshtunnel, pymysql). Finally, the script can be run with the following command:  

* sudo python3 ./flask-proxy.py -m Master-Node-IP -n2 Data-node-2-IP -n3 Data-node-3-IP -n4 Data-node-4-IP -proxy Proxy-local-IP  

This is starting the server on the instance on port 5000, which is opened according to the security groups. It can now accept requests according to the implementation described above.  

A sample requests.sh script is available in the scripts folder to test the proxy implementation with sample requests:  

* bash ./scripts/requests.sh  

