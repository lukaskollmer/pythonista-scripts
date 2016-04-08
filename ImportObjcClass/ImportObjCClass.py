# coding: utf-8
import editor, console, sys
from objc_util import ObjCClass

selection = editor.get_selection()
line = editor.get_line_selection()

text = editor.get_text()

classname = text[int(selection[0]):int(selection[1])]

try:
	ObjCClass(classname)
	editor.set_selection(selection[1])
	editor.replace_text(selection[1], selection[1], ' = ObjCClass(\'{}\')'.format(classname))
except:
	console.hud_alert(sys.exc_info()[1].message, 'error')
