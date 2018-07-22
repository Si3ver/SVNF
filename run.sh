#!/bin/sh
# --- k=20 c=5000 ---
# 生成流量
python3 traffic.py -c 5000 -k 20 -Tm 10 -al 2.1 -s 10 -o output/traffic.txt
# 我的方案SVNFP
python3 svnfp.py -k 20 -i output/traffic.txt -o output/result_svnf.txt -n
python3 resultAnalysis.py -c 5000 -k 20 -i output/result_svnf.txt -o output/analysis_svnf.txt
python3 plr.py -c 5000 -k 20 -i output/result_svnf.txt -s 10 -o output/plr_svnf.txt
# 对比方案RNDP
python3 rndp.py -k 20 -i output/traffic.txt -o output/result_rndp.txt -s 20 -n
python3 resultAnalysis.py -c 5000 -k 20 -i output/result_rndp.txt -o output/analysis_rndp.txt
python3 plr.py -c 5000 -k 20 -i output/result_rndp.txt -s 10 -o output/plr_rndp.txt
# 对比方案CLBP
python3 clbp.py -k 20 -i output/traffic.txt -o output/result_clbp.txt -n
python3 resultAnalysis.py -c 5000 -k 20 -i output/result_clbp.txt -o output/analysis_clbp.txt
python3 plr.py -c 5000 -k 20 -i output/result_clbp.txt -s 10 -o output/plr_clbp.txt
# --- k=20 c=1000 ---
# 生成流量
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o output2/traffic.txt
# 我的方案SVNFP
python3 svnfp.py -k 20 -i output2/traffic.txt -o output2/result_svnf.txt -n
python3 resultAnalysis.py -c 1000 -k 20 -i output2/result_svnf.txt -o output2/analysis_svnf.txt
python3 plr.py -c 1000 -k 20 -i output2/result_svnf.txt -s 10 -o output2/plr_svnf.txt
# 对比方案RNDP
python3 rndp.py -k 20 -i output2/traffic.txt -o output2/result_rndp.txt -s 20 -n
python3 resultAnalysis.py -c 1000 -k 20 -i output2/result_rndp.txt -o output2/analysis_rndp.txt
python3 plr.py -c 1000 -k 20 -i output2/result_rndp.txt -s 10 -o output2/plr_rndp.txt
# 对比方案CLBP
python3 clbp.py -k 20 -i output2/traffic.txt -o output2/result_clbp.txt -n
python3 resultAnalysis.py -c 1000 -k 20 -i output2/result_clbp.txt -o output2/analysis_clbp.txt
python3 plr.py -c 1000 -k 20 -i output2/result_clbp.txt -s 10 -o output2/plr_clbp.txt
# --- k=20 c=10000 ---
# 生成流量
python3 traffic.py -c 10000 -k 20 -Tm 10 -al 2.1 -s 10 -o output2/traffic.txt
# 我的方案SVNFP
python3 svnfp.py -k 20 -i output2/traffic.txt -o output2/result_svnf.txt -n
python3 resultAnalysis.py -c 10000 -k 20 -i output2/result_svnf.txt -o output2/analysis_svnf.txt
python3 plr.py -c 10000 -k 20 -i output2/result_svnf.txt -s 10 -o output2/plr_svnf.txt
# 对比方案RNDP
python3 rndp.py -k 20 -i output2/traffic.txt -o output2/result_rndp.txt -s 20 -n
python3 resultAnalysis.py -c 10000 -k 20 -i output2/result_rndp.txt -o output2/analysis_rndp.txt
python3 plr.py -c 10000 -k 20 -i output2/result_rndp.txt -s 10 -o output2/plr_rndp.txt
# 对比方案CLBP
python3 clbp.py -k 20 -i output2/traffic.txt -o output2/result_clbp.txt -n
python3 resultAnalysis.py -c 10000 -k 20 -i output2/result_clbp.txt -o output2/analysis_clbp.txt
python3 plr.py -c 10000 -k 20 -i output2/result_clbp.txt -s 10 -o output2/plr_clbp.txt
# 绘图
python3 draw.py
