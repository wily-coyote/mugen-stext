import sublime
import sublime_plugin
import urllib.parse
import re
from .utils.data import data as data

_args_re = re.compile(r"[\(,\)\*\s]+")

_fmt_money_re = re.compile(r"\$([A-Za-z_]+[0-9]?)")
_mugen_doc_format = "<html><body><b>{}</b><p>{}</p><a href=\"{}\">Elecbyte documentation</a><br><a href=\"{}\">MFG documentation (DDG)</a></body></html>"
_ikemen_doc_format = "<html><body><b>{}</b><p>{}</p><a href=\"{}\">Github documentation</a></body></html>"

def sctrl_doc(sctrl):
	found = None
	for k in data["sctrl"]:
		if k.lower() == sctrl.lower():
			found = data["sctrl"][k]
			break
	if found["ikgo"]:
		return _ikemen_doc_format.format(
			sctrl,
			found["doc"],
			"https://github.com/ikemen-engine/Ikemen-GO/wiki/State-controllers#{}".format(urllib.parse.quote_plus(sctrl.lower()))
		)
	else:
		return _mugen_doc_format.format(
			sctrl,
			found["doc"],
			"http://www.elecbyte.com/mugendocs/sctrls.html#{}".format(urllib.parse.quote_plus(sctrl.lower())),
			"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22sctrl%22".format(urllib.parse.quote_plus("\""+sctrl+"\""))
		)

def trigger_doc(trigger):
	found = None
	for k in data["trigger"]:
		if k.lower() == trigger.lower():
			found = data["trigger"][k]
			break
	if found["ikgo"]:
		return _ikemen_doc_format.format(
			trigger,
			found["doc"],
			"https://github.com/ikemen-engine/Ikemen-GO/wiki/Triggers#{}".format(urllib.parse.quote_plus(trigger.lower()))
		)
	else:
		return _mugen_doc_format.format(
			trigger,
			found["doc"],
			"http://www.elecbyte.com/mugendocs/trigger.html#{}".format(urllib.parse.quote_plus(_args_re.sub("-", trigger.lower()).strip("-"))),
			"https://duckduckgo.com/?q=!ducky+site:mugenguild.com+{}+AND+%22trigger%22".format(urllib.parse.quote_plus("\""+trigger+"\""))
		)

class CNSCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if not (view.match_selector(locations[0], "source.cns") or view.match_selector(locations[0], "source.zss")):
			return
		is_zss = view.match_selector(locations[0], "source.zss") is True

		# line = view.substr(view.line(locations[0]))
		prefix = prefix.lower()
		out = []


		def do_Trigger():
			for key in data["trigger"]:
				if key.lower().startswith(prefix):
					completed = data["trigger"].get(key) or None
					if completed is None: continue
					idx = 1
					def lovepython(x):
						nonlocal idx
						ret = "${{{}:{}}}".format(idx, x.group(1))
						idx = idx + 1
						return ret
					fmt = completed["fmt"]
					fmt = _fmt_money_re.sub(lambda x: lovepython(x), fmt)
					print(fmt)
					item = sublime.CompletionItem(
						key,
						"trigger",
						fmt,
						1,
						(7, "t", "trigger"),
						"<a href='subl:show_trigger_documentation {{\"arg\": \"{}\"}}'>Show documentation</a>".format(key)
					)
					out.append(item)

		for key in data["sctrl"]:
			if key.lower().startswith(prefix):
				completed = data["sctrl"].get(key) or None
				if completed is None: continue
				content = ""
				if is_zss:
					content = key+"{\n"
					idx = 1
					if completed.get("req"):
						for item in completed["req"]:
							content += "\t{}: ".format(item["name"])
							values = item["value"].copy()
							for k in range(len(values)):
								values[k] = "${{{}:{}}}".format(idx, values[k])
								idx+=1
							content += ", ".join(values) + ";\n"
					if completed.get("opt"):
						for item in completed["opt"]:
							content += "\t# {}: ".format(item["name"])
							values = item["value"].copy()
							for k in range(len(values)):
								values[k] = "${{{}:{}}}".format(idx, values[k])
								idx+=1
							content += ", ".join(values) + ";\n"
					content += "}"
				else:
					idx = 1
					content = "[State ${{{}:{}}}]\n".format(idx, key); idx += 1
					content += "type={}\n".format(key)
					content += "trigger1=${{{}:1}}\n".format(idx); idx += 1
					if completed.get("req"):
						for item in completed["req"]:
							content += "{}=".format(item["name"])
							values = item["value"].copy()
							for k in range(len(values)):
								values[k] = "${{{}:{}}}".format(idx, values[k])
								idx+=1
							content += ", ".join(values) + "\n"
					if completed.get("opt"):
						for item in completed["opt"]:
							content += "; {}=".format(item["name"])
							values = item["value"].copy()
							for k in range(len(values)):
								values[k] = "${{{}:{}}}".format(idx, values[k])
								idx+=1
							content += ", ".join(values) + "\n"
				item = sublime.CompletionItem(
					key,
					"sctrl",
					content,
					1,
					(3, "s", "sctrl"),
					"<a href='subl:show_sctrl_documentation {{\"arg\": \"{}\"}}'>Show documentation</a>".format(key)
				)
				out.append(item)
		do_Trigger()
		return out

class CNSTooltips(sublime_plugin.EventListener):
	def on_hover(self, view, point, hover_zone):
		if view.syntax() is not None and not (view.syntax().scope in ["source.cns", "source.zss"]):
			return
		is_zss = view.syntax().scope == "source.zss"
		region = view.extract_scope(point)
		word = view.substr(region)
		line = view.substr(view.line(point))
		if len(line) <= 0: return

		def do_Trigger():
			region = view.word(point)
			word = view.substr(region)
			found = sorted(list(filter(lambda x: x.strip().lower().startswith(word.lower()), data["trigger"].keys())), key=len)
			if len(found) > 0:
				found = found[0]
				view.show_popup(trigger_doc(found),
				flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
				location=point,
				max_width=420)

		if line.strip().startswith("type") or is_zss:
			found = list(filter(lambda x: x.strip().lower().startswith(word.lower()), data["sctrl"].keys()))
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
