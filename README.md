# NFV simu

生成流量
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o traffic.txt
生流定义为，<源服务器编号、目标服务器编号、流速率、SFCPubLen、SFCPriLen、SFC>

python3 traffic.py -c 10 -k 20 -Tm 10 -al 2.1 -s 10 -o traffic.txt
python3 svnfp.py -i traffic.txt -l result.txt -n
分析结果：
python3 resultAnalysis.py -i result.txt -l log.txt -n
