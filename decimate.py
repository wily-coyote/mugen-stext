import sublime
import sublime_plugin
import re

_normalize_chain = [
	(re.compile(r"\s*;.*((?:\n|\r\n)+|$)"), "\n"),
	(re.compile(r"(?:\n|\r\n){2,}"), "\n"),
	(re.compile(r"(?!^)\["), "\n["),
	(re.compile(r"^(?:\r\n|\n)+|(?:\r\n|\n)+$"), "")
]

def normalizeText(text):
	_text = text
	for regex in _normalize_chain:
		_text = regex[0].sub(regex[1], _text)
	return _text

class NormalizeCnsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sel = view.sel()
		for region in sel:
			text = view.substr(region)
			view.replace(edit, region, normalizeText(text))
		pass

	def is_enabled(self):
		return self.view.syntax().scope == "source.cns"

class NormalizeAllCnsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sel = view.sel()
		region = sublime.Region(0, len(view))
		text = view.substr(region)
		view.replace(edit, region, normalizeText(text))
		pass

	def is_enabled(self):
		return self.view.syntax().scope == "source.cns"