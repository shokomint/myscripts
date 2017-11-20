# myscripts
#
# 使い方
########
#
# 衆院／参院の質問1の質問と答弁を取得する。出力先はDownload配下。
# ./test_QandA.sh shu|san -d 1
# 
# 衆院や参院の質問や答弁を要約したら、log_done.json に番号を記録する。
# 
# 衆院の質問や回答でアップされてるもののうち、まだ要約していないものを一覧にする。出力先はSTDOUT。
# python3 ./shuin_QandA.py -ul
#
# 参院バージョン
# python3 ./sanin_QandA.py -ul
