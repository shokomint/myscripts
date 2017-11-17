# 参考 
# https://qiita.com/Taillook/items/a0f2c59d8e17381fc835
# https://media.accel-brain.com/web-pdf-abstract-academic-papers/

import requests
import re
from html.parser import HTMLParser
from argparse import ArgumentParser

class ParserTable(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []
		self.title = False
		self.slink = False
		self.tlink = False
	
	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if tag == "td" and "headers" in attrs and attrs["headers"] == "SHITSUMON.KENMEI":
			self.data.append({})
			self.title = True

		if tag == "td" and "headers" in attrs and attrs["headers"] == "SHITSUMON.SLINKPDF":
			self.slink = True

		if tag == "td" and "headers" in attrs and attrs["headers"] == "SHITSUMON.TLINKPDF":
			self.tlink = True

		if tag == "a" and self.slink == True:
			self.data[-1].update({"slink":attrs["href"]})
			self.slink = False

		if self.slink == True and tag == "span":
			self.data[-1].update({"slink":"not yet"})
			self.slink = True

		if self.slink == True and tag == "br":
			self.slink = False

		if tag == "a" and self.tlink == True:
			self.data[-1].update({"tlink":attrs["href"]})
			self.tlink = False

		if self.tlink == True and tag == "span":
			self.data[-1].update({"tlink":"not yet"})
			self.tlink = True

		if self.tlink == True and tag == "br":
			self.tlink = False

	def handle_data(self, data):
		if self.title == True:
			self.data[-1].update({"title":data})
			self.title = False

# $B9q2q$N2q4|$rA*Br$9$k(B
f = requests.get("http://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/kaiji195_l.htm")

parser = ParserTable()
parser.feed(f.text)
parser.close()
f.close()

# PDF$B%Z!<%8$N%k!<%H$r@_Dj$9$k(B
root_pdf = "http://www.shugiin.go.jp/internet/"

# $B<hF@$7$?(BPDF$B$N(BURL$B$r@dBP%Q%9$KJQ99$9$k$?$a$N@55,I=8=(B
url = re.compile("^../../../")

# $B%3%^%s%I%i%$%s0z?t(B
arg_parser = ArgumentParser()
arg_parser.add_argument("--number", "-n", help="specify question number",type=int)
arg_parser.add_argument("--list","-l", action="store_true", help="list all the quiestions")
args = arg_parser.parse_args()

if args.number:
	q = args.number - 1
	if q >= 0 and q < len(parser.data):
		print(root_pdf + url.sub("", parser.data[q]["title"]))
		print(root_pdf + url.sub("", parser.data[q]["slink"]))
		print(root_pdf + url.sub("", parser.data[q]["tlink"]))

if args.list:
	i = 0
	for d in parser.data:
		print(d["title"])

		if d["slink"] != "not yet":
			print(root_pdf + url.sub("",d["slink"]))
		else:
			print(d["slink"])
	
		if d["tlink"] != "not yet":
			print(root_pdf + url.sub("",d["tlink"]))
		else:
			print(d["tlink"])

		print("")


