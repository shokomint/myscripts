import re
from argparse import ArgumentParser

arg_parser = ArgumentParser()
arg_parser.add_argument("--file", "-f", help="specify file you want to convert",type=str)
args = arg_parser.parse_args()

if args.file:

    f = open(args.file, "r")
    src = f.read()
    f.close()

    src = src.translate({
        ord('︒'):'。',
        ord('︑'):'、',
        ord('﹁'):'「',
        ord('﹂'):'」',
        ord('︵'):'（',
        ord('︶'):'）',
        ord('〇'):'0'
    })

    src = src.replace("(cid:7923)","っ")
    src = src.replace("(cid:7939)","ヶ")
    src = src.replace("(cid:7891)","ー")
    src = src.replace("(cid:7931)","ェ")
    src = src.replace("(cid:7934)","ャ")
    src = src.replace("(cid:7935)","ュ")
    src = src.replace("(cid:7936)","ョ")
    src = src.replace("(cid:7933)","ッ")
    src = src.replace("(cid:7929)","ィ")
    src = src.replace("(cid:7722)","遡")
    src = src.replace("(cid:7970)","餐")
    src = src.replace("(cid:7894)","〜")

    src = src.replace("平成三十年","2018/")
    src = src.replace("平成二十九年","2017/")
    src = src.replace("平成二十八年","2016/")
    src = src.replace("十月","10/")
    src = src.replace("十一月","11/")
    src = src.replace("十二月","12/")
    src = src.replace("十日","10")
    src = src.replace("十一日","11")
    src = src.replace("十二日","12")
    src = src.replace("十三日","13")
    src = src.replace("十四日","14")
    src = src.replace("十五日","15")
    src = src.replace("十六日","16")
    src = src.replace("十七日","17")
    src = src.replace("十八日","18")
    src = src.replace("十九日","19")
    src = src.replace("二十日","20")
    src = src.replace("二十一日","21")
    src = src.replace("二十二日","22")
    src = src.replace("二十三日","23")
    src = src.replace("二十四日","24")
    src = src.replace("二十五日","25")
    src = src.replace("二十六日","26")
    src = src.replace("二十七日","27")
    src = src.replace("二十八日","28")
    src = src.replace("二十九日","29")
    src = src.replace("三十日","30")
    src = src.replace("三十一日","31")

    src = src.replace("\n一","１.")
    src = src.replace("\n二","２.")
    src = src.replace("\n三","３.")
    src = src.replace("\n四","４.")
    src = src.replace("\n五","５.")
    src = src.replace("\n六","６.")
    src = src.replace("\n七","７.")
    src = src.replace("\n八","８.")
    src = src.replace("\n九","９.")
    src = src.replace("\n十","１０.")
    src = src.replace("\n十一","１１.")
    src = src.replace("\n十二","１２.")

    conv = src.maketrans("一二三四五六七八九","123456789")
    src = src.translate(conv)

    src = src.replace("十","10")
    src = src.replace("年","/")
    src = src.replace("月","/")
    src = src.replace("日","")

    f = open(args.file,"w")
    f.write(src)
    f.close()

