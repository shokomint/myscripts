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
    src = src.replace("(cid:7926)","ょ")
    src = src.replace("(cid:7938)","ヵ")
    src = src.replace("(cid:7939)","ヶ")
    src = src.replace("(cid:7891)","ー")
    src = src.replace("(cid:7928)","ァ")
    src = src.replace("(cid:7929)","ィ")
    src = src.replace("(cid:7931)","ェ")
    src = src.replace("(cid:7932)","ォ")
    src = src.replace("(cid:7934)","ャ")
    src = src.replace("(cid:7935)","ュ")
    src = src.replace("(cid:7936)","ョ")
    src = src.replace("(cid:7933)","ッ")
    src = src.replace("(cid:7722)","遡")
    src = src.replace("(cid:7767)","灘")
    src = src.replace("(cid:7970)","餐")
    src = src.replace("(cid:7972)","煽")
    src = src.replace("(cid:7894)","〜")

    f = open(args.file,"w")
    f.write(src)
    f.close()

