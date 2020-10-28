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

	tracking = False
	daily_runtime = 0

	session_start = 0
	session_runtime = 0
	total_runtime = 0
	action = 0
	session_count = 0

	while True:

		current_time = time.strftime("%H:%M:%S", time.localtime())
		app_list = os.popen('wmic process get description').read()

		if app in app_list and tracking == False:
			if action == 1:
				pass
			else:
				tracking = True
				session_start = in_seconds(current_time)
				session_count += 1
				print('{} started at {}.'.format(str(app), str(current_time)))
				action = 1
				
		elif app in app_list and tracking == True:
			
			session_runtime = in_seconds(current_time) - session_start
			print('{} has been running for {}.'.format(str(app), str(format_seconds(session_runtime))),end='\r', flush=True)
		

		elif app not in app_list and tracking == False:
			if action == 2:
				pass
			else:
				print('\n{} not running. Waiting for input.\n'.format(str(app)))
				action = 2
		elif app not in app_list and tracking == True:
			if action == 3:
				pass
			else:
				total_runtime += session_runtime
				print('\n{} closed.\nSession runtime: {}\nDaily runtime: {}\nDaily session count: {}\n'.format(str(app), str(format_seconds(session_runtime)), str(format_seconds(total_runtime)), str(session_count)),end='\r', flush=True)
				session_runtime = 0
				session_start = 0
				tracking = False
				action == 3
		else:
			pass

run_check()