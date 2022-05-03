import sublime
import sublime_plugin

import subprocess
import threading
import os

from .utils import command

class MugenCommand(command.MUGENBaseCommand):
	def get_cli(self, args):
		vars = self.window.extract_variables()
		settings = sublime.load_settings("MUGEN.sublime-settings")
		mugen = settings.get("mugen_path", "")
		for x in [args["char1"], args["char2"]]:
			if x == "${file_base_name}":
				x = vars["file_base_name"]
		if len(mugen) <= 0:
			sublime.error_message("Please tell me where MUGEN is and run the build again.")
			self.window.open_file("{}/MUGEN/MUGEN.sublime-settings".format(sublime.packages_path()))
			sublime.save_settings("MUGEN.sublime-settings")
			return
		args = [mugen]
		if len(args["char1"]) > 0 or len(args["char2"]) > 0:
			args.append(args["char1"])
			args.append(args["char2"])
		return (os.path.split(mugen)[0], args)