import json, sublime, os.path

def getpath(bah):
	return os.path.join(sublime.packages_path(), "MUGEN", "utils", bah)

data = {}

with open(getpath("mugen-sctrl.json"), "r") as file:
	data["mugen-sctrl"] = json.load(file)

with open(getpath("mugen-trigger.json"), "r") as file:
	data["mugen-trigger"] = json.load(file)