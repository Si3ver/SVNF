# Scalable Virtual Network Function Placement(SVNFP)

## 说明

转载或引用请联系本项目作者：周伟林 izhouwl@163.com

如果对你有帮助，麻烦加个star吧！

## 依赖库

请安装python3、argparse、numpy、matplotlib等依赖库，推荐用pip3安装，并安装anaconda工具。

## 使用说明

1.生成流量

```console
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o output/traffic.txt
```

+ -c 指定生成的流量条数，默认1000条
+ -k 指定拓扑基于 k-阶胖树 拓扑。决定了服务器编号的起始地址和终止地址 [(5k^2)/4 , (5k^2)/4 + (3k^3)/4 -1 ]
+ -Tm 指定最小流速率
+ -al 指定tr与Tm的关系因子
+ -s 指定随机数的起始随机种子
+ -o 指定输出结果存储到的文件名

2.运行SVNFP算法，进行VNF放置

```console
python3 svnfp.py -k 20 -i output/traffic.txt -o output/result.txt -n
或简写如下：
python3 svnfp.py -k 20 -n
```

+ -i 指定读入文件名
+ -o 指定输出文件名

3.分析结果，统计该放置方法的总FPL、AR值

```console
python3 resultAnalysis.py -k 20 -i output/result.txt -o output/analysis.txt
或简写如下：
python3 resultAnalysis.py -k 20
```

+ -i 指定读入文件名
+ -o 指定输出文件名

## 文件格式说明

1.traffic.txt

```console
r'(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<tr>[0-9]+\.[0-9]+)\s(?P<peak>[0-9]+\.[0-9]+)\s(?P<sfcLen>[0-9]+)\s(?P<sfc>\[([0-9]+, )*[0-9]+\])'
<src, dst, tr, peak, sfcLen, <sfc>>
```

2.result.txt

```console
r'(?P<dId>[0-9]+)\s(?P<src>[0-9]+)\s(?P<dst>[0-9]+)\s(?P<exp>[0-9]+\.[0-9]+)\s(?P<mipsList>\[([0-9]+, )*[0-9]*\])\s(?P<servList>\[([0-9]+, )*[0-9]*\])'
<dId, src, dst, exp, <mipsList>, <severNo>>
serverNo 为对应vnf的所部署到的服务器编号，若为空，表示reject；
```

3.analysis.txt

```console
<dId, hops>
```

## 评估

> 五个评价指标：PLR(packet loss rate)、BSR(bad server rate)、SU(server utility)、FPL(flow path length)、AR(accept rate)

当服务器mips超过其计算容量值时，将丢包。
实验情景：依次随机选择一条流，让其流量从tr突变为peak。
评估参数：
1.sum plrServers记录存在丢包情况的服务器数量。$cnt_ps$
2.单台服务器丢包率 $plr_k = 超出mips/其计算容量$
plr1 记录丢包服务器的平均丢包率。$plr = 总丢包率/cnt_ps$
plr2 记录总的丢包率。$plr = 总丢包率/总服务器数量$

1.plr.py 负责重放结果，输出数据

```console
python3 plr.py -c 1000 -k 20 -i ../output/result.txt -o ../output/plr.txt -s 10
或简写如下：
python3 plr.py
```

+ -c 指定生成的流量条数，默认1000条
+ -k 指定拓扑基于 k-阶胖树 拓扑，默认20
+ -i 指定读入文件名
+ -o 指定输出文件名
+ -s 指定随机数的起始随机种子

2.draw.py负责画图

```console
python3 draw.py
```

## 实验数据

使用20-阶胖树拓扑，5000条流量，共有2000台服务器，每台服务器计算能力为100000mips。

```shell
#!/bin/sh
# --- k=10 c=500 ---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 10 -o out500/traffic.txt
# MVSH
python3 mvsh.py -k 10 -i out500/traffic.txt -o out500/result_mvsh.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i out500/result_mvsh.txt -o out500/analysis_mvsh.txt
python3 plr.py -c 500 -k 10 -i out500/result_mvsh.txt -s 10 -o out500/plr_mvsh.txt
# 我的方案SVNFP
python3 svnfp.py -k 10 -i out500/traffic.txt -o out500/result_svnf.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i out500/result_svnf.txt -o out500/analysis_svnf.txt
python3 plr.py -c 500 -k 10 -i out500/result_svnf.txt -s 10 -o out500/plr_svnf.txt
# 对比方案CLBP
python3 clbp.py -k 10 -i out500/traffic.txt -o out500/result_clbp.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i out500/result_clbp.txt -o out500/analysis_clbp.txt
python3 plr.py -c 500 -k 10 -i out500/result_clbp.txt -s 10 -o out500/plr_clbp.txt
# 绘图
python3 draw.py -c 500
# --- k=10 c=1000 ---
# 生成流量
python3 traffic.py -c 1000 -k 10 -Tm 10 -al 2.1 -s 10 -o out1000/traffic.txt
# MVSH
python3 mvsh.py -k 10 -i out1000/traffic.txt -o out1000/result_mvsh.txt -n
python3 resultAnalysis.py -c 1000 -k 10 -i out1000/result_mvsh.txt -o out1000/analysis_mvsh.txt
python3 plr.py -c 1000 -k 10 -i out1000/result_mvsh.txt -s 10 -o out1000/plr_mvsh.txt
# 我的方案SVNFP
python3 svnfp.py -k 10 -i out1000/traffic.txt -o out1000/result_svnf.txt -n
python3 resultAnalysis.py -c 1000 -k 10 -i out1000/result_svnf.txt -o out1000/analysis_svnf.txt
python3 plr.py -c 1000 -k 10 -i out1000/result_svnf.txt -s 10 -o out1000/plr_svnf.txt
# 对比方案CLBP
python3 clbp.py -k 10 -i out1000/traffic.txt -o out1000/result_clbp.txt -n
python3 resultAnalysis.py -c 1000 -k 10 -i out1000/result_clbp.txt -o out1000/analysis_clbp.txt
python3 plr.py -c 1000 -k 10 -i out1000/result_clbp.txt -s 10 -o out1000/plr_clbp.txt
# 绘图
python3 draw.py -c 1000
```

## 实验结果

### k=10, c = 500

| 算法 | AR | FLP（跳数） | AVG SU |
| --- | --- | --- | --- |
| SVNFP | 74.1% | 25.994 | 75.089% |
| SVNFP-adv | 99.8% | 13.372 | 71.104% |
| CLBP | 75.7% | 5.142 | 72.944% |

![实验1](/results/shiyan1.png)

### k=10, c = 1000

| 算法 | AR | FLP（跳数） | AVG SU |
| --- | --- | --- | --- |
| SVNFP | 74.1% | 25.994 | 75.089% |
| SVNFP-adv | 64.5% | 9.592 | 67.375% |
| CLBP | 75.7% | 5.142 | 72.944% |

![实验2](/results/shiyan2.png)
