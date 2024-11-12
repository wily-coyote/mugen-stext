import json, sublime, os.path

def getpath(bah):
	return os.path.join(sublime.packages_path(), "MUGEN", "utils", bah)

def safeget(list, index):
	if index >= len(list):
		return None
	else:
		return list[index]

data = {
	"sctrl": {},
	"trigger": {}
}

with open(getpath("data.tsv"), "r") as file:
	obj = None
	doc = None
	while True:
		line = file.readline()
		if len(line) == 0:
			break
		line = line.rstrip().replace("\\n", "\n")
		if len(line) > 0:
			fields = line.split("\t")
			if len(fields) >= 1:
				field1 = safeget(fields, 0)
				field2 = safeget(fields, 1)
				field3 = safeget(fields, 2)
				if field1 == "sctrl" or field1 == "trigger":
					obj = {
						"ikgo": field3 == "ikgo"
					}
					data[field1][field2] = obj
				else:
					if field1 == "opt" or field1 == "req":
						item = {
							"name": field2,
							"value": []
						}
						for k in range(len(fields)):
							if k >= 2:
								item["value"].append(fields[k])
						if obj.get(field1) is not None:
							obj[field1].append(item)
						else:
							obj[field1] = [item]
					elif field1 == "docbgn":
						doc = ""
						obj["doc"] = doc
					elif field1 == "docend":
						obj["doc"] = doc.rstrip().lstrip()
						doc = None
					elif doc is not None:
						doc = doc + line + "\n"
					elif (obj is not None) and (field1 is not None):
						obj[field1] = field2
