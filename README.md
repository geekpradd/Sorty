##Sorty

A file sorting magician in your command line. Sorty sorts files in a folder by their extensions and organizes stuff. Sorty is built in Python and works cross platform and on both Python 2 and 3. 

###Why Sorty?

Sorty shouldn't be used in project folders or code folders. It's better for organising folders like Downloads, Pictures, Trip Media etc.

For example, we download a lot of stuff in our computers. Most of the time, our download folder is a mess. 

But worry not because Sorty is here!. Sorty sorts your files based on your extensions and groups similar files together. So your program setup files are in one folder, your PDF documents are in one, and your downloaded songs are in another. You can then rename these folders to suit yourself.

Another Example, whenever we go out for a holiday or a trip, we take a lot of pictures and videos. But when we import our files from our Camera or Smartphone, the videos and pictures are grouped together. And separating them takes time especially when we have many files. Again, Sorty to the rescue!. Sorty will group your videos separately and your pictures separately. 

###Installation

####Cross Platform

You need to have Python installed for this method. It will work on Windows, Unix/Linux and Mac OS X.

Use `pip` to install:

```
pip install sorty
```

####Installer

The Installer is coming soon for Windows. It will be a small exe that you need to place in your system folder and you are good to go.

Linux and Mac OS X don't get a compiled executable because Python is pre installed in these systems


###Usage

Navigate to the Folder which you want to sort in your Terminal/Command Prompt

Enter the following command:

```
sorty
```

And the Magic will start. By default Sorty does not sort files contained in subfolders but if you want that, just add the `--topdown` argument so that the command becomes:

```
sorty --topdown
```

Alternatively instead of navigating to the folder, you can let sorty do that for you using the `directory` argument.

```
sorty -d "C:\Pictures" --topdown
```

###Dependencies

If you have Python >2.7 and >3.2 then there are no external dependencies. To Support Python 2.5 - 2.6 and 3.0 - 3.1, the `argparse` module is required. If you are installing using pip then don't worry, everything will be installed automatically.

###About

Created By Pradipta. Copyright 2015 MIT Licensed.