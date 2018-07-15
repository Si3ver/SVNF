cd myGen

生成流量
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o traffic.txt
生流定义为，<源服务器编号、目标服务器编号、流速率、SFCPubLen、SFCPriLen、SFC>

随机x%条流，增大y%
python3 increase.py -c


分割流量




python3 traffic.py -c 10 -k 20 -Tm 10 -al 2.1 -s 10 -o traffic.txt
python3 svnfp.py -i traffic.txt -l log.txt -d traffic.html -n
