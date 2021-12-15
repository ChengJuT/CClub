#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:37:49 2021

@author: LiamTsai
"""

import wx
import wx.html as html
import wx.html2 as html2
import wx.lib.agw.hyperlink as hl

# Hiiiiaaaaaa
# mdkmamdgiaoi;sd
AREA = {
        "Taipei" : 0,
        "New Taiper City" : 1,
        "Other" : 2,
        "AAAA" : 3,
        "MASJFI" : 4
        }


class HomepagePanel(wx.Panel):
    #Layout
    
    # Title
    # Butt1, Butt2, Butt3
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # The vbox of the panel
        self.panel_box = wx.BoxSizer(wx.VERTICAL)
        # Text 
        self.text = wx.StaticText(self, label = "Choose pls")
        self.panel_box.Add(self.text)
        # Button container
        self.areaButt_box = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_box.Add(self.areaButt_box, 1,  wx.EXPAND, 1)
        ## Buttons
        self.area_butts = [] # List of area buttons
        for area_name, area_id in zip(AREA.keys(), AREA.values()):
            self.area_butts.append(wx.Button(self, label = area_name))
            self.area_butts[area_id].Bind(wx.EVT_BUTTON, self.SelectArea)
            self.areaButt_box.Add(self.area_butts[area_id], 1,  wx.EXPAND, 1)
                    
        
        self.SetSizer(self.panel_box)
        self.Show()
        self.Hide()
        
    def SelectArea(self, event):
        butt = event.GetEventObject()
        self.Hide()
        self.parent.SelectArea(butt.Label)
        
class AreaDetailPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Sizer
        self.panel_box = wx.BoxSizer(wx.VERTICAL)
        # Title text
        self.text = wx.StaticText(self, label = "area name")
        self.panel_box.Add(self.text)
        # Exit button
        self.exit_butt = wx.Button(self, label = "Back")
        self.exit_butt.Bind( wx.EVT_BUTTON, self.OnClick_exit_butt)
        self.panel_box.Add(self.exit_butt)
        
        '''
        # Map image
        imgPath = "./map.png"
        img = wx.Image(imgPath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.map = wx.StaticBitmap(self, bitmap = img, size = (img.GetWidth()/1000, img.GetHeight()/1000))
        self.panel_box.Add(self.map)
        # Buttons on map
        self.map_butt =  wx.Button(self, label = "Test")
        self.map_butt.Bind( wx.EVT_BUTTON, self.SelectLocation)
        self.map_butt.Position = 50, 170
        #'''
        
        #'''
        txt_style = wx.VSCROLL|wx.HSCROLL|wx.TE_READONLY|wx.BORDER_SIMPLE
        self.htmlViewer = html.HtmlWindow(self, -1, size=(300, 150), style=txt_style)
        self.htmlViewer.LoadPage("./map.html")
        self.panel_box.Add(self.htmlViewer,1, wx.EXPAND, 1)
        #'''
        
        '''
        self.browser = wx.html2.WebView.New(self)
        self.panel_box.Add(self.browser, 1, wx.EXPAND, 10)
        self.browser.LoadURL("http://www.google.com") 
        #'''
        
        self.SetSizer(self.panel_box)
        self.Show()
        self.Hide()
        
    def SelectLocation(self,event):
        butt = event.GetEventObject()
        butt.Position = (butt.Position[0] + 5, butt.Position[1])
        self.browser.Show()
        
    def Open(self, areaName):
        self.text.Label = areaName
        self.Show()
    
    def OnClick_exit_butt(self, event):
        self.Hide()
        self.parent.ReturnHome()
        
        

class Main_frame(wx.Frame):
    def __init__(self):
        super().__init__(None)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.homepage_panel = HomepagePanel(self)
        self.areaDetail_panel = AreaDetailPanel(self)
        
        vbox.Add(self.homepage_panel)
        vbox.Add(self.areaDetail_panel)
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