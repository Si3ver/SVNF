# 实验

## 实验0 (debug)

取k=6, 共54台服务器  编号为[45,98]。

6个pod         [45-98]
每个pod3个tor   [45-53] ...
每个tor3台serv  [45-47] [48-50] [51-53] ...

```shell
# --- k=6 c=100 s=30 ---
# 生成流量
python3 traffic.py -c 100 -k 6 -Tm 10 -al 2.1 -s 20 -o debug/traffic-c100s20.txt
python3 mvsh.py -k 6 -i debug/traffic-c100s20.txt -o debug/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug/result_mvsh-c100s20.txt -o debug/analysis_mvsh-c100s20.txt
python3 plr.py -c 100 -k 6 -i debug/result_mvsh-c100s20.txt -s 30 -o debug/plr_mvsh-c100s20.txt -a mvsh
python3 svnfp.py -k 6 -i debug/traffic-c100s20.txt -o debug/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug/result_svnf-c100s20.txt -o debug/analysis_svnf-c100s20.txt
python3 plr.py -c 100 -k 6 -i debug/result_svnf-c100s20.txt -s 30 -o debug/plr_svnf-c100s20.txt -a svnf
python3 clbp.py -k 6 -i debug/traffic-c100s20.txt -o debug/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 100 -k 6 -i debug/result_clbp-c100s20.txt -o debug/analysis_clbp-c100s20.txt
python3 plr.py -c 100 -k 6 -i debug/result_clbp-c100s20.txt -s 30 -o debug/plr_clbp-c100s20.txt -a clbp
python3 draw.py -c 100 -s 30
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  4.803     |52.475%  |
| sVNFP-adv | 100%  |  2.404     |60.219%  |
| CLBP      | 100%  |  1.908     |88.552%  |

## 实验1   (exp: 1~2)

```shell
# --- k=10 c=500 s=30 ---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 1
python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 1
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 1

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 1
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 1

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 1
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 1

python3 draw.py = -x 1

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
# --- k=10 c=500 s=30 ---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 2

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 2
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 2

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 2
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 2

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 2
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 2

python3 draw.py -c 500 -s 30 -x 2
```

## 实验3 (exp=3~4)

```console
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 3

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 3

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 3

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 3

python3 draw.py -c 500 -s 30 -x 3
```

```console
# 100组实验
run 1000 python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 2 >> test1.txt
run 1000 python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 2 >> test2.txt
run 1000 python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 2 >> test3.txt
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

<!-- ## 实验3 (exp: 一半1\~2，一半3\~4)

```shell
# --- k=10 c=500 s=30 ---
# 生成流量
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan3/traffic-c100s20.txt -x 3
python3 mvsh.py -k 10 -i shiyan3/traffic-c100s20.txt -o shiyan3/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan3/result_mvsh-c100s20.txt -o shiyan3/analysis_mvsh-c100s20.txt
python3 plr.py -c 500 -k 10 -i shiyan3/result_mvsh-c100s20.txt -s 30 -o shiyan3/plr_mvsh-c100s20.txt -a mvsh -x 3
python3 svnfp.py -k 10 -i shiyan3/traffic-c100s20.txt -o shiyan3/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan3/result_svnf-c100s20.txt -o shiyan3/analysis_svnf-c100s20.txt
python3 plr.py -c 500 -k 10 -i shiyan3/result_svnf-c100s20.txt -s 30 -o shiyan3/plr_svnf-c100s20.txt -a svnf -x 3
python3 clbp.py -k 10 -i shiyan3/traffic-c100s20.txt -o shiyan3/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan3/result_clbp-c100s20.txt -o shiyan3/analysis_clbp-c100s20.txt
python3 plr.py -c 500 -k 10 -i shiyan3/result_clbp-c100s20.txt -s 30 -o shiyan3/plr_clbp-c100s20.txt -a clbp -x 3
python3 draw.py -c 500 -s 30 -x 3
```

| 算法       | AR    | FLP（跳数） | AVG SU  |
| ---       | ---   | ---        | ---     |
| sVNFP     | 100%  |  5.121     |47.066%  |
| sVNFP-adv | 100%  |  2.410     |47.066%  |
| CLBP      | 100%  |  2.164     |85.265%  |

![plr](./results/plr_c500s30-3.pdf)
![bsr](results/bsr_c500s30-3.pdf)
![su](results/su_c500s30-3.pdf) -->

python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 3

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 3

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 3

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 3
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 3


-------
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 4

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 4
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 4

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 4
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 4

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 4
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 4

```console
-------
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 5

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 5
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 5

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 5
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 5

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 5
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 5

-------
python3 traffic.py -c 500 -k 10 -Tm 10 -al 2.1 -s 20 -o shiyan1/traffic-c100s20.txt -x 6

python3 mvsh.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_mvsh-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -o shiyan1/analysis_mvsh-c100s20.txt -a mvsh -x 6
python3 plr.py -c 500 -k 10 -i shiyan1/result_mvsh-c100s20.txt -s 30 -o shiyan1/plr_mvsh-c100s20.txt -a mvsh -x 6

python3 svnfp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_svnf-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -o shiyan1/analysis_svnf-c100s20.txt  -a svnf -x 6
python3 plr.py -c 500 -k 10 -i shiyan1/result_svnf-c100s20.txt -s 30 -o shiyan1/plr_svnf-c100s20.txt -a svnf -x 6

python3 clbp.py -k 10 -i shiyan1/traffic-c100s20.txt -o shiyan1/result_clbp-c100s20.txt -n
python3 resultAnalysis.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -o shiyan1/analysis_clbp-c100s20.txt -a clbp -x 6
python3 plr.py -c 500 -k 10 -i shiyan1/result_clbp-c100s20.txt -s 30 -o shiyan1/plr_clbp-c100s20.txt -a clbp -x 6
```