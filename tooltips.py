import sublime_plugin, sublime, json, os, urllib.parse

sctrls = []
with open(os.path.join(sublime.packages_path(), "MUGEN", "sctrl.sublime-completions"), "r") as funny:
	sctrls = json.loads(funny.read())["completions"]

class MugenTooltipListener(sublime_plugin.EventListener):
	def on_hover(self, view, point, hover_zone):
		if view.syntax().scope != "source.cns":
			return
		region = view.extract_scope(point)
		text = view.substr(region)
		found = list(filter(lambda x: text.strip().lower().startswith(x["trigger"].lower()), sctrls))
		if len(found) > 0:
			found = found[0]
			view.show_popup("<b>{}</b><p>{}</p><a href=\"{}\">Elecbyte documentation</a><br><a href=\"{}\">MFG documentation (DDG)</a>".format(
				found["trigger"],
				found["details"],
				"http://www.elecbyte.com/mugendocs/sctrls.html#{}".format(urllib.parse.quote_plus(found["trigger"].lower())),
				"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22sctrl%22".format(urllib.parse.quote_plus("\""+found["trigger"]+"\""))),
			flags=8,
			location=point,
			max_width=420)