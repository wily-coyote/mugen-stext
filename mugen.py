import sublime
import sublime_plugin

import subprocess
import threading
import os

from .utils import command
from .utils import def_reader

class MugenCommand(command.BaseCommand):
	def get_cli(self, shtuff):
		vars = self.window.extract_variables()
		settings = sublime.load_settings("MUGEN.sublime-settings")
		mugen = settings.get("ikemen_path", "") if shtuff.get("ikemen", False) is True else settings.get("mugen_path", "")
		kfm = settings.get("kfm_path", "kfm")
		if len(mugen) <= 0:
			sublime.error_message("Please tell me where {} is and run the build again.".format("IKEMEN" if shtuff.get("ikemen", False) is True else "MUGEN"))
			self.window.open_file("{}/MUGEN.sublime-settings".format(os.path.join(sublime.packages_path(), "User")))
			return
		for x in ["char1", "char2", "motif", "stage"]:
			if shtuff[x] == "${file_base_name}":
				shtuff[x] = vars["file_base_name"]
			if shtuff[x] == "${def_input}":
				thing = "chars"
				if x == "stage":
					thing = "stages"
				shtuff[x] = (os.path.splitext(os.path.relpath(vars["file"], os.path.join(os.path.dirname(mugen), thing)))[0].replace("\\", "/"))+".def"
			if shtuff[x] == "${kfm}":
				shtuff[x] = kfm
			if shtuff[x] == "${def_output}":
				with open(vars["file"], "r") as file:
					deffile = def_reader.read(file)
					print(deffile)
					if ("Output" in deffile) and ("filename" in deffile["Output"]):
						shtuff[x] = os.path.splitext(os.path.basename(deffile["Output"]["filename"]))[0]
					else:
						thing = "chars"
						if x == "stage":
							thing = "stages"
						shtuff[x] = (os.path.splitext(os.path.relpath(vars["file"], os.path.join(os.path.dirname(mugen), thing)))[0].replace("\\", "/"))
		args = [mugen]
		if len(shtuff["char1"]) > 0 or len(shtuff["char2"]) > 0:
			args.append(shtuff["char1"])
			args.append(shtuff["char2"])
		if len(shtuff["motif"]) > 0:
			args.append("-r")
			args.append(shtuff["motif"])
		if len(shtuff["stage"]) > 0:
			args.append("-s")
			args.append(shtuff["stage"])
		return os.path.split(mugen)[0], args