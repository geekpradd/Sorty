# A sample context menu handler.
# Adds a menu item with sub menu to all files and folders, different options inside specified folder. 
# When clicked a list of selected items is displayed.
#
# To demostrate:
# * Execute this script to register the context menu. `python context_menu.py --register`
# * Restart explorer.exe- in the task manager end process on explorer.exe. Then file > new task, then type explorer.exe
# * Open Windows Explorer, and browse to a file/directory.
# * Right-Click file/folder - locate and click on an option under 'Menu options'.

import os
import pythoncom
from win32com.shell import shell, shellcon
import win32gui
import win32con
import win32api

class ShellExtension:
    _reg_progid_ = "Python.ShellExtension.ContextMenu"
    _reg_desc_ = "Python Sample Shell Extension (context menu)"
    _reg_clsid_ = "{CED0336C-C9EE-4a7f-8D7F-C660393C381F}"
    _com_interfaces_ = [shell.IID_IShellExtInit, shell.IID_IContextMenu]
    _public_methods_ = shellcon.IContextMenu_Methods + shellcon.IShellExtInit_Methods

    def Initialize(self, folder, dataobj, hkey):
        print "Init", folder, dataobj, hkey
        win32gui.InitCommonControls()
        self.brand= "Menu options"
        self.folder= "C:\\Users\\Paul\\"
        self.dataobj = dataobj
        self.hicon= self.prep_menu_icon(r"C:\path\to\icon.ico")


    def QueryContextMenu(self, hMenu, indexMenu, idCmdFirst, idCmdLast, uFlags):
        print "QCM", hMenu, indexMenu, idCmdFirst, idCmdLast, uFlags

        # Query the items clicked on
        files= self.getFilesSelected()

        fname = files[0]
        idCmd = idCmdFirst

        isdir= os.path.isdir(fname)
        in_folder= all([f_path.startswith(self.folder) for f_path in files])

        win32gui.InsertMenu(hMenu, indexMenu,
            win32con.MF_SEPARATOR|win32con.MF_BYPOSITION,
            0, None)
        indexMenu += 1

        menu= win32gui.CreatePopupMenu()
        win32gui.InsertMenu(hMenu,indexMenu,win32con.MF_STRING|win32con.MF_BYPOSITION|win32con.MF_POPUP,menu,self.brand)
        win32gui.SetMenuItemBitmaps(hMenu,menu,0,self.hicon,self.hicon)
#        idCmd+=1
        indexMenu+=1

        if in_folder:
            if len(files) == 1:
                if isdir:
                    win32gui.InsertMenu(menu,0,win32con.MF_STRING,idCmd,"Item 1"); idCmd+=1
                else:
                    win32gui.InsertMenu(menu,0,win32con.MF_STRING,idCmd,"Item 2")
                    win32gui.SetMenuItemBitmaps(menu,idCmd,0,self.hicon,self.hicon)
                    idCmd+=1
        else:
            win32gui.InsertMenu(menu,0,win32con.MF_STRING,idCmd,"Item 3")
            win32gui.SetMenuItemBitmaps(menu,idCmd,0,self.hicon,self.hicon)
            idCmd+=1

        if idCmd > idCmdFirst:
            win32gui.InsertMenu(menu,1,win32con.MF_SEPARATOR,0,None)

        win32gui.InsertMenu(menu,2,win32con.MF_STRING,idCmd,"Item 4")
        win32gui.SetMenuItemBitmaps(menu,idCmd,0,self.hicon,self.hicon)
        idCmd+=1
        win32gui.InsertMenu(menu,3,win32con.MF_STRING,idCmd,"Item 5")
        win32gui.SetMenuItemBitmaps(menu,idCmd,0,self.hicon,self.hicon)
        idCmd+=1

        win32gui.InsertMenu(menu,4,win32con.MF_SEPARATOR,0,None)

        win32gui.InsertMenu(menu,5,win32con.MF_STRING|win32con.MF_DISABLED,idCmd,"Item 6")
        win32gui.SetMenuItemBitmaps(menu,idCmd,0,self.hicon,self.hicon)
        idCmd+=1

        win32gui.InsertMenu(hMenu, indexMenu,
                            win32con.MF_SEPARATOR|win32con.MF_BYPOSITION,
                            0, None)
        indexMenu += 1
        return idCmd-idCmdFirst # Must return number of menu items we added.

    def getFilesSelected(self):
        format_etc = win32con.CF_HDROP, None, 1, -1, pythoncom.TYMED_HGLOBAL
        sm = self.dataobj.GetData(format_etc)
        num_files = shell.DragQueryFile(sm.data_handle, -1)
        files= []
        for i in xrange(num_files):
            fpath= shell.DragQueryFile(sm.data_handle,i)
            files.append(fpath)
        return files

    def prep_menu_icon(self, icon): #Couldn't get this to work with pngs, only ico
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def InvokeCommand(self, ci):
        mask, hwnd, verb, params, dir, nShow, hotkey, hicon = ci
        win32gui.MessageBox(hwnd, str(self.getFilesSelected()), "Wow", win32con.MB_OK)

    def GetCommandString(self, cmd, typ):
        # If GetCommandString returns the same string for all items then
        # the shell seems to ignore all but one.  This is even true in
        # Win7 etc where there is no status bar (and hence this string seems
        # ignored)
        return "Hello from Python (cmd=%d)!!" % (cmd,)

def DllRegisterServer():
    import _winreg
    folder_key = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,
    "Folder\\shellex")
    folder_subkey = _winreg.CreateKey(folder_key, "ContextMenuHandlers")
    folder_subkey2 = _winreg.CreateKey(folder_subkey, "PythonSample")
    _winreg.SetValueEx(folder_subkey2, None, 0, _winreg.REG_SZ,
    ShellExtension._reg_clsid_)

    file_key = _winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,
    "*\\shellex")
    file_subkey = _winreg.CreateKey(file_key, "ContextMenuHandlers")
    file_subkey2 = _winreg.CreateKey(file_subkey, "PythonSample")
    _winreg.SetValueEx(file_subkey2, None, 0, _winreg.REG_SZ,
    ShellExtension._reg_clsid_)

    print ShellExtension._reg_desc_, "registration complete."

def DllUnregisterServer():
    import _winreg
    try:
        folder_key = _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT,

        "Folder\\shellex\\ContextMenuHandlers\\PythonSample")
        file_key = _winreg.DeleteKey(_winreg.HKEY_CLASSES_ROOT,

        "*\\shellex\\ContextMenuHandlers\\PythonSample")
    except WindowsError, details:
        import errno
        if details.errno != errno.ENOENT:
            raise
    print ShellExtension._reg_desc_, "unregistration complete."

if __name__=='__main__':
    from win32com.server import register
    register.UseCommandLine(ShellExtension,
                   finalize_register = DllRegisterServer,
                   finalize_unregister = DllUnregisterServer)