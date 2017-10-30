import wx.media
import os



class MainWindow(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Music Player',size=(700,560),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        wx.Frame.CenterOnScreen(self)
        
       
        

        self.currentVolume =10
        #bg = wx.Image('images2.JPG', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.bitmap1 = wx.StaticBitmap(self, -1, bg, (0,0))
        panel = wx.Panel(self,-1)
        self.panel = panel
       
        
        self.panel.SetBackgroundColour(wx.BLUE)

        

        ##MENU AND STATUS BAR
        self.status = self.CreateStatusBar()
        self.status.SetStatusText('Ready')
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        view_menu = wx.Menu()
        controls_menu = wx.Menu()
        help_menu = wx.Menu()

        #MENU ID'S
        ID_FILE_LOAD = 2
        ID_FILE_EXIT = 3

        ID_VIEW_SHOW_STATUSBAR = 4

        ID_CONTROLS_PLAY = 5
        ID_CONTROLS_PAUSE = 6
        ID_CONTROLS_STOP = 7

        ID_HELP_ABOUT = 8

        ##FILE MENU
        file_menu.Append(ID_FILE_LOAD, "&LOAD...\tCtrl+L", "This will let you choose a song to load")
        file_menu.AppendSeparator()
        file_menu.Append(ID_FILE_EXIT,"Exit","This will exit the program")

        ##VIEW MENU
        self.check_statusbar = view_menu.Append(ID_VIEW_SHOW_STATUSBAR,'Show Stat&usbar\tCtrl+U', "This will disable the statusbar", kind=wx.ITEM_CHECK)
        view_menu.Check(self.check_statusbar.GetId(), True)

        ##CONTROLS MENU
        controls_menu.Append(ID_CONTROLS_PLAY,"&Play\tEnter", "Play the selected song")
        controls_menu.Append(ID_CONTROLS_PAUSE,"&Pause\tSpace", "Pause the selected song")

        help_menu.Append(ID_HELP_ABOUT,"&About","About player")

        ##MENUBAR APPEND
        menubar.Append(file_menu,"File")
        menubar.Append(view_menu,"View")
        menubar.Append(controls_menu,"Controls")
        menubar.Append(help_menu,"Help")
        self.SetMenuBar(menubar)

        ##MENU ACTION BINDING
        self.Bind(wx.EVT_MENU, self.Load, None, 2)        
        self.Bind(wx.EVT_MENU, self.Close, None, 3)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.check_statusbar)
        self.Bind(wx.EVT_MENU, self.Play, None, 5)
        self.Bind(wx.EVT_MENU, self.Pause, None, 6)
        self.Bind(wx.EVT_MENU, self.About, None, 8)

        ##FONTS
        font1 = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        try:
            self.mc = wx.media.MediaCtrl(self)
        except NotImplementedError:
            raise

        ##BUTTONS

        bttnprt = panel

        loadButton = wx.Button(bttnprt, -1, "open file...", pos=(235,400), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.Load, loadButton)

        playButton = wx.Button(bttnprt, -1, "Play", pos=(330,440), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.Play, playButton)

        pauseButton = wx.Button(bttnprt, -1, "Pause", pos=(410,440), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.Pause, pauseButton)

        volumeUpButton = wx.Button(bttnprt, -1, "Up", pos=(330,400), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.onSetVolumeUp, volumeUpButton)

        volumeDownButton = wx.Button(bttnprt, -1, "Down", pos=(410,400), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.onSetVolumeDown, volumeDownButton)

        backButton = wx.Button(bttnprt, -1, "Back", pos=(235,440), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.previousSong, backButton)

        nextButton = wx.Button(bttnprt, -1, "Next", pos=(500,440), size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.nextSong, nextButton)
        

        
        slider2 = wx.Slider(bttnprt, -1, 0, 0, 100, size=(90, -1),pos=(500,400))
        self.volumeCtrl = slider2
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.onSetVolume)

        #songlist = os.listdir('songs')
        self.myListBox = listbox = wx.ListBox(bttnprt, -1,pos=(0,5),size=(200,480), style=wx.LB_SINGLE)

        self.Bind(wx.EVT_LISTBOX, self.selLoadFile, listbox)

        #self.st_file = wx.StaticText(bttnprt, -1, "Blank", pos=(30,30))

    """def newWin(self, event):
        self.new = NewWindow(parent=self, id=-1)
        self.new.Show()"""

    
        
    def Close(self, event):
        box=wx.MessageDialog(None, 'Are you sure you want to exit?', 'Exit program?', wx.YES_NO)
        answer=box.ShowModal()
        if answer==wx.ID_YES:
            self.Destroy()

    def About(self, event):
        self.new = wx.Frame(parent=self, id=-1)
        self.new.Show()
        

    def selLoadFile(self, event):
            my_selection = self.myListBox.GetStringSelection()
            folder, filename = os.path.split(self.path)
            file_path = os.path.join(folder,my_selection)
            
            self.doLoadFile2(file_path)
            #self.doLoadFile2(my_selection)
           

    def Load(self, event):
        dlg = wx.FileDialog(self, "Choose a media file", "songs", "", "*.mp3", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.path = path
            self.doLoadFile(self.path)
            dlg.Destroy() 

    def load2(self):
            my_selection = self.myListBox.GetStringSelection()
            #file_path = os.path.join(os.getcwd(),"songs",my_selection)
            folder, filename = os.path.split(self.path)
            file_path = os.path.join(folder,my_selection)
            self.doLoadFile2(file_path)
            #self.doLoadFile2(my_selection)
            
            self.mc.Play()

    def doLoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)

        else:
            folder, filename = os.path.split(path)
            self.myListBox.Append(filename)
            #self.myListBox = listbox = wx.ListBox(bttnprt, -1, (301,80), (296,206), filename, wx.LB_SINGLE)
            self.mc.SetInitialSize()
            self.mc.Play()

    def doLoadFile2(self, file_path):
        if not self.mc.Load(file_path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % file_path, "ERROR", wx.ICON_ERROR | wx.OK)

        else:
            folder, filename = os.path.split(file_path)
            #self.st_file.SetLabel('%s' % filename)
            
            self.status.SetStatusText("Now Playing: " +'%s' % file_path)
            self.mc.SetInitialSize()
            self.mc.Play()

    def Play(self, event):
        self.mc.Play()

    def Pause(self, event):
        self.mc.Pause()

    def onSetVolumeUp(self, event):

        self.currentVolume = self.volumeCtrl.GetValue()
        self.newVolumeAdd = self.currentVolume + 1.5
        self.volumeCtrl.SetValue(self.newVolumeAdd)

        self.mc.SetVolume(float(self.currentVolume) / 100)

    def onSetVolumeDown(self, event):
        self.currentVolume = self.volumeCtrl.GetValue()
        self.newVolumeSub = self.currentVolume - 1.5
        self.volumeCtrl.SetValue(self.newVolumeSub)

        self.mc.SetVolume(float(self.currentVolume) / 100)

    def previousSong(self, event):
        current = self.myListBox.GetSelection()
        new = current - 1
        self.myListBox.SetSelection(new)
        self.mc.Stop()
        self.load2()

    def nextSong(self, event):
        current = self.myListBox.GetSelection()
        new = current + 1
        self.myListBox.SetSelection(new)
        self.mc.Stop()
        self.load2()

    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        self.mc.SetVolume(self.currentVolume)     

    def ToggleStatusBar(self, e):
        if self.check_statusbar.IsChecked():
            self.status.Show()
            self.status.SetStatusText('Ready')
        else:
            self.status.Hide()

        ##RUN##

if __name__=='__main__':
        app=wx.App()
        frame=MainWindow(parent=None,id=-1)
        frame.Show()
        app.MainLoop()
