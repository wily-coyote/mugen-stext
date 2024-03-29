import sublime
import sublime_plugin

import subprocess
import threading
import os
import time

class BaseCommand(sublime_plugin.WindowCommand):
	start = 0
	encoding = "utf-8"
	killed = False
	proc = None
	panel = None
	panel_lock = threading.Lock()
	def run(self, name=None, char1="", char2="", motif="", stage="", storyboard="", ikemen=False):
		self.start = time.time()
		runs = locals()
		
		working_dir, argv = self.get_cli(runs)

		if argv is None:
			return

		with self.panel_lock:
			self.panel = self.window.create_output_panel("exec")
			self.window.run_command("show_panel", {"panel": "output.exec"})

		self.queue_write('{}, {}\n'.format(working_dir, argv))

		self.proc = subprocess.Popen(
			argv,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			cwd=working_dir,
			shell=True
		)

		self.killed = False

		threading.Thread(
			target=self.read_handle,
			args=(self.proc.stdout,)
		).start()

	def get_cli(self, vars):
		"""Get working directory and command line"""
		sublime.save_settings("MUGEN.sublime-settings")
		settings = sublime.load_settings("MUGEN.sublime-settings")
		vars = self.window.extract_variables()
		bah = ("mugen_path", "MUGEN")
		if vars["ikemen"] is True:
			bah = ("ikemen_path", "IKEMEN")
		mugen = settings.get(bah[0], "")
		if len(mugen) <= 0:
			sublime.error_message("Please tell me where {} is and run the build again.".format(bah[1]))
			self.window.open_file("{}/MUGEN.sublime-settings".format(os.path.join(sublime.packages_path(), "User")))
			sublime.save_settings("MUGEN.sublime-settings")
			return None
		args = [mugen]
		return (os.path.split(mugen)[0], args)

	def is_enabled(self):
		return True
	def is_visible(self):
		return True
	def description(self):
		return ""

	def read_handle(self, handle):
		chunk_size = 2 ** 13
		out = b''
		while True:
			try:
				data = os.read(handle.fileno(), chunk_size)
				out += data
				if len(data) == chunk_size:
					continue
				if data == b'' and out == b'':
					self.done()
					break
				self.queue_write(out.decode(self.encoding))
				if data == b'':
					self.done()
					break
				out = b''
			except (UnicodeDecodeError) as e:
				msg = 'Error decoding output using %s - %s'
				self.queue_write(msg  % (self.encoding, str(e)))
				break

	def done(self):
		return self.queue_write("\n<Done ({}s)>".format(round(time.time()-self.start,2)))

	def queue_write(self, text):
		sublime.set_timeout(lambda: self.do_write(text), 1)

	def do_write(self, text):
		with self.panel_lock:
			self.panel.run_command('append', {'characters': text})

