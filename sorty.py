"""
Sorty: A File Sorting Magician for your Computer

Sorty sorts files in your current working folder based on the Extension name.
All .exe files are stored in a separate "EXE Files" folder, .pdf files are stored in "PDF Files" Folder etc

Copyright 2015 Pradipta
"""
import shutil, os, argparse, sys
join = os.path.join

if sys.version_info[0]==2: input = raw_input

def make_folder(name, var):
	"""
	Create a new folder if the folder does not exist.
	If the folder is created then increment the count and return it else return the count directly
	"""
	if not os.path.exists(name):
		os.makedirs(name)
		return var+1
	return var

def get_extension(file):
	"""
	Return the Extension of a filename
	"""
	return file.split('.')[-1]

def get_files(folder,topdown):
	"""
	Return a dictionary of files in the folder where keys are the parent folders of the files and the
	values are a list of files in that folder.

	If topdown is true then return all files in that folder, else return only the immediate files 
	, that is those files that are not under subfolders, in the dictionary
	"""
	if not topdown:
		return {folder:list(filter(lambda x:os.path.isfile(os.path.join(folder,x)),[files for files in os.listdir(folder)]))}
	
	#Use os.walk for recursively accessing all files
	#Use dict constructor method inplace of dictionary comprehension for Python 2.6/3.0 compatibility
	return dict([(root,files) for root, dirs,files in os.walk(folder)])

def run_script(folder,topdown):
	"""
	Run the core script by getting the files and iterating over the dictionary
	
	If the file is already sorted then ignore it else sort it out and move the files.

	"""
	if "c:" in folder.lower():
		x = input("You are running the program from the C Drive. Are you sure you want to sort files in the C Partition?")
		if "n" in x.lower():
			sys.exit(0)
	files = get_files(folder,topdown)
	moves, folders_created = 0,0
	for key in files:
		for f in files[key]:
			folder = get_extension(f).upper() + " Files"
			if not folder in key:
				folders_created = make_folder(join(key,folder),folders_created)
				shutil.move(join(key,f),join(key,folder,f))
				moves += 1

	print ("\nSorty created {0} folders and moved {1} files and sorted them".format(folders_created,moves))

def main():
	"""
	Create the Parser using argparse and parse arguments
	"""

	parser = argparse.ArgumentParser(description=__doc__,usage="sorty [-d DIRECTORY] [--topdown]",formatter_class=argparse.RawTextHelpFormatter)
	
	parser.add_argument('-s','--sort',dest="run", action='store_true',help="Use this parameter to sort files in the current directory")
	parser.add_argument('-d','--directory',help="Use this parameter to change the working directory")
	parser.add_argument('-t','--topdown',dest='feature', action='store_true',help="Use this parameter to sort files in subfolders")
	parser.set_defaults(feature=False)

	args=parser.parse_args()
	if args.directory:
		path = os.path.expanduser(args.directory)
		if os.path.isdir(path):
			os.chdir(path)
		else:
			if 'n' in input("Invalid Directory. Use Current Directory in Script? ").lower():
				sys.exit(0)
	
	if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable) 
		print (os.path.isdir(application_path))
		print ("Sorty is running from path {0}".format(application_path))
	if bool(args.feature) or bool(args.run):
		print ("Sorty is beginning it's magic..")
		run_script(os.getcwd(),bool(args.feature))
	else:
		print (parser.format_help())
		sys.exit(0)
if __name__=='__main__':
	if sys.platform == "win32":
		try:
			import _winreg
		except ImportError:
			import winreg as _winreg
		def define_action_on(filetype, registry_title, command, title=None):
		    """
		    define_action_on(filetype, registry_title, command, title=None)
		        filetype: either an extension type (ex. ".txt") or one of the special values ("*" or "Directory"). Note that "*" is files only--if you'd like everything to have your action, it must be defined under "*" and "Directory"
		        registry_title: the title of the subkey, not important, but probably ought to be relevant. If title=None, this is the text that will show up in the context menu.
		    """
		    #all these opens/creates might not be the most efficient way to do it, but it was the best I could do safely, without assuming any keys were defined.
		    reg = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Classes", 0, _winreg.KEY_SET_VALUE)
		    k1 = _winreg.CreateKey(reg, filetype) #handily, this won't delete a key if it's already there.
		    k2 = _winreg.CreateKey(k1, "shell")
		    k3 = _winreg.CreateKey(k2, registry_title)
		    k4 = _winreg.CreateKey(k3, "command")
		    if title != None:
		        _winreg.SetValueEx(k3, None, 0, _winreg.REG_SZ, title)
		    _winreg.SetValueEx(k4, None, 0, _winreg.REG_SZ, command)
		    _winreg.CloseKey(k3)
		    _winreg.CloseKey(k2)
		    _winreg.CloseKey(k1)
		if getattr(sys, 'frozen', False):

			application_path = os.path.dirname(sys.executable) 
			query = "{0} -d \"%1\" -s".format(application_path)
		else:
			application_path = os.path.abspath(__file__)
			query = "python \"{0}\" -s -d  \"%1\"".format(application_path)
			print (query)
		define_action_on("Directory", "Sorty", query, title="Sort Files")
	main()