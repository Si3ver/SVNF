# 实验

## 实验0 (debug)

取k=6, 共54台服务器  编号为[45,98]。

6个pod         [45-98]
每个pod3个tor   [45-53] ...
每个tor3台serv  [45-47] [48-50] [51-53] ...

```shell
# 初始化expri0所需目录结构
chmod a+x init.sh clear.sh
./clear.sh expri0
./init.sh expri0
# --- k=6 c=100 s=30 ---
# 生成流量
python3 traffic.py -c 100 -k 6 -Tm 10 -al 2.1 -s 20 -o expri0/traffic/traffic-c100s20.txt #产生流量

python3 mvsh.py -k 6 -i expri0/traffic/traffic-c100s20.txt -o expri0/placeResult/result_mvsh-c100s20.txt -n #VNF放置算法，输出放置结果
python3 resultAnalysis.py -c 100 -k 6 -i expri0/placeResult/result_mvsh-c100s20.txt -o expri0/staticAnalysis/analysis_mvsh-c100s20.txt #输出静态分析结果
python3 plr.py -c 100 -k 6 -i expri0/placeResult/result_mvsh-c100s20.txt -s 30 -o expri0/evaluation/plr_mvsh-c100s20.txt -a mvsh #输出压测结果

python3 svnfp.py -k 6 -i expri0/traffic/traffic-c100s20.txt -o expri0/placeResult/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i expri0/placeResult/result_svnf-c100s20.txt -o expri0/staticAnalysis/analysis_svnf-c100s20.txt
python3 plr.py -c 100 -k 6 -i expri0/placeResult/result_svnf-c100s20.txt -s 30 -o expri0/evaluation/plr_svnf-c100s20.txt -a svnf

python3 clbp2.py -k 6 -i expri0/traffic/traffic-c100s20.txt -o expri0/placeResult/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i expri0/placeResult/result_clbp-c100s20.txt -o expri0/staticAnalysis/analysis_clbp-c100s20.txt
python3 plr.py -c 100 -k 6 -i expri0/placeResult/result_clbp-c100s20.txt -s 30 -o expri0/evaluation/plr_clbp-c100s20.txt -a clbp

python3 draw.py -c 100 -s 30 -x 0
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  4.803     |52.475%  |
| sVNFP-adv | 100%  |  2.404     |60.219%  |
| CLBP      | 100%  |  1.908     |88.552%  |

## 实验1   (exp: 1~2)

```shell
# 初始化expri1所需目录结构
chmod a+x init.sh clear.sh
./clear.sh expri1
./init.sh expri1
# --- k=10 c=500 s=30 x=1---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o expri1/traffic/traffic-c100s20.txt -x 1

python3 mvsh.py -k 10 -i expri1/traffic/traffic-c100s20.txt -o expri1/placeResult/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri1/placeResult/result_mvsh-c100s20.txt -o expri1/staticAnalysis/analysis_mvsh-c100s20.txt -a mvsh -x 1
python3 plr.py -c 500 -k 10 -i expri1/placeResult/result_mvsh-c100s20.txt -s 30 -o expri1/evaluation/plr_mvsh-c100s20.txt -a mvsh -x 1

python3 svnfp.py -k 10 -i expri1/traffic-c100s20.txt -o expri1/placeResult/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri1/placeResult/result_svnf-c100s20.txt -o expri1/staticAnalysis/analysis_svnf-c100s20.txt  -a svnf -x 1
python3 plr.py -c 500 -k 10 -i expri1/placeResult/result_svnf-c100s20.txt -s 30 -o expri1/evaluation/plr_svnf-c100s20.txt -a svnf -x 1

python3 clbp2.py -k 10 -i expri1/traffic-c100s20.txt -o expri1/placeResult/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri1/placeResult/result_clbp-c100s20.txt -o expri1/staticAnalysis/analysis_clbp-c100s20.txt -a clbp -x 1
python3 plr.py -c 500 -k 10 -i expri1/placeResult/result_clbp-c100s20.txt -s 30 -o expri1/evaluation/plr_clbp-c100s20.txt -a clbp -x 1

python3 draw.py -c 500 -s 30 -x 1
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  5.090     |49.697%  |
| sVNFP-adv | 100%  |  2.370     |49.697%  |
| CLBP      | 100%  |  2.082     |92.032%  |

## 实验2 (exp: 2~3)

```shell
# 初始化expri2所需目录结构
chmod a+x init.sh clear.sh
./clear.sh expri2
./init.sh expri2
# --- k=10 c=500 s=30 x=2---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o expri2/traffic/traffic-c100s20.txt -x 2

python3 mvsh.py -k 10 -i expri2/traffic/traffic-c100s20.txt -o expri2/placeResult/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri2/placeResult/result_mvsh-c100s20.txt -o expri2/staticAnalysis/analysis_mvsh-c100s20.txt -a mvsh -x 2
python3 plr.py -c 500 -k 10 -i expri2/placeResult/result_mvsh-c100s20.txt -s 30 -o expri2/evaluation/plr_mvsh-c100s20.txt -a mvsh -x 2

python3 svnfp.py -k 10 -i expri2/traffic-c100s20.txt -o expri2/placeResult/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri2/placeResult/result_svnf-c100s20.txt -o expri2/staticAnalysis/analysis_svnf-c100s20.txt  -a svnf -x 2
python3 plr.py -c 500 -k 10 -i expri2/placeResult/result_svnf-c100s20.txt -s 30 -o expri2/evaluation/plr_svnf-c100s20.txt -a svnf -x 2

python3 clbp2.py -k 10 -i expri2/traffic-c100s20.txt -o expri2/placeResult/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri2/placeResult/result_clbp-c100s20.txt -o expri2/staticAnalysis/analysis_clbp-c100s20.txt -a clbp -x 2
python3 plr.py -c 500 -k 10 -i expri2/placeResult/result_clbp-c100s20.txt -s 30 -o expri2/evaluation/plr_clbp-c100s20.txt -a clbp -x 2

python3 draw.py -c 500 -s 30 -x 2
```

## 实验3 (exp=3~4)

```shell
# 初始化expri3所需目录结构
chmod a+x init.sh clear.sh
./clear.sh expri3
./init.sh expri3
# 路径需要按照实验0修改！
# --- k=10 c=500 s=30 x=3---
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o expri3/traffic/traffic-c100s20.txt -x 3

python3 mvsh.py -k 10 -i expri3/traffic/traffic-c100s20.txt -o expri3/placeResult/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri3/placeResult/result_mvsh-c100s20.txt -o expri3/staticAnalysis/analysis_mvsh-c100s20.txt -a mvsh -x 3
python3 plr.py -c 500 -k 10 -i expri3/placeResult/result_mvsh-c100s20.txt -s 30 -o expri3/evaluation/plr_mvsh-c100s20.txt -a mvsh -x 3

python3 svnfp.py -k 10 -i expri3/traffic-c100s20.txt -o expri3/placeResult/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri3/placeResult/result_svnf-c100s20.txt -o expri3/staticAnalysis/analysis_svnf-c100s20.txt  -a svnf -x 3
python3 plr.py -c 500 -k 10 -i expri3/placeResult/result_svnf-c100s20.txt -s 30 -o expri3/evaluation/plr_svnf-c100s20.txt -a svnf -x 3

python3 clbp2.py -k 10 -i expri3/traffic-c100s20.txt -o expri3/placeResult/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i expri3/placeResult/result_clbp-c100s20.txt -o expri3/staticAnalysis/analysis_clbp-c100s20.txt -a clbp -x 3
python3 plr.py -c 500 -k 10 -i expri3/placeResult/result_clbp-c100s20.txt -s 30 -o expri3/evaluation/plr_clbp-c100s20.txt -a clbp -x 3

python3 draw.py -c 500 -s 30 -x 3
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  5.119     |49.697%  |
| sVNFP-adv | 100%  |  2.371     |49.697%  |
| CLBP      | 100%  |  2.205     |79.136%  |

## 100组实验

```console
# 100组实验
run 100 python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 3 >> test1.txt
run 100 python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 3 >> test2.txt
run 100 python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 3 >> test3.txt
```

结果详见我的论文（ICC已录用）: W.  Zhou,  Y.  Yang,  and  M.  Xu, Hao Chen,  “Accommodating  dynamic  trafficimmediately:  a  VNF  placement  approach,”.
