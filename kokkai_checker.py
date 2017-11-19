
# 国会回次選択
home_shuin = "http://kokkai.ndl.go.jp/SENTAKU/syugiin/195/mainb.html"
home_sanin = "http://kokkai.ndl.go.jp/SENTAKU/sangiin/195/mainb.html"
home_ryoin = ""
root_shuin = "http://kokkai.ndl.go.jp/SENTAKU/syugiin/195/"
root_sanin = "http://kokkai.ndl.go.jp/SENTAKU/sangiin/195/"
root_ryoin = ""

file_committee = "/Users/shoko/Develop/myscripts/committee.json"

import requests
import re
import urllib
from html.parser import HTMLParser
from argparse import ArgumentParser
import json
import codecs

class CommitteeList(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.clist = []
		self.clist_flg = False
	
	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)

		if tag == "a":
			self.clist.append({})
			self.clist[-1].update({"url":attrs["href"]})
			self.clist_flg = True
	
	def handle_data(self, data):
		if self.clist_flg == True:
			self.clist[-1].update({"name":data})
			self.clist_flg = False


# コマンドライン引数を設定
arg_parser = ArgumentParser()
arg_parser.add_argument("--init", action="store_true", help="obtain committee lists")
args = arg_parser.parse_args()

if args.init:

	if home_shuin != "":
		shuin_url = requests.get(home_shuin)
		shuin_list = CommitteeList()
		shuin_list.feed(shuin_url.text)
		shuin_list.close()
		shuin_url.close()
	
	if home_sanin != "":
		sanin_url = requests.get(home_sanin)
		sanin_list = CommitteeList()
		sanin_list.feed(sanin_url.text)
		sanin_list.close()
		sanin_url.close()

	if home_ryoin != "":
		ryoin_url = requests.get(home_ryoin)
		ryoin_list = CommitteeList()
		ryoin_list.feed(sanin_url.text)
		ryoin_list.close()
		ryoin_url.close()

	f = codecs.open(file_committee, "w", "utf-8")

	if home_ryoin != "":
		json.dump([{"shuin": shuin_list.clist},{"sanin": sanin_list.clist}, {"ryoin": ryoin_list.clist}],f, ensure_ascii=False)
	else:
		json.dump([{"shuin": shuin_list.clist},{"sanin": sanin_list.clist}],f, ensure_ascii=False)
	

	f.close()

