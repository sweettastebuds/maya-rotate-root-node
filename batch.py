import os
import sys
import imp
import subprocess
import logging
import datetime

MAYA_EXE_PATH = "D:\Program Files\Autodesk\Maya2019\\bin\maya.exe"
IMPORT_FILETYPE = '.ma'
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'main.py')
LOGGER_CONFIG = False


logger = logging.getLogger('maya_logger')
log_dir = os.path.join(os.path.dirname(__file__), 'log')

#	Checks if log dir exists, and creates it if not
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

#	Sets log filenames per run instance
log_file = os.path.join(log_dir, 'log_' + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.txt')
error_log_file = os.path.join(log_dir, 'error_log_' + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.txt')
assets_log_file = os.path.join(log_dir, 'asset_log_' + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.txt')
"""
    Functions
"""    



def createAssetsLog():
    #	ASSET LOG FILE CREATION
    with open(assets_log_file, 'w') as assets_log:
        assets_log.write("*" * 100+"\n")
        assets_log.write("Assets Log - " + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + "\n")
        assets_log.write("*" * 100+"\n")

    assets_log.close()


def configure_logging():
	# http://stackoverflow.com/questions/4136129/managing-loggers-with-python-logging
	global LOGGER_CONFIG
	if not LOGGER_CONFIG:
		format = "%(asctime)s - %(levelname)s - %(message)s"
		formatter = logging.Formatter(format)
		#logging.basicConfig(format=format)
		logger.setLevel(logging.DEBUG) # or whatever
		console = logging.StreamHandler()
		file = logging.FileHandler(log_file)
		error_file = logging.FileHandler(error_log_file)
		console.setFormatter(formatter)
		file.setFormatter(formatter)
		error_file.setFormatter(formatter)
		error_file.setLevel(logging.ERROR)
		#set a level on the handlers if you want;
		#if you do, they will only output events that are >= that level
		logger.addHandler(console)
		logger.addHandler(file)
		logger.addHandler(error_file)
		LOGGER_CONFIG = True
		logger.debug('Configure logging')

def get_user_input():
	return raw_input()

def query_yes_no(question, default="yes"):
	"""Ask a yes/no question via raw_input() and return their answer.
	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).
	The "answer" return value is True for "yes" or False for "no".
	"""
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = get_user_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")


def parse_inputs():
	# skip first one since it's barkeep.py itself
	print sys.argv
	filepath_list = []
	for filepath in sys.argv[1:]:
		if filepath.startswith('-' or '--'):
			 # is a config argument, skip
			continue
		if filepath.lower().endswith(IMPORT_FILETYPE):
			filepath_list.append(filepath)
			logger.debug('%s file detected' %IMPORT_FILETYPE)

		elif not os.path.isdir(filepath):
			logger.debug('input %s is not %s file, reading file...' %(filepath, IMPORT_FILETYPE))

			with open(filepath, 'r') as text_input_file:
				filepath_list = text_input_file.readlines()

				for filepath in filepath_list:
					filepath = filepath.rstrip()
					logger.debug('filepath: ' + str(filepath))

					if filepath.endswith(IMPORT_FILETYPE):
						filepath_list.append(filepath)

					else:
						logger.error('Invalid filepath "' +
									filepath +
									'": expected %s file' %IMPORT_FILETYPE)
	return filepath_list

if __name__ == "__main__":
    """
	for file
	subprocess call file python batch_actions
	"""

    configure_logging()
    parsed_file_list = parse_inputs()

    parsed_file_list = [file for file in parsed_file_list if file.lower().endswith(IMPORT_FILETYPE)]
    count = 0

    for file in parsed_file_list:
        count += 1
        file = os.path.relpath(file)

        print('call', MAYA_EXE_PATH, '-batch', '-command', 'python "execfile(SCRIPT_PATH)"')
        subprocess.call([ 'call', MAYA_EXE_PATH, '-batch', '-command', 'python "execfile(SCRIPT_PATH)"'], shell=True )

    print('Batch complete!', count)