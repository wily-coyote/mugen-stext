import sublime
import sublime_plugin

import subprocess
import threading
import os

from .utils import command

class MugenCommand(command.BaseCommand):
	def get_cli(self, shtuff):
		vars = self.window.extract_variables()
		settings = sublime.load_settings("MUGEN.sublime-settings")
		mugen = settings.get("mugen_path", "")
		for x in ["char1", "char2"]:
			if shtuff[x] == "${file_base_name}":
				shtuff[x] = vars["file_base_name"]
		if len(mugen) <= 0:
			sublime.error_message("Please tell me where MUGEN is and run the build again.")
			self.window.open_file("{}/MUGEN/MUGEN.sublime-settings".format(sublime.packages_path()))
			sublime.save_settings("MUGEN.sublime-settings")
			return
		args = [mugen]
		if len(shtuff["char1"]) > 0 or len(shtuff["char2"]) > 0:
			args.append(shtuff["char1"])
			args.append(shtuff["char2"])
		return os.path.split(mugen)[0], args