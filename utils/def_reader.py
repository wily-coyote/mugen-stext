import re

_comment_re = re.compile(r";.*$")
_section_re = re.compile(r"(?!\[\s*).*?(?=\s*\])")
_keyval_re = re.compile(r"\s*(?P<key>.*?)\s*=\s*(?P<value>.*?)$")

def read(file):
	_dict = {}
	section = ""
	for line in file:	
		line = line.strip()	
		line = _comment_re.sub("", line)
		keymatch = _keyval_re.search(line)
		sectionmatch = _section_re.search(line)
		if keymatch:
			key = keymatch.group("key")
			fard = keymatch.group("value").strip().split(",")
			_dict[section][key] = fard[0] if len(fard) == 1 else fard
			continue
		if sectionmatch:
			section = sectionmatch.group(0)
			if section not in _dict:
				_dict[section] = {}
			continue
	return _dict