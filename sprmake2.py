import sublime
import sublime_plugin

import subprocess
import threading
import os
from .utils import command

class Sprmake2Command(command.MUGENBaseCommand):
	description = "Run sprmake2"
	def get_cli(self, vars):
		"""Get working directory and command line"""
		settings = sublime.load_settings("MUGEN.sublime-settings")
		mugen = settings.get("mugen_path", "")
		vars = self.window.extract_variables()
		if len(mugen) <= 0:
			sublime.error_message("Please tell me where MUGEN is and run sprmake2 again.")
			self.window.open_file("{}/MUGEN/MUGEN.sublime-settings".format(sublime.packages_path()))
			return None
		mugen = os.path.split(mugen)[0]
		return (mugen, [os.path.join(mugen, "sprmake2"), "-o", vars["file_base_name"], vars["file_name"]])