# 参考 
# https://qiita.com/Taillook/items/a0f2c59d8e17381fc835
# https://media.accel-brain.com/web-pdf-abstract-academic-papers/

import requests
import re
import urllib
from html.parser import HTMLParser
from argparse import ArgumentParser
from kokkailib import LogDone,UndoneList
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import MeCab
import CaboCha 

class ParserTable(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.title = False
        self.syuh = False
        self.touh = False
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "a" and re.match("meisai", attrs["href"]):
            self.title = True
            self.data.append({})

        elif tag == "a" and re.match("syuh", attrs["href"]):
            self.data[-1].update({"syuh":attrs["href"]})
            self.syuh = False

        elif self.syuh == True:
            self.data[-1].update({"syuh":"not yet"})
            self.syuh = False

        elif tag == "a" and re.match("touh", attrs["href"]):
            self.data[-1].update({"touh":attrs["href"]})
            self.touh = False

        elif self.touh == True:
            self.data[-1].update({"touh":"not yet"})
            self.touh = False

    def handle_data(self, data):
        if self.title == True:
            self.data[-1].update({"title":data})
            self.title = False
            self.syuh = True
            self.touh = True

    def get_title(self, number):
        return(self.data[number]["title"])

    def get_slink(self, number):
        return(self.data[number]["syuh"])

    def get_tlink(self, number):
        return(self.data[number]["touh"])

    def get_len(self):
        return(len(self.data))

class ParserContents(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ""
        self.flg = False

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.flg = True

    def handle_endtag(self, tag):
        if tag == "td":
            self.flg = False

    def handle_data(self, data):
        if self.flg == True:
            self.data += data

# 参照する国会会期のURLを指定 
f = requests.get("http://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/195/syuisyo.htm")
f.encoding = "utf-8"
parser = ParserTable()
parser.feed(f.text)
parser.close()
f.close()

# HTMLファイルのルート 
root_html = "http://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/195/"

# HTMLファイルダウンロード先
dir_name = "sanin_downloads"

# コマンドライン引数の設定 
arg_parser = ArgumentParser()
arg_parser.add_argument("--number", "-n", help="specify question number",type=int)
arg_parser.add_argument("--summarize", "-sum", help="summarize specified question",type=int)
arg_parser.add_argument("--list","-l", action="store_true", help="list all the quiestions")
arg_parser.add_argument("--download", "-d", help="download q and a", type=int) 
arg_parser.add_argument("--done_Q","-Q",help="input finised question")
arg_parser.add_argument("--done_A","-A",help="input finised answer")
arg_parser.add_argument("--ulist","-ul", action="store_true",help="list undone list")
args = arg_parser.parse_args()

if args.number:
    q = args.number - 1
    if q >= 0 and q < parser.get_len():
        print(parser.get_title(q))
        print(root_html + parser.get_slink(q))
        print(root_html + parser.get_tlink(q))

        f = requests.get(root_html + parser.get_slink(q))
        f.encoding = "utf-8"
        p_contents = ParserContents()
        p_contents.feed(f.text)
        p_contents.close()
        f.close()
        print(p_contents.data)

elif args.summarize:
    
    q = args.summarize - 1
    if q >= 0 and q < parser.get_len():

        f = requests.get(root_html + parser.get_slink(q))
        f.encoding = "utf-8"
        p_contents = ParserContents()
        p_contents.feed(f.text)
        p_contents.close()
        f.close()

        # Object of automatic summarization.
        #auto_abstractor = AutoAbstractor()
        # Set tokenizer for Japanese.
        #auto_abstractor.tokenizable_doc = MeCabTokenizer()
        # Set delimiter for making a list of sentence.
        #auto_abstractor.delimiter_list = ["。", "\n","<br>"]
        # Object of abstracting and filtering document.
        #abstractable_doc = TopNRankAbstractor()
        # Summarize document.
        #result_dict = auto_abstractor.summarize(p_contents.data, abstractable_doc)
        #m = MeCab.Tagger("-Ochasen")
        # Output result.
        #print(m.parse(p_contents.data))

        c = CaboCha.Parser()
        tree =  c.parse(p_contents.data)
        size = tree.size()
        print(tree.toString(2))

elif args.list:
    i = 0
    for d in parser.data:
        print(d["title"])

        if d["syuh"] != "not yet":
            print(root_html + d["syuh"])
        else:
            print(d["syuh"])
    
        if d["touh"] != "not yet":
            print(root_html + d["touh"])
        else:
            print(d["touh"])

        print("")

elif args.download:
    if parser.data[args.download-1]["syuh"] != "not yet":
        result = urllib.request.urlretrieve(root_html + parser.data[args.download-1]["syuh"], dir_name + "/q_" + str(args.download) + ".htm")
    if parser.data[args.download-1]["touh"] != "not yet":
        result = urllib.request.urlretrieve(root_html + parser.data[args.download-1]["touh"], dir_name + "/a_" + str(args.download) + ".htm")
    print(parser.data[args.download-1]["title"])
    print(root_html + parser.data[args.download-1]["syuh"])
    print(root_html + parser.data[args.download-1]["touh"])

elif args.done_Q:
    LogDone("sanin_q",args.done_Q)

elif args.done_A:
    LogDone("sanin_a",args.done_A)


elif args.ulist:
    UndoneList("sanin_q",parser)
    UndoneList("sanin_a",parser)
