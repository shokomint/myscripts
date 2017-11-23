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

# 委員会のホムペから議事録一覧を取得する。
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

            # 委員会ホムペから取得した議事録一覧に、会期を追加する。
            for i in range(len(klist.clist)):
                klist.clist[i].update({"kaiki":[]})
                json_data.update({ktype:klist.clist})

# 議事録一覧を取得する
class MinutesList():
    def __init__(self, ktype, root_url, json_home):

        self.uplist ={} 
        for i in range(len(json_home[ktype])):

            # 委員会ページ
            cnumber = re.search("\d+",json_home[ktype][i]["url"]).group()
            homepage = root_url + cnumber + "/mainb.html"
            url =requests.get(homepage)
            url.encoding = ENCODE
            mpage =  MinutesPage()
            mpage.feed(url.text)

            # 委員会ページにアップされてる議事録集    
            self.uplist.update({json_home[ktype][i]["name"]:mpage.data})

    def print(self):
        print(self.uplist)

# 委員会ページを読み出し、アップされてる議事録を取得する。
class MinutesPage(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.flg_date = False
        self.flg_number = False
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and re.search("pdf",attrs["href"]) == None and self.flg_date == False and self.flg_number == False:
            
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


class PrintMinutesList():
    def __init__(self, ktype, root_url, done_list, uplist):

        x = 0
        for key in uplist:
            if len(uplist[key]) > len(done_list[ktype][x]["kaiki"]):
                i = 0 
                while i < len(uplist[key]) - len(done_list[ktype][x]["kaiki"]):
                    print(key + uplist[key][i]["number"])
                    print(root_url+re.search("\d+",done_list[ktype][x]["url"]).group()+re.search("/\d+\w+.html",uplist[key][i]["url"]).group())
                    print("")
                    i += 1
            x += 1

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
                json_data[args.done][i]["kaiki"].insert(0,args.n)
            else:
                print("it's already logged.")

    f = codecs.open(FILE_COMMITTEE, "w", "utf-8")
    json.dump(json_data,f, ensure_ascii=False)
    f.close()

elif args.undone:
    
    f = codecs.open(FILE_COMMITTEE, "r", "utf-8")
    json_done = json.load(f)
    f.close()

    if HOME_SHUIN != "":
        shu = MinutesList("shuin",ROOT_SHUIN,json_done)
        print("shuin")
        PrintMinutesList("shuin",ROOT_SHUIN,json_done,shu.uplist)

    if HOME_SANIN != "":
        san = MinutesList("sanin",ROOT_SANIN,json_done)
        print("sanin")
        PrintMinutesList("sanin",ROOT_SANIN,json_done,san.uplist)

    if HOME_RYOIN != "":
        ryo = MinutesList("ryoin",ROOT_RYOIN,json_done)
        print("ryoin")
        PrintMinutesList("ryoin",ROOT_RYOIN,json_done,ryo.uplist)
 
