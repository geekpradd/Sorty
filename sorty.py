"""
Sorty: A File Sorting Magician for your Computer

Sorty sorts files in your current working folder based on the Extension name.
All .exe files are stored in a separate "EXE Files" folder, .pdf files are stored in "PDF Files" Folder etc


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
		return {folder:list(filter(lambda x:"." in x,[files for files in os.listdir(folder)]))}
	return dict([(root,files) for root, dirs,files in os.walk(folder)])

def run_script(folder,topdown):
	"""
	Run the core script by getting the files and iterating over the dictionary
	
	If the file is already sorted then ignore it else sort it out and move the files.

	"""
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
	
	parser.add_argument('-d','--directory',help="Use this parameter to change the working directory")
	parser.add_argument('--topdown',dest='feature', action='store_true',help="Use this paramter to sort files in subfolders")
	parser.set_defaults(feature=False)

	args=parser.parse_args()
	if args.directory:
		path = os.path.expanduser(args.directory)
		if os.path.isdir(path):
			os.chdir(path)
		else:
			if 'n' in input("Invalid Directory. Use Current Directory in Script? ").lower():
				sys.exit(0)

	run_script(os.getcwd(),bool(args.feature))
	
if __name__=='__main__':
	main()