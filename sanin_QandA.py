# 参考 
# https://qiita.com/Taillook/items/a0f2c59d8e17381fc835
# https://media.accel-brain.com/web-pdf-abstract-academic-papers/

import requests
import re
import urllib
from html.parser import HTMLParser
from argparse import ArgumentParser

class ParserTable(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []
		self.title = False
		self.syup = False
		self.toup = False
	
	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)

		if tag == "a" and re.match("meisai", attrs["href"]):
			self.title = True
			self.data.append({})

		elif tag == "a" and re.match("syup", attrs["href"]):
			self.data[-1].update({"syup":attrs["href"]})
			self.syup = False

		elif self.syup == True:
			self.data[-1].update({"syup":"not yet"})
			self.syup = False

		elif tag == "a" and re.match("toup", attrs["href"]):
			self.data[-1].update({"toup":attrs["href"]})
			self.toup = False

		elif self.toup == True:
			self.data[-1].update({"toup":"not yet"})
			self.toup = False

	def handle_data(self, data):
		if self.title == True:
			self.data[-1].update({"title":data})
			self.title = False
			self.syup = True
			self.toup = True

# 参照する国会会期のURLを指定 
f = requests.get("http://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/195/syuisyo.htm")
f.encoding = "utf-8"
parser = ParserTable()
parser.feed(f.text)
parser.close()
f.close()

# PDFファイルのルート 
root_pdf = "http://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/195/"

# PDFファイルダウンロード先
dir_name = "sanin_downloads"

# コマンドライン引数の設定 
arg_parser = ArgumentParser()
arg_parser.add_argument("--number", "-n", help="specify question number",type=int)
arg_parser.add_argument("--list","-l", action="store_true", help="list all the quiestions")
arg_parser.add_argument("--download", "-d", help="download q and a", type=int) 
args = arg_parser.parse_args()

if args.number:
	q = args.number - 1
	if q >= 0 and q < len(parser.data):
		print(parser.data[q]["title"])
		print(root_pdf + parser.data[q]["syup"])
		print(root_pdf + parser.data[q]["toup"])

if args.list:
	i = 0
	for d in parser.data:
		print(d["title"])

		if d["syup"] != "not yet":
			print(root_pdf + d["syup"])
		else:
			print(d["syup"])
	
		if d["toup"] != "not yet":
			print(root_pdf + d["toup"])
		else:
			print(d["toup"])

		print("")

if args.download:
	if parser.data[args.download-1]["syup"] != "not yet":
		result = urllib.request.urlretrieve(root_pdf + parser.data[args.download-1]["syup"], dir_name + "/q_" + str(args.download) + ".pdf")
	if parser.data[args.download-1]["toup"] != "not yet":
		result = urllib.request.urlretrieve(root_pdf + parser.data[args.download-1]["toup"], dir_name + "/a_" + str(args.download) + ".pdf")
	print(parser.data[args.download-1]["title"])
	print(root_pdf + parser.data[args.download-1]["syup"])
	print(root_pdf + parser.data[args.download-1]["toup"])


