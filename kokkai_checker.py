ENCODE = "sjis"

# 国会回次選択
HOME_SHUIN = "http://kokkai.ndl.go.jp/SENTAKU/syugiin/195/mainb.html"
HOME_SANIN = "http://kokkai.ndl.go.jp/SENTAKU/sangiin/195/mainb.html"
HOME_RYOIN = ""
ROOT_SHUIN = "http://kokkai.ndl.go.jp/SENTAKU/syugiin/195/"
ROOT_SANIN = "http://kokkai.ndl.go.jp/SENTAKU/sangiin/195/"
ROOT_RYOIN = ""

FILE_COMMITTEE = "/Users/shoko/Develop/myscripts/committee.json"

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

	def print(self):
		print(self.clist)
			
class CommitteeFile():
	def __init__(self, ktype, homepage, json_data):
		if homepage != "":
			url =requests.get(homepage)
			url.encoding = ENCODE
			klist = CommitteeList()
			klist.feed(url.text)
			klist.close()
			url.close()
			for i in range(len(klist.clist)):
				klist.clist[i].update({"kaiki":[]})
				json_data.update({ktype:klist.clist})


# 各委員会のページへアクセスし、既にアップされてる議事録番号を取得する。
class MinutesList():
	def __init__(self, ktype, root_url, json_home):

		self.uplist = {}
		for i in range(len(json_home[ktype])):
			cnumber = re.search("\d+",json_home[ktype][i]["url"]).group()
			homepage = root_url + cnumber + "/mainb.html"
			url =requests.get(homepage)
			url.encoding = ENCODE
			mpage =  MinutesPage()
			mpage.feed(url.text)
			self.uplist.update({json_home[ktype][i]["name"]:mpage.data})
		
# {"shuin": ["本会議":[1,2,3...],...],...}
class MinutesPage(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []
		self.flg_date = False
		self.flg_number = False
		
	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if tag == "a" and attrs["target"] == "MAIN" and self.flg_date == False and self.flg_number == False:
			self.data.append({})
			self.data[-1].update({"url":attrs["href"]})
			self.flg_date = True
			self.flg_number = True

	def handle_data(self, data):
		
		if re.match("平成\d+年\d+月\d+日",data) != None:
			tmp_date = re.search("平成\d+年\d+月\d+日",data).group()
			self.data[-1].update({"date":tmp_date})
			self.flg_date = False

		elif re.match("第\d+号",data) != None:
			self.data[-1].update({"number":data})
			self.flg_number = False

			
# コマンドライン引数を設定
arg_parser = ArgumentParser()
arg_parser.add_argument("--init", action="store_true", help="obtain committee lists")
arg_parser.add_argument("--done", help="obtain committee lists", type=str)
arg_parser.add_argument("-s", help="specify committee name",type=str)
arg_parser.add_argument("-n", help="specify kaiki",type=int)
arg_parser.add_argument("--undone","-ul", action="store_true",help="list all undone minutes")
args = arg_parser.parse_args()

if args.init:
	json_data = {} 
	CommitteeFile("shuin", HOME_SHUIN, json_data)
	CommitteeFile("sanin", HOME_SANIN, json_data)
	CommitteeFile("ryoin", HOME_RYOIN, json_data)
	f = codecs.open(FILE_COMMITTEE, "w", "utf-8")
	json.dump(json_data,f, ensure_ascii=False)
	f.close()

elif args.done in ["shuin","sanin","ryoin"] and args.s and args.n:
	f = codecs.open(FILE_COMMITTEE, "r", "utf-8")
	json_data = json.load(f)
	f.close()

	for i in range(len(json_data[args.done])):

		if json_data[args.done][i]["name"] == args.s:
			if  args.n not in json_data[args.done][i]["kaiki"]:
				json_data[args.done][i]["kaiki"].append(args.n)
			else:
				print("it's already logged.")

	f = codecs.open(FILE_COMMITTEE, "w", "utf-8")
	json.dump(json_data,f, ensure_ascii=False)
	f.close()

elif args.undone:
	json_home = {} 
	CommitteeFile("shuin", HOME_SHUIN, json_home)
	CommitteeFile("sanin", HOME_SANIN, json_home)
	CommitteeFile("ryoin", HOME_RYOIN, json_home)
	
	f = codecs.open(FILE_COMMITTEE, "r", "utf-8")
	json_done = json.load(f)
	f.close()

	if HOME_SHUIN != "":
		shu = MinutesList("shuin",ROOT_SHUIN,json_home)

	if HOME_SANIN != "":
		san = MinutesList("sanin",ROOT_SANIN,json_home)

	if HOME_RYOIN != "":
		ryo = MinutesList("ryoin",ROOTE_RYOIN,json_home)
	

	print({"shuin":shu.uplist, "sanin":san.uplist})	


