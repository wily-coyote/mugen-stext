import json, sublime, os.path

def getpath(bah):
	return os.path.join(sublime.packages_path(), "MUGEN", "utils", bah)

data = {}

jsons = [
	"mugen-sctrl",
	"mugen-trigger",
	"ikemen-sctrl",
	"ikemen-trigger"
]

for path in jsons:
	with open(getpath(path+".json"), "r") as file:
		data[path] = json.load(file)