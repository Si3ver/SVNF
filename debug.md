# 测试(小规模实验)

取k=6, 共54台服务器  编号为[45,98]。

6个pod         [45-98]
每个pod3个tor   [45-53] ...
每个tor3台serv  [45-47] [48-50] [51-53] ...

## 实验1：

```shell
# --- k=6 c=10 s=20 ---
# 生成流量
python3 traffic.py -c 10 -k 6 -Tm 10 -al 2.1 -s 20 -o debug/traffic-c10s20.txt
python3 mvsh.py -k 6 -i debug/traffic-c10s20.txt -o debug/result_mvsh-c10s20.txt -n
python3 resultAnalysis.py -c 10 -k 6 -i debug/result_mvsh-c10s20.txt -o debug/analysis_mvsh-c10s20.txt
python3 plr.py -c 10 -k 6 -i debug/result_mvsh-c10s20.txt -s 20 -o debug/plr_mvsh-c10s20.txt -a mvsh
python3 svnfp.py -k 6 -i debug/traffic-c10s20.txt -o debug/result_svnf-c10s20.txt -n
python3 resultAnalysis.py -c 10 -k 6 -i debug/result_svnf-c10s20.txt -o debug/analysis_svnf-c10s20.txt
python3 plr.py -c 10 -k 6 -i debug/result_svnf-c10s20.txt -s 20 -o debug/plr_svnf-c10s20.txt -a svnf
python3 clbp.py -k 6 -i debug/traffic-c10s20.txt -o debug/result_clbp-c10s20.txt -n
python3 resultAnalysis.py -c 10 -k 6 -i debug/result_clbp-c10s20.txt -o debug/analysis_clbp-c10s20.txt
python3 plr.py -c 10 -k 6 -i debug/result_clbp-c10s20.txt -s 20 -o debug/plr_clbp-c10s20.txt -a clbp
python3 draw.py -c 10 -s 20
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| SVNFP     | 100%  |  3.803     |17.547%  |
| SVNFP-adv | 100%  |  2.025     | 4.094%  |
| CLBP      | 100%  |  1.271     |13.647%  |

![实验1](../results/c10.png)

## 实验2

```shell
# --- k=6 c=50 s=20 ---
# 生成流量
python3 traffic.py -c 50 -k 6 -Tm 10 -al 2.1 -s 20 -o debug/traffic-c50s20.txt
python3 mvsh.py -k 6 -i debug/traffic-c50s20.txt -o debug/result_mvsh-c50s20.txt -n
python3 resultAnalysis.py -c 50 -k 6 -i debug/result_mvsh-c50s20.txt -o debug/analysis_mvsh-c50s20.txt
python3 plr.py -c 50 -k 6 -i debug/result_mvsh-c50s20.txt -s 20 -o debug/plr_mvsh-c50s20.txt -a mvsh
python3 svnfp.py -k 6 -i debug/traffic-c50s20.txt -o debug/result_svnf-c50s20.txt -n
python3 resultAnalysis.py -c 50 -k 6 -i debug/result_svnf-c50s20.txt -o debug/analysis_svnf-c50s20.txt
python3 plr.py -c 50 -k 6 -i debug/result_svnf-c50s20.txt -s 20 -o debug/plr_svnf-c50s20.txt -a svnf
python3 clbp.py -k 6 -i debug/traffic-c50s20.txt -o debug/result_clbp-c50s20.txt -n
python3 resultAnalysis.py -c 50 -k 6 -i debug/result_clbp-c50s20.txt -o debug/analysis_clbp-c50s20.txt
python3 plr.py -c 50 -k 6 -i debug/result_clbp-c50s20.txt -s 20 -o debug/plr_clbp-c50s20.txt -a clbp
python3 draw.py -c 50 -s 20
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| SVNFP     | 100%  |  5.094     |26.127%  |
| SVNFP-adv | 100%  |  2.144     |26.127%  |
| CLBP      | 100%  |  1.078     |37.128%  |

![实验2](../results/c50.png)

## 实验3

```shell
# --- k=6 c=100 s=20 ---
# 生成流量
python3 traffic.py -c 100 -k 6 -Tm 10 -al 2.1 -s 20 -o debug/traffic-c100s20.txt
python3 mvsh.py -k 6 -i debug/traffic-c100s20.txt -o debug/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug/result_mvsh-c100s20.txt -o debug/analysis_mvsh-c100s20.txt
python3 plr.py -c 100 -k 6 -i debug/result_mvsh-c100s20.txt -s 20 -o debug/plr_mvsh-c100s20.txt -a mvsh
python3 svnfp.py -k 6 -i debug/traffic-c100s20.txt -o debug/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug/result_svnf-c100s20.txt -o debug/analysis_svnf-c100s20.txt
python3 plr.py -c 100 -k 6 -i debug/result_svnf-c100s20.txt -s 20 -o debug/plr_svnf-c100s20.txt -a svnf
python3 clbp.py -k 6 -i debug/traffic-c100s20.txt -o debug/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug/result_clbp-c100s20.txt -o debug/analysis_clbp-c100s20.txt
python3 plr.py -c 100 -k 6 -i debug/result_clbp-c100s20.txt -s 20 -o debug/plr_clbp-c100s20.txt -a clbp
python3 draw.py -c 100 -s 20
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| SVNFP     | 100%  |  5.009     |46.511%  |
| SVNFP-adv | 100%  |  2.181     |46.511%  |
| CLBP      | 100%  |  1.282     |50.232%  |

![实验3](../results/c100.png)

```shell
# --- k=6 c=100 s=20 ---
python3 traffic.py -c 100 -k 6 -Tm 10 -al 2.1 -s 20 -o debug100-3/traffic.txt
python3 mvsh.py -k 6 -i debug100-3/traffic.txt -o debug100-3/result_mvsh.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-3/result_mvsh.txt -o debug100-3/analysis_mvsh.txt
python3 plr.py -c 100 -k 6 -i debug100-3/result_mvsh.txt -s 20 -o debug100-3/plr_mvsh.txt
python3 svnfp.py -k 6 -i debug100-3/traffic.txt -o debug100-3/result_svnf.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-3/result_svnf.txt -o debug100-3/analysis_svnf.txt
python3 plr.py -c 100 -k 6 -i debug100-3/result_svnf.txt -s 20 -o debug100-3/plr_svnf.txt
python3 clbp.py -k 6 -i debug100-3/traffic.txt -o debug100-3/result_clbp.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-3/result_clbp.txt -o debug100-3/analysis_clbp.txt
python3 plr.py -c 100 -k 6 -i debug100-3/result_clbp.txt -s 20 -o debug100-3/plr_clbp.txt
python3 draw2.py -c 100
```

```shell
# --- k=6 c=100 s=20 MVSH1 ---
python3 traffic.py -c 100 -k 6 -Tm 10 -al 2.1 -s 20 -o debug100-3/traffic.txt
python3 mvsh1.py -k 6 -i debug100-3/traffic.txt -o debug100-3/result_mvsh.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-3/result_mvsh.txt -o debug100-3/analysis_mvsh.txt
python3 plr.py -c 100 -k 6 -i debug100-3/result_mvsh.txt -s 20 -o debug100-3/plr_mvsh.txt
python3 svnfp.py -k 6 -i debug100-3/traffic.txt -o debug100-3/result_svnf.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-3/result_svnf.txt -o debug100-3/analysis_svnf.txt
python3 plr.py -c 100 -k 6 -i debug100-3/result_svnf.txt -s 20 -o debug100-3/plr_svnf.txt
python3 clbp.py -k 6 -i debug100-3/traffic.txt -o debug100-3/result_clbp.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-3/result_clbp.txt -o debug100-3/analysis_clbp.txt
python3 plr.py -c 100 -k 6 -i debug100-3/result_clbp.txt -s 20 -o debug100-3/plr_clbp.txt
python3 draw2-mvsh1.py -c 100
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| SVNFP     |  98%  |  4.865     |43.700%  |
| SVNFP-adv |  99%  |  2.173     |43.160%  |
| CLBP      | 100%  |  1.398     |52.211%  |

![实验3-2](../results/c100-2.png)

```shell
# --- k=6 c=100 s=30 ---
python3 traffic.py -c 100 -k 6 -Tm 10 -al 2.1 -s 30 -o debug100-2/traffic.txt
python3 mvsh.py -k 6 -i debug100-2/traffic.txt -o debug100-2/result_mvsh.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-2/result_mvsh.txt -o debug100-2/analysis_mvsh.txt
python3 plr.py -c 100 -k 6 -i debug100-2/result_mvsh.txt -s 30 -o debug100-2/plr_mvsh.txt
python3 svnfp.py -k 6 -i debug100-2/traffic.txt -o debug100-2/result_svnf.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-2/result_svnf.txt -o debug100-2/analysis_svnf.txt
python3 plr.py -c 100 -k 6 -i debug100-2/result_svnf.txt -s 30 -o debug100-2/plr_svnf.txt
python3 clbp.py -k 6 -i debug100-2/traffic.txt -o debug100-2/result_clbp.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug100-2/result_clbp.txt -o debug100-2/analysis_clbp.txt
python3 plr.py -c 100 -k 6 -i debug100-2/result_clbp.txt -s 30 -o debug100-2/plr_clbp.txt
python3 draw3.py -c 100
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| SVNFP     |  98%  |  4.865     |43.700%  |
| SVNFP-adv |  99%  |  2.173     |43.160%  |
| CLBP      | 100%  |  1.398     |52.211%  |

![实验3-2](../results/c100-2.png)

## 实验4

```shell
# --- k=6 c=200 s=20 ---
# 生成流量
python3 traffic.py -c 200 -k 6 -Tm 10 -al 2.1 -s 20 -o debug/traffic-c200s20.txt
python3 mvsh.py -k 6 -i debug/traffic-c200s20.txt -o debug/result_mvsh-c200s20.txt -n
python3 resultAnalysis.py -c 200 -k 6 -i debug/result_mvsh-c200s20.txt -o debug/analysis_mvsh-c200s20.txt
python3 plr.py -c 200 -k 6 -i debug/result_mvsh-c200s20.txt -s 20 -o debug/plr_mvsh-c200s20.txt -a mvsh
python3 svnfp.py -k 6 -i debug/traffic-c200s20.txt -o debug/result_svnf-c200s20.txt -n
python3 resultAnalysis.py -c 200 -k 6 -i debug/result_svnf-c200s20.txt -o debug/analysis_svnf-c200s20.txt
python3 plr.py -c 200 -k 6 -i debug/result_svnf-c200s20.txt -s 20 -o debug/plr_svnf-c200s20.txt -a svnf
python3 clbp.py -k 6 -i debug/traffic-c200s20.txt -o debug/result_clbp-c200s20.txt -n
python3 resultAnalysis.py -c 200 -k 6 -i debug/result_clbp-c200s20.txt -o debug/analysis_clbp-c200s20.txt
python3 plr.py -c 200 -k 6 -i debug/result_clbp-c200s20.txt -s 20 -o debug/plr_clbp-c200s20.txt -a clbp
python3 draw.py -c 200 -s 20
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| SVNFP     |  87%  |  4.579     |74.537%  |
| SVNFP-adv |  80%  |  2.021     |70.888%  |
| CLBP      |75.5%  |  1.275     |72.735%  |

![实验4](../results/c200.png)
