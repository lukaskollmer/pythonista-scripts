# coding: utf-8
import re
import sys
import appex
import console
import datetime
import clipboard
import utilities

#clipboard.set('https://youtu.be/fTTGALaRZoc')

add_if_already_exists = False

console.clear()


import LKEvernoteApi



guid = '__YOUR_NOTE_GUID_HERE__'

input = ''

if appex.is_running_extension():
	LKEvernoteApi.log_progress('load url provided to app extension')
	input = appex.get_url()
else:
	LKEvernoteApi.log_progress('not running from extension, checking arguments')
	if len(sys.argv) > 1:
		evernote.log_progress('argument found, use that')
		input = sys.argv[1]
	else:
		LKEvernoteApi.log_progress('no arguments found, will use clipboard text')
		input = clipboard.get()
		if clipboard.get() == '':
			sys.exit('Clipboard is empty, no arguments passed to script')

LKEvernoteApi.log_progress('Loading title of passed url')
url_title = ' (' + utilities.title_of_url(input) + ') '

if url_title is ' () ':
	url_title = ''
else:
	url_title = url_title.replace('&', 'and')

LKEvernoteApi.log_progress('create date text')
date = datetime.datetime.now().strftime('%d %b %Y %H:%M')

LKEvernoteApi.log_progress('create ENML string')
en_todo_text = '<en-todo checked="false"></en-todo> {0}{1}(@ {2})'.format(input, url_title, date)
print(en_todo_text)

LKEvernoteApi.log_progress('call ´appendNote´ function')
LKEvernoteApi.append_to_note(guid=guid, new_content=en_todo_text, main_new_content=input, add_if_already_exists=add_if_already_exists)

LKEvernoteApi.log_progress('Done')

if appex.is_running_extension():
	appex.finish()
	#utilities.quit()
else:
	sys.exit()
