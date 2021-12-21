#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:37:49 2021

@author: LiamTsai
"""

import wx
import wx.html as html
import wx.html2 as html2

# Hiiii
AREA = {
        "Taipei" : 0,
        "New Taiper City" : 1,
        "Other" : 2,
        "AAAA" : 3,
        "MASJFI" : 4,
        "c" : 5,
        "d" : 6
        }

MAPS = {
        0 : "./map.html",
        1 : "./map.html",
        2 : "./map.html",
        3 : "./map.html",
        4 : "./map.html",
        5 : "./map.html",
        6 : "./map.html",
        } 

MAPS2 = {
        0 : "file:///Users/LiamTsai/Documents/Github/CClub/CClub/Interface/map.html",
        1 : "https://www.google.com/",
        2 : "file:///Users/LiamTsai/Documents/Github/CClub/CClub/Interface/map.html",
        3 : "file:///Users/LiamTsai/Documents/Github/CClub/CClub/Interface/map.html",
        4 : "https://www.youtube.com/watch?v=3AvnZ_Wt47s",
        5 : "file:///Users/LiamTsai/Documents/Github/CClub/CClub/Interface/map.html",
        6 : "file:///Users/LiamTsai/Documents/Github/CClub/CClub/Interface/map.html",
        } 

windowSize = (400,300)


class HomepagePanel(wx.Panel):
    #Layout
    
    # Title
    # Butt1, Butt2, Butt3
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # The vbox of the panel
        self.panel_box = wx.BoxSizer(wx.VERTICAL)
        # Title text 
        imgSize= (120,120)
        img = wx.Image("./title.png").Scale(imgSize[0], imgSize[1])
        self.titleBG = wx.StaticBitmap(self, -1, img.ConvertToBitmap(), pos = (int(windowSize[0]/2-imgSize[0]/2),-20))
        self.text = wx.StaticText(self, label = "Choose pls", style = wx.CENTER )
        self.text.SetForegroundColour(wx.Colour(255,255,255))
        self.panel_box.Add(self.text, 1, wx.ALIGN_CENTER_HOＲIZONTAL|wx.ALL, int(imgSize[1]/3 - 3))
      

        self.dialog = HTML_frame2(self, -1)
        
        
        nButts = 0;
        nButtsPerRow = 3;
        # Button container
        self.areaButt_box = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_box.Add(self.areaButt_box, 1, flag = wx.EXPAND, border = 0)
        ## Buttons
        self.area_butts = [] # List of area buttons
        
        
        for area_name, area_id in zip(AREA.keys(), AREA.values()):
            if(nButts == nButtsPerRow):
                self.areaButt_box = wx.BoxSizer(wx.HORIZONTAL)
                self.panel_box.Add(self.areaButt_box, 1, flag = wx.EXPAND|wx.BOTTOM, border = 10)
                nButts = 0
            butt = wx.Button(self, label = area_name, size = (self.GetSize()[0]//3, 10 ))
            self.area_butts.append(butt)
            butt.Bind(wx.EVT_BUTTON, self.SelectArea)
            
            self.areaButt_box.Add(butt, 1, flag = wx.EXPAND|wx.ALL, border = 5)
            nButts += 1
        if(nButts < nButtsPerRow):
            for i in range(nButtsPerRow - nButts):
                butt = wx.Button(self, label = "", size = (self.GetSize()[0]//3, 10 ))
                self.areaButt_box.Add(butt, 1, flag = wx.EXPAND|wx.ALL, border = 5)
                butt.Disable()
            
        
        self.SetSizer(self.panel_box)
        self.Show()
        self.Hide()
        
    def SelectArea(self, event):
        butt = event.GetEventObject()
        self.dialog.browser.LoadURL(MAPS2[AREA[butt.Label]])
        self.dialog.title = butt.Label
        self.dialog.Show();
        
class HTML_frame(wx.Frame):
    def __init__(self, title, webPage):
        super().__init__(None)
        self.SetTitle(title)
        
        self.panel_box = wx.BoxSizer(wx.VERTICAL)
        
        txt_style = wx.VSCROLL|wx.HSCROLL|wx.TE_READONLY|wx.BORDER_SIMPLE
        self.htmlViewer = html.HtmlWindow(self, -1, size=(300, 150), style=txt_style)
        self.htmlViewer.LoadPage(webPage)
        self.panel_box.Add(self.htmlViewer,1, wx.EXPAND, 1)
        
        self.Show()
        self.Layout()
        self.Refresh()
  
class HTML_frame2(wx.Dialog): 
  def __init__(self, *args, **kwds): 
    wx.Dialog.__init__(self, *args, **kwds) 
    sizer = wx.BoxSizer(wx.VERTICAL) 
    self.browser = wx.html2.WebView.New(self) 
    sizer.Add(self.browser, 1, wx.EXPAND, 10) 
    self.SetSizer(sizer) 
    self.SetSize((700, 700)) 

class Main_frame(wx.Frame):
    def __init__(self):
        super().__init__(None, size = windowSize ,style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetBackgroundColour(wx.Colour(219, 80, 74))
        
        #background
        '''
        scale = 0.4
        bgSize = (1680 * scale,1120*scale)
        img = wx.Image("./bg.jpeg").Scale(bgSize[0],bgSize[1]).ConvertToBitmap()
        self.bg = wx.StaticBitmap(self, -1, img, (0, -170))
        '''
        scale = 0.6
        bgSize = (int(800 * scale),int(533*scale))
        img = wx.Image("./bg2.jpeg").Scale(bgSize[0],bgSize[1]).ConvertToBitmap()
        self.bg = wx.StaticBitmap(self, -1, img, (-70, 0))

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.homepage_panel = HomepagePanel(self)
        vbox.Add(self.homepage_panel, 0, flag = wx.EXPAND, border = 0)
        self.SetSizer(vbox)
        self.Show()
        self.homepage_panel.Show()
        self.Layout()
        self.Refresh()
    
    def SelectArea(self, areaName):
        self.areaDetail_panel.Open(areaName)
        self.Layout()
        self.Refresh()
        
    def ReturnHome(self):
        self.homepage_panel.Show()
        self.Layout()
        self.Refresh()
        


app = wx.App()
Main_frame()
app.MainLoop()