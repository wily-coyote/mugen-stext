import sublime
import sublime_plugin
import urllib.parse
import re
from .utils.data import data as data

_args_re = re.compile(r"[\(,\)\*\s]+")

def sctrl_doc(sctrl):
	return "<html><body><b>{}</b><p>{}</p><a href=\"{}\">Elecbyte documentation</a><br><a href=\"{}\">MFG documentation (DDG)</a></body></html>".format(
					sctrl,
					data["mugen-sctrl"][sctrl]["doc"],
					"http://www.elecbyte.com/mugendocs/sctrls.html#{}".format(urllib.parse.quote_plus(sctrl.lower())),
					"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22sctrl%22".format(urllib.parse.quote_plus("\""+sctrl+"\""))
				)

def trigger_doc(trigger):
	return "<html><body><b>{}</b><p>{}</p><a href=\"{}\">Elecbyte documentation</a><br><a href=\"{}\">MFG documentation (DDG)</a></body></html>".format(
					trigger,
					data["mugen-trigger"][trigger]["doc"],
					"http://www.elecbyte.com/mugendocs/trigger.html#{}".format(urllib.parse.quote_plus(_args_re.sub("-", trigger.lower()).strip("-"))),
					"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22trigger%22".format(urllib.parse.quote_plus("\""+trigger+"\""))
				)

class CNSCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if not view.match_selector(locations[0], "source.cns"):
			return []

		line = view.substr(view.line(locations[0]))
		prefix = prefix.lower()
		out = []

		if line.lower().strip().startswith("type"):
			for key in data["mugen-sctrl"].keys():
				if key.lower().startswith(prefix):
					completed = data["mugen-sctrl"][key]
					item = sublime.CompletionItem(
						key,
						"sctrl",
						key+"\n"+"\n".join(["{}=".format(x) for x in  completed["req"]])+"\n"+"\n".join(["; {}=".format(x) for x in  completed["opt"]]),
						0,	
						(3, "s", "sctrl"),
						"<a href='subl:show_sctrl_documentation {{\"arg\": \"{}\"}}'>Show documentation</a>".format(key)
					)
					out.append(item)
		else:
			if view.match_selector(locations[0], "meta.mapping.key.cns") or view.match_selector(locations[0], "punctuation.separator.mapping.key-value.cns"):
				return
			for key in data["mugen-trigger"].keys():
				if key.lower().startswith(prefix):
					completed = data["mugen-trigger"][key]
					item = sublime.CompletionItem(
						key,
						"trigger",
						completed["fmt"],
						0,
						(7, "t", "trigger"),
						"<a href='subl:show_trigger_documentation {{\"arg\": \"{}\"}}'>Show documentation</a>".format(key)
					)
					out.append(item)

		return out

class CNSTooltips(sublime_plugin.EventListener):
	def on_hover(self, view, point, hover_zone):
		if view.syntax() is not None and view.syntax().scope != "source.cns":
			return
		region = view.extract_scope(point)
		text = view.substr(region)
		line = view.substr(view.line(point))
		if line.strip().startswith("type"):
			found = list(filter(lambda x: text.strip().lower().startswith(x.lower()), data["mugen-sctrl"].keys()))
			if len(found) > 0:
				found = found[0]
				view.show_popup(sctrl_doc(found),
				flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				location=point,
				max_width=420)
		else:
			if view.match_selector(point, "meta.mapping.key.cns") or view.match_selector(point, "punctuation.separator.mapping.key-value.cns"):
				return
			region = view.word(point)
			word = view.substr(region)
			found = sorted(list(filter(lambda x: x.strip().lower().startswith(word.lower()), data["mugen-trigger"].keys())), key=len)
			if len(found) > 0:
				found = found[0]
				view.show_popup(trigger_doc(found),
				flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				location=point,
				max_width=420)

class ShowSctrlDocumentationCommand(sublime_plugin.ApplicationCommand):
	def run(self, arg=None):
		if arg: 
			sublime.active_window().active_view().show_popup(
				sctrl_doc(arg),
				flags=sublime.COOPERATE_WITH_AUTO_COMPLETE|sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				max_width=420
			)

class ShowTriggerDocumentationCommand(sublime_plugin.ApplicationCommand):
	def run(self, arg=None):
		if arg: 
			sublime.active_window().active_view().show_popup(
				trigger_doc(arg),
				flags=sublime.COOPERATE_WITH_AUTO_COMPLETE|sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				max_width=420
			)
