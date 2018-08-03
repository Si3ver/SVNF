# --- k=6 c=300 ---
# 生成流量
python3 traffic.py -c 300 -k 6 -Tm 10 -al 2.1 -s 10 -o debug/traffic.txt
# MVSH -- sVNFP
python3 mvsh.py -k 6 -i debug/traffic.txt -o debug/result_mvsh.txt -n
python3 resultAnalysis.py -c 300 -k 6 -i debug/result_mvsh.txt -o debug/analysis_mvsh.txt
python3 plr.py -c 300 -k 6 -i debug/result_mvsh.txt -s 10 -o debug/plr_mvsh.txt
# SVNFP -- sVNFP-adv
python3 svnfp.py -k 6 -i debug/traffic.txt -o debug/result_svnf.txt -n
python3 resultAnalysis.py -c 300 -k 6 -i debug/result_svnf.txt -o debug/analysis_svnf.txt
python3 plr.py -c 300 -k 6 -i debug/result_svnf.txt -s 10 -o debug/plr_svnf.txt
# CLBP
python3 clbp.py -k 6 -i debug/traffic.txt -o debug/result_clbp.txt -n
python3 resultAnalysis.py -c 300 -k 6 -i debug/result_clbp.txt -o debug/analysis_clbp.txt
python3 plr.py -c 300 -k 6 -i debug/result_clbp.txt -s 10 -o debug/plr_clbp.txt
# 绘图
python3 draw.py -c 300


| 算法       | AR      | FLP（跳数）| AVG SU  |
| ---       | ---     | ---       | ---     |
| SVNFP     | 58.667% | 18.233    | 74.763% |
| SVNFP-adv | 54.000% | 8.253     | 71.031% |
| CLBP      | 67.000% | 4.153     | 75.864% |

