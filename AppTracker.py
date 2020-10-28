import os
import time

app = 'sublime_text.exe'

def in_seconds(time_str):
	# Converts a time string (hh:mm:ss) into an integer of seconds.

	h,m,s = time_str.split(':')
	seconds = (int(h)*60*60)+(int(m)*60)+int(s)

	return(seconds)

def total_time(start_str, end_str):
	# Finds the elapsed total seconds between a starting string and
	# ending string (formatted as hh:mm:ss) as an integer of seconds.

	elapsed_time = time.strftime('%H:%M:%S', time.gmtime(in_seconds(end_str) - in_seconds(start_str)))

	print(elapsed_time)

def format_seconds(seconds):
	# Converts an integer of seconds into the string hh:mm:ss

 	return(time.strftime('%H:%M:%S', time.gmtime(seconds)))


def run_check():

	# Lots of variables. Probably too many.
	
	tracking = False
	waiting = False
	session_start = 0
	session_runtime = 0
	daily_runtime = 0
	session_count = 1
	action = 0

	# The action variable determines whether or not some if statements will pass. This was due to
	# some issues I was having with clean print statements of statuses, which would occasionally
	# overlap. This is a quick workaround that I hope to fix with improvment in string manipulation.

	while True:

		current_time = time.strftime("%H:%M:%S", time.localtime())
		app_list = os.popen('wmic process get description').read()

		started = ('{} started at {}. Session count: {}'.format(str(app), str(current_time), str(session_count)))
		running = ('{} has been running for {}.'.format(str(app), str(format_seconds(session_runtime)),))
		not_running = ('{} not running. Waiting for open.\n'.format(str(app)))
		closed = ('''{} closed.\nSession runtime: {}\nTotal runtime today: {}\n'''.format(str(app),str(format_seconds(session_runtime)),format(str(format_seconds(daily_runtime)))))
		state_change = False
		output = ''

		
		if app in app_list and tracking == False:
			if action == 1:
				pass
			else:
				tracking = True
				session_count += 1
				session_start = in_seconds(current_time)
				output = (started)
				action = 1
		elif app in app_list and tracking == True:
				session_runtime = in_seconds(current_time) - session_start
				output = (running,end='\r', flush=True)
		elif app not in app_list and tracking == False:
			if action == 2:
				pass
			else:
				output = (not_running)
				action = 2
		elif app not in app_list and tracking == True:
			if action == 3:
				pass
			else:
				daily_runtime += session_runtime
				session_runtime = 0
				session_start = 0
				tracking = False
				output = ('')
				output = (closed)
				action = 3
		else:
			pass

run_check()