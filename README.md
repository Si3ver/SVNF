# Scalable Virtual Network Function Placement

## 说明

转载或引用请联系本项目作者：周伟林 izhouwl@163.com

如果对你有帮助，麻烦加个star吧！

## 依赖库

请安装python3、argparse、numpy等依赖库，推荐用pip3安装。

## 运行说明

1. 生成流量

```
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o output/traffic.txt
```

+ -c 指定生成的流量条数，默认1000条
+ -k 指定拓扑基于 k-阶胖树 拓扑。决定了服务器编号的起始地址和终止地址 [(5k^2)/4 , (5k^2)/4 + (3k^3)/4 -1 ]
+ -Tm 指定最小流速率
+ -al 指定tr与Tm的关系因子
+ -s 指定随机数的起始随机种子
+ -o 指定输出结果存储到的文件名

2. 运行SVNFP算法，进行VNF放置

```
python3 svnfp.py -k 20 -i output/traffic.txt -o output/result.txt -n
或简写如下：
python3 svnfp.py -k 20 -n
```

+ -i 指定读入文件名
+ -o 指定输出文件名

3. 分析结果，统计总流路径长度、平均流路径长度、接受率等

```
python3 resultAnalysis.py -k 20 -i output/result.txt -o output/analysis.txt
或简写如下：
python3 resultAnalysis.py -k 20
```

+ -i 指定读入文件名
+ -o 指定输出文件名

## 文件格式说明

1. traffic.txt

```
r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
<src, dst, tr, peak, sfcLen, <sfc>>
```

2. result.txt

```
r'(?P<dId>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<exp>[0-9]+\.[0-9]+)\s(?P<mipsList>\[([0-9]+, )*[0-9]*\])\s(?P<servList>\[([0-9]+, )*[0-9]*\])'
<dId, src, dst, exp, <mipsList>, <severNo>>
serverNo 为对应vnf的所部署到的服务器编号，若为空，表示reject；
```

3. analysis.txt

```
<dId, hops>
```

## 评估

当服务器mips超过其计算容量值时，将丢包。
实验：依次随机选择一条流，让其流量从tr突变为peak。
评估参数： 
1. sum plrServers记录存在丢包情况的服务器数量。$cnt_ps$
2. 单台服务器丢包率 $plr_k = 超出mips/其计算容量$
plr1 记录丢包服务器的平均丢包率。$plr = 总丢包率/cnt_ps$
plr2 记录总的丢包率。$plr = 总丢包率/总服务器数量$



1. 随着 tr -> peak的流数量增加，丢包率的变化情况。

```
python3 plr.py -c 1000 -k 20 -i ../output/result.txt -o ../output/plr.txt -s 10
或简写如下：
python3 plr.py
```

+ -c 指定生成的流量条数，默认1000条
+ -k 指定拓扑基于 k-阶胖树 拓扑，默认20
+ -i 指定读入文件名
+ -o 指定输出文件名
+ -s 指定随机数的起始随机种子

2. 画图

```
python3 draw.py
```

## 实验数据

使用20-阶胖树拓扑，共有2000台服务器，每台服务器计算能力为100000mips。

1. 1000条流量

```
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o output/traffic.txt
python3 svnfp.py -k 20 -i output/traffic.txt -o output/result.txt -n
python3 resultAnalysis.py -c 1000 -k 20 -i output/result.txt -o output/analysis.txt
python3 plr.py -c 1000 -k 20 -i output/result.txt -o output/plr.txt -s 10
```

2. 5000条流量

```
python3 traffic.py -c 5000 -k 20 -Tm 10 -al 2.1 -s 10 -o output/traffic.txt
python3 svnfp.py -k 20 -i output/traffic.txt -o output/result.txt -n
python3 resultAnalysis.py -c 5000 -k 20 -i output/result.txt -o output/analysis.txt
python3 plr.py -c 5000 -k 20 -i output/result.txt -o output/plr.txt -s 10
```
