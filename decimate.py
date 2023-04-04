import sublime
import sublime_plugin


class DecimateCommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sel = view.sel()
		pass