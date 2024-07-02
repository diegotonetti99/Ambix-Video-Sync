import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

from ambix_video_sync import align, merge, inject, clear

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(1200, 800))

        # Create a panel
        panel = wx.Panel(self)

        # Create a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        # IMPORT AUDIO BUTTON
        # Create an horizontal box for each file entry
        hboxa = wx.BoxSizer(wx.HORIZONTAL)
        # Create a import audio button
        self.audio_button = wx.Button(panel, label="Import Audio")
        hboxa.Add(self.audio_button, flag= wx.ALL , border=10)
        # Bind the button click event to the update methods
        self.audio_button.Bind(wx.EVT_BUTTON, self.import_audio)
        # Create a text entry for audio
        self.audio_box = wx.TextCtrl(panel)
        hboxa.Add(self.audio_box, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(hboxa, flag=wx.EXPAND)

        # IMPORT VIDEO BUTTON
        hboxv = wx.BoxSizer(wx.HORIZONTAL)
        self.video_button = wx.Button(panel, label="Import Video")
        hboxv.Add(self.video_button, flag=wx.ALL , border=10)
        self.video_button.Bind(wx.EVT_BUTTON, self.import_video)
        self.video_box = wx.TextCtrl(panel)
        hboxv.Add(self.video_box, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(hboxv, flag=wx.EXPAND)

        # Create a Matplotlib figure and axis
        self.figure = Figure()
        self.ax = self.figure.subplots(2,1, sharex=True)
        self.ax[0].set_title('Ambix')
        self.ax[1].set_title('Video')
        self.ax[1].set_xlabel('samples')

        # Create a canvas to display the plot
        self.canvas = FigureCanvas(panel, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        vbox.Add(self.toolbar, flag=wx.LEFT | wx.TOP)
        vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)

        # EXPORt VIDEO BUTTON
        hboxe = wx.BoxSizer(wx.HORIZONTAL)
        self.output_button = wx.Button(panel, label="Output Video")
        hboxe.Add(self.output_button, flag=wx.ALL , border=10)
        self.output_button.Bind(wx.EVT_BUTTON, self.output_video)
        self.output_box = wx.TextCtrl(panel)
        hboxe.Add(self.output_box, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        self.export_button = wx.Button(panel, label="Start Export")
        hboxe.Add(self.export_button, flag = wx.ALL, border=10)
        self.export_button.Bind(wx.EVT_BUTTON, self.export_video)
        vbox.Add(hboxe, flag=wx.EXPAND)

        # Set the sizer for the panel
        panel.SetSizer(vbox)

        # Center the frame on the screen
        self.Centre()

    def import_audio(self, event):
        with wx.FileDialog(self, "Open WAV file", wildcard="WAV files (*.wav;*.WAV)|*.wav;*.WAV|All files (*.*)|*.*",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.audio_box.Clear()
            self.audio_box.WriteText(pathname)

    def import_video(self, event):
        with wx.FileDialog(self, "Open MP4 file", wildcard="MP4 files (*.mp4;*.MP4)|*.mp4;*.MP4|All files (*.*)|*.*",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.video_box.Clear()
            self.video_box.WriteText(pathname)

    def output_video(self, event):
        with wx.FileDialog(self, "Open MP4 file", wildcard="MP4 files (*.mp4;*.MP4)|*.mp4;*.MP4|All files (*.*)|*.*",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.output_box.Clear()
            self.output_box.WriteText(pathname)

    def export_video(self, event):
        # temporary file - no need to edit
        video_audio = 'video_audio.wav'
        trimmed_ambix = 'trimmed_ambix.wav'
        merged_video = 'merged.mov'

        input_video = self.video_box.GetLineText(0)
        input_ambix = self.audio_box.GetLineText(0)
        output_video = self.output_box.GetLineText(0)

        # align the ambix audio with the video audio and trim the excess
        ambisonics_trimmed, audio_video_a = align(input_video, input_ambix, video_audio, trimmed_ambix)

        # # plot 
        self.ax[0].plot(ambisonics_trimmed[0])
        self.ax[1].plot(audio_video_a)
        self.canvas.draw()

        merge(input_video, trimmed_ambix, merged_video)

        inject(merged_video, output_video)

        clear(merged_video, trimmed_ambix, video_audio)

        dialog = wx.MessageDialog(self, "Export completed", "Info", wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="Ambix Video Sync")
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
