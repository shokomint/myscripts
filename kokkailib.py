import json

# 要約終了記録ファイル
log_done = "log_done.json"

class LogDone():
	def __init__(self, key, value):
		f = open(log_done,"r")
		done_dict = json.load(f)
		f.close()

		if value not in done_dict[key]:
			done_dict[key].append(value)
		f = open(log_done,"w")
		json.dump(done_dict,f)
		f.close()

class UndoneList():
	def __init__(self, key_qa, data):
	# key_qa: shuin_q, shuin_a, sanin_q or sanin_a (for json data)

		f = open(log_done,"r")
		done_dict = json.load(f)
		f.close()

		for i in range(data.get_len()):
			if (i+1) not in done_dict[key_qa]:
				if key_qa in ("shuin_q","sanin_q") and data.get_slink(i) != "not yet":
					print(key_qa + str(i+1))

				elif key_qa in ("shuin_a","sanin_a") and data.get_tlink(i) != "not yet":
					print(key_qa + str(i+1))

class ConvText():
    def __init__(self, org):
        self.text = org.tranlate({
            })
        
