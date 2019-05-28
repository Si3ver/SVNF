# 实验

## 实验0 (debug)

取k=6, 共54台服务器  编号为[45,98]。

6个pod         [45-98]
每个pod3个tor   [45-53] ...
每个tor3台serv  [45-47] [48-50] [51-53] ...

```shell
# --- k=6 c=100 s=30 ---
chmod a+x init.sh clear.sh
./clear.sh expri0
./init.sh expri0
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
# --- k=10 c=500 s=30 x=1---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 1
python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 1
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 1

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 1
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 1

python3 clbp2.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 1
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 1

python3 draw.py -c 500 -s 30 -x 1
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  5.090     |49.697%  |
| sVNFP-adv | 100%  |  2.370     |49.697%  |
| CLBP      | 100%  |  2.082     |92.032%  |

[plr](./results/plr_c500s30-1.pdf)
[bsr](./results/bsr_c500s30-1.pdf)
[su](./results/su_c500s30-1.pdf)
[cdf](cdf_su0.2-1.pdf)
[cdf](cdf_su0.5-1.pdf)
[cdf](cdf_su0.7-1.pdf)

## 实验2 (exp: 2~3)

```shell
# --- k=10 c=500 s=30 x=2---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 2

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 2
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 2

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 2
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 2

python3 clbp2.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 2
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 2

python3 draw.py -c 500 -s 30 -x 2
```

## 实验3 (exp=3~4)

```console
# --- k=10 c=500 s=30 x=3---
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 3
python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 3

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 3

python3 clbp2.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 3

python3 draw.py -c 500 -s 30 -x 3
```

```console
# 100组实验
run 100 python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 3 >> test1.txt
run 100 python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 3 >> test2.txt
run 100 python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 3 >> test3.txt
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  5.119     |49.697%  |
| sVNFP-adv | 100%  |  2.371     |49.697%  |
| CLBP      | 100%  |  2.205     |79.136%  |

[plr](results/plr_c500s30-2.pdf)
[bsr](results/bsr_c500s30-2.pdf)
[su](results/su_c500s30-2.pdf)
[cdf](cdf_su0.2-2.pdf)
[cdf](cdf_su0.5-2.pdf)
[cdf](cdf_su0.7-2.pdf)

```shell
# -------x = 4
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 4

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 4
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 4

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 4
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 4

python3 clbp2.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 4
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 4
# ------ x=5
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 5

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 5
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 5

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 5
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 5

python3 clbp2.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 5
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 5

# ------- x=6
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 6

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 6
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 6

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 6
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 6

python3 clbp2.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 6
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 6
```

结果详见我的论文（已投稿IPCCC，等待评审中...）:

W.  Zhou,  Y.  Yang,  and  M.  Xu,  “Accommodating  dynamic  trafficimmediately:  a  VNF  placement  approach,”  in2018 IEEE 37th In-ternational Performance Computing and Communications Conference(IPCCC) (IPCCC 2018), Orlando, USA, Nov. 2018.

BibTex

@INPROCEEDINGS{Zhou,
AUTHOR="Weilin Zhou and Yuan Yang and Mingwei Xu",
TITLE="Accommodating Dynamic Traffic Immediately: a {VNF} Placement Approach",
BOOKTITLE="2018 IEEE 37th International Performance Computing and Communications
Conference (IPCCC) (IPCCC 2018)",
ADDRESS="Orlando, USA",
DAYS=17,
MONTH=nov,
YEAR=2018,
KEYWORDS="NFV; Dynamic Traffic; VNF placement; network scalability; heuristic
algorithm; heuristic algorithm",
ABSTRACT="Network Function Virtualization (NFV) offers a new way to design, deploy
and manage network services as it provides operator with agility and
flexibility of network service deployment. While NFV orchestration becomes
quite complicated when consider dynamic traffic variability in real network
scenario. To fit in the situation of traffic rate change and add
scalability to NFV deployment, we raise a scalable virtual network function
(VNF) placement algorithm. In this paper, we first quantify scalability and
identify the factors that undermine scalability. Furthermore, for improve
network scalability and reduce the flow path length, we put forward a
heuristic algorithm named SVNFP. We evaluate our approach consider packet
loss rate, bad server rate, server utility, flow path length and traffic
accept rate. The simulation shows that our aproach effectively improve
network scalability and reduce flow path length."
}