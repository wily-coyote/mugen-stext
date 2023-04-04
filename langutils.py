import sublime
import sublime_plugin
import urllib.parse
import re
from .utils.data import data as data

_args_re = re.compile(r"[\(,\)\*\s]+")

_mugen_doc_format = "<html><body><b>{}</b><p>{}</p><a href=\"{}\">Elecbyte documentation</a><br><a href=\"{}\">MFG documentation (DDG)</a></body></html>"
_ikemen_doc_format = "<html><body><b>{}</b><p>{}</p><a href=\"{}\">Github documentation</a></body></html>"

def sctrl_doc(sctrl):
	if sctrl in data["mugen-sctrl"]:
		return _mugen_doc_format.format(
				sctrl,
				data["mugen-sctrl"][sctrl]["doc"],
				"http://www.elecbyte.com/mugendocs/sctrls.html#{}".format(urllib.parse.quote_plus(sctrl.lower())),
				"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22sctrl%22".format(urllib.parse.quote_plus("\""+sctrl+"\""))
			)
	elif sctrl in data["ikemen-sctrl"]:
		return _ikemen_doc_format.format(
				sctrl,
				data["ikemen-sctrl"][sctrl]["doc"],
				"https://github.com/ikemen-engine/Ikemen-GO/wiki/State-controllers#{}".format(urllib.parse.quote_plus(sctrl.lower()))
			)

def trigger_doc(trigger):
	if trigger in data["mugen-trigger"]:
		return _mugen_doc_format.format(
				trigger,
				data["mugen-trigger"][trigger]["doc"],
				"http://www.elecbyte.com/mugendocs/trigger.html#{}".format(urllib.parse.quote_plus(_args_re.sub("-", trigger.lower()).strip("-"))),
				"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22trigger%22".format(urllib.parse.quote_plus("\""+trigger+"\""))
			)
	elif trigger in data["ikemen-trigger"]:
		return _ikemen_doc_format.format(
				trigger,
				data["ikemen-trigger"][trigger]["doc"],
				"https://github.com/ikemen-engine/Ikemen-GO/wiki/Triggers#{}".format(urllib.parse.quote_plus(trigger.lower()))
			)

_sctrl_index = list(data["mugen-sctrl"].keys())+list(data["ikemen-sctrl"].keys())
_trigger_index = list(data["mugen-trigger"].keys())+list(data["ikemen-trigger"].keys())

class CNSCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if not (view.match_selector(locations[0], "source.cns") or view.match_selector(locations[0], "source.zss")):
			return
		is_zss = view.match_selector(locations[0], "source.zss") is True

		line = view.substr(view.line(locations[0]))
		prefix = prefix.lower()
		out = []

		def do_Trigger():
			for key in _trigger_index:
				if key.lower().startswith(prefix):
					completed = (data["mugen-trigger"].get(key) or data["ikemen-trigger"].get(key)) or None
					if completed is None: continue
					item = sublime.CompletionItem(
						key,
						"trigger",
						completed["fmt"],
						0,
						(7, "t", "trigger"),
						"<a href='subl:show_trigger_documentation {{\"arg\": \"{}\"}}'>Show documentation</a>".format(key)
					)
					out.append(item)


		if line.lower().strip().startswith("type") or is_zss:
			for key in _sctrl_index:
				if key.lower().startswith(prefix):
					completed = (data["mugen-sctrl"].get(key) or data["ikemen-sctrl"].get(key)) or None
					if completed is None: continue
					content = ""
					if is_zss:
						content = key+"{{{}}}".format(";".join(["{}: ".format(x) for x in completed["req"]]))
					else:
						content = key+"\n"+"\n".join(["{}=".format(x) for x in  completed["req"]])+"\n"+"\n".join(["; {}=".format(x) for x in  completed["opt"]])
					item = sublime.CompletionItem(
						key,
						"sctrl",
						content,
						0,	
						(3, "s", "sctrl"),
						"<a href='subl:show_sctrl_documentation {{\"arg\": \"{}\"}}'>Show documentation</a>".format(key)
					)
					out.append(item)
			if is_zss:
				do_Trigger()
		else:
			if view.match_selector(locations[0], "meta.mapping.key.cns") or view.match_selector(locations[0], "punctuation.separator.mapping.key-value.cns"):
				return
			do_Trigger()
		return out

class CNSTooltips(sublime_plugin.EventListener):
	def on_hover(self, view, point, hover_zone):
		if view.syntax() is not None and not (view.syntax().scope in ["source.cns", "source.zss"]):
			return
		is_zss = view.syntax().scope == "source.zss"
		region = view.extract_scope(point)
		text = view.substr(region)
		line = view.substr(view.line(point))

		def do_Trigger():
			region = view.word(point)
			word = view.substr(region)
			found = sorted(list(filter(lambda x: x.strip().lower().startswith(word.lower()), _trigger_index)), key=len)
			if len(found) > 0:
				found = found[0]
				view.show_popup(trigger_doc(found),
				flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				location=point,
				max_width=420)

		if line.strip().startswith("type") or is_zss:
			found = list(filter(lambda x: text.strip().lower().startswith(x.lower()), _sctrl_index))
			if len(found) > 0:
				found = found[0]
				view.show_popup(sctrl_doc(found),
				flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				location=point,
				max_width=420)
				return
			if is_zss:
				do_Trigger()
	
		else:
			if view.match_selector(point, "meta.mapping.key.cns") or view.match_selector(point, "punctuation.separator.mapping.key-value.cns"):
				return
			do_Trigger()

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
