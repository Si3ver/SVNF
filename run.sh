# --- k=20 c=5000 ---
# 生成流量
python3 traffic.py -c 5000 -k 20 -Tm 10 -al 2.1 -s 10 -o output1/traffic.txt
# MVSH
python3 mvsh.py -k 20 -i output1/traffic.txt -o output1/result_mvsh.txt -n
python3 resultAnalysis.py -c 5000 -k 20 -i output1/result_mvsh.txt -o output1/analysis_mvsh.txt
python3 plr.py -c 5000 -k 20 -i output1/result_mvsh.txt -s 10 -o output1/plr_mvsh.txt
# 我的方案SVNFP
python3 svnfp.py -k 20 -i output1/traffic.txt -o output1/result_svnf.txt -n
python3 resultAnalysis.py -c 5000 -k 20 -i output1/result_svnf.txt -o output1/analysis_svnf.txt
python3 plr.py -c 5000 -k 20 -i output1/result_svnf.txt -s 10 -o output1/plr_svnf.txt
# 对比方案RNDP
python3 rndp.py -k 20 -i output1/traffic.txt -o output1/result_rndp.txt -s 20 -n
python3 resultAnalysis.py -c 5000 -k 20 -i output1/result_rndp.txt -o output1/analysis_rndp.txt
python3 plr.py -c 5000 -k 20 -i output1/result_rndp.txt -s 10 -o output1/plr_rndp.txt
# 对比方案CLBP
python3 clbp.py -k 20 -i output1/traffic.txt -o output1/result_clbp.txt -n
python3 resultAnalysis.py -c 5000 -k 20 -i output1/result_clbp.txt -o output1/analysis_clbp.txt
python3 plr.py -c 5000 -k 20 -i output1/result_clbp.txt -s 10 -o output1/plr_clbp.txt


# --- k=20 c=1000 ---
# 生成流量
python3 traffic.py -c 1000 -k 20 -Tm 10 -al 2.1 -s 10 -o output2/traffic.txt

# 我的方案MVSH
python3 mvsh.py -k 20 -i output2/traffic.txt -o output2/result_mvsh.txt -n
python3 resultAnalysis.py -c 1000 -k 20 -i output2/result_mvsh.txt -o output2/analysis_mvsh.txt
python3 plr.py -c 1000 -k 20 -i output2/result_mvsh.txt -s 10 -o output2/plr_mvsh.txt
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
python3 traffic.py -c 10000 -k 20 -Tm 10 -al 2.1 -s 10 -o output3/traffic.txt
# MVSH
python3 mvsh.py -k 20 -i output3/traffic.txt -o output3/result_mvsh.txt -n
python3 resultAnalysis.py -c 10000 -k 20 -i output3/result_mvsh.txt -o output3/analysis_mvsh.txt
python3 plr.py -c 10000 -k 20 -i output3/result_mvsh.txt -s 10 -o output3/plr_mvsh.txt
# 我的方案SVNFP
python3 svnfp.py -k 20 -i output3/traffic.txt -o output3/result_svnf.txt -n
python3 resultAnalysis.py -c 10000 -k 20 -i output3/result_svnf.txt -o output3/analysis_svnf.txt
python3 plr.py -c 10000 -k 20 -i output3/result_svnf.txt -s 10 -o output3/plr_svnf.txt
# 对比方案RNDP
python3 rndp.py -k 20 -i output3/traffic.txt -o output3/result_rndp.txt -s 20 -n
python3 resultAnalysis.py -c 10000 -k 20 -i output3/result_rndp.txt -o output3/analysis_rndp.txt
python3 plr.py -c 10000 -k 20 -i output3/result_rndp.txt -s 10 -o output3/plr_rndp.txt
# 对比方案CLBP
python3 clbp.py -k 20 -i output3/traffic.txt -o output3/result_clbp.txt -n
python3 resultAnalysis.py -c 10000 -k 20 -i output3/result_clbp.txt -o output3/analysis_clbp.txt
python3 plr.py -c 10000 -k 20 -i output3/result_clbp.txt -s 10 -o output3/plr_clbp.txt
# 绘图
python3 draw.py
# MVSH




python3 mvsh.py -k 20 -i output1/traffic.txt -o output1/result_mvsh.txt -n

