#!/usr/bin/env python

import os
import gen_settingsstructs
from gen_settingsstructs import Struct, Array

html_tmpl = """
<!doctype html>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Description of SumatraPDF settings</title>
<style type=text/css>
body {
	font-size: 90%;
	background-color: #f5f5f5;
}

.txt1 {
	/* bold doesn't look good in the fonts above */
	font-family: Monaco, 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Lucida Console', monospace;
	font-size: 88%;
	color: #800; /* this is brown */
}

.txt {
	font-family: Verdana, Arial, sans-serif;
	font-size: 90%;
	font-weight: bold;
	color: #800; /* this is brown */
}

.cm {
	color: #800;   /* this is brown, a bit aggressive */
	color: #8c8c8c; /* this is gray */
	color: #555; /* this is darker gray */
	font-weight: normal;
}
</style>
</head>

<p>You can change the look and behavior of
<a href="http://blog.kowalczyk.info/software/sumatrapdf/">SumatraPDF</a>
by editing <code>SumatraPDF.dat</code> settings file.</p>

<p>The file is stored in <code>%APPDATA%\SumatraPDF</code> directory for the
installed version or in the same directory as SumataPDF.exe executable for the
portable version.</p>

<p>The file is in a simple text format. Here's what different settings mean and
what is their default value:</p>

<pre class=txt>
%INSIDE%
</pre>

<body>

</body>
</html>
"""

#indent_str = "&nbsp;&nbsp;"
indent_str = "  "

def gen_comment(comment, start, first = False):
	line_len = 80
	s = start + '<span class=cm>'
	if not first:
		s = "\n" + s
	left = line_len - len(start)
	for word in comment.split():
		if left < len(word):
			s += "\n" + start
			left = line_len - len(start)
		word += " "
		left -= len(word)
		s += word
	s = s.rstrip()
	s += '</span>'
	return [s]

def gen_struct(struct, comment=None, indent=""):
	lines = []
	if comment:
		lines += gen_comment(comment, "") + [""]
	for field in struct.default:
		if field.internal:
			continue
		first = (field == struct.default[0])
		if type(field) in [Struct, Array] and not field.type.name == "Compact":
			lines += gen_comment(field.comment, indent, first)
			#lines += ["%s%s [" % (indent, field.name), gen_struct(field, None, indent + "  "), "%s]" % indent, ""]
			lines += ["%s%s [" % (indent, field.name), gen_struct(field, None, indent + indent_str), "%s]" % indent]
		else:
			s = field.inidefault(commentChar="").lstrip()
			lines += gen_comment(field.comment, indent, first) + [indent + s]
	return "\n".join(lines)

def gen_html():
	prefs = gen_settingsstructs.GlobalPrefs
	inside = gen_struct(prefs)
	s = html_tmpl.replace("%INSIDE%", inside)
	p = os.path.join("scripts", "settings.html")
	open(p, "w").write(s)

if __name__ == "__main__":
	gen_html()
