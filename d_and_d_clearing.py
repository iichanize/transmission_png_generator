# -*- coding: utf-8 -*-

import wx
import os
import cv2
import numpy as np

class ImagePanel(wx.Panel):
    def __init__(self, parent, panel_size):
        wx.Panel.__init__(self, parent)
        self.panel_size = panel_size
        self.rangeMin=[0,0,0]
        self.rangeMax=[0,0,0]
        self.load_image()
        self.image_path
        self.image_ctrl
        self.img_height
        self.img_width
    # -------------------------------------------------------------------------

    def load_image(self, input_image=''):
        if input_image == '':
            image = 'input.png'
        else:
            image = input_image
        self.image_path = image
        img = wx.Image(image)
        backimg = wx.Image('Empty.png')
        #Newimg = img.Scale(self.panel_size[0], self.panel_size[1], wx.IMAGE_QUALITY_HIGH)
        height = img.GetHeight()
        width = img.GetWidth()
        if (height > width)and(height > self.panel_size[1]):
            Newimg = img.Scale(self.panel_size[0]*width/height, self.panel_size[1], wx.IMAGE_QUALITY_HIGH)
        elif (width > height)and(width > self.panel_size[0]):
            Newimg = img.Scale(self.panel_size[0], self.panel_size[1]*height/width, wx.IMAGE_QUALITY_HIGH)
        elif (width == height)and(width > self.panel_size[0]):
            Newimg = img.Scale(self.panel_size[0], self.panel_size[1], wx.IMAGE_QUALITY_HIGH)
        else:
            Newimg = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        self.img_width = Newimg.GetWidth()
        self.img_height = Newimg.GetHeight()
        self.back_image = wx.StaticBitmap(self, -1, wx.Bitmap(backimg))
        self.image_ctrl = wx.StaticBitmap(self, -1, wx.Bitmap(Newimg))
        self.cv2_clearing(self.rangeMin,self.rangeMax)

    def cv2_clearing(self,RangeMin,RangeMax):
        cv_image = cv2.imread(self.image_path,-1)
        if cv_image.ndim == 3:  # RGBならアルファチャンネル追加
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2RGBA)
        self.cv_result = cv_image
        height,width,color = cv_image.shape
        for i in range(width):
            for j in range(height):
                if (RangeMin[2] <= cv_image[j,i,0] <= RangeMax[2]) and (RangeMin[1] <= cv_image[j,i,1] <= RangeMax[1]) and (RangeMin[0] <= cv_image[j,i,2] <= RangeMax[0]):
                    self.cv_result[j,i,3] = 0
        cv2.imwrite('result_img.png',self.cv_result)
#        cv2.imshow('work_space', cv_image)
    
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):

        # D&Dされた最後の画像パスを取得し、ImagePanelクラスのメソッドload_imageに渡す.
        dd_input_image_path = filenames[0]
        self.window.load_image(dd_input_image_path)
        return True


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="clearing", size=(400, 600))
        self.p = wx.Panel(self)
        s_text_R = wx.StaticText(self.p, wx.ID_ANY, 'R:')
        s_text_G = wx.StaticText(self.p, wx.ID_ANY, 'G:')
        s_text_B = wx.StaticText(self.p, wx.ID_ANY, 'B:')
        
        text_space1 = wx.StaticText(self.p, wx.ID_ANY, '  ～  ')
        text_space2 = wx.StaticText(self.p, wx.ID_ANY, '  ～  ')
        text_space3 = wx.StaticText(self.p, wx.ID_ANY, '  ～  ')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sliderR = wx.BoxSizer(wx.HORIZONTAL)
        sliderG = wx.BoxSizer(wx.HORIZONTAL)
        sliderB = wx.BoxSizer(wx.HORIZONTAL)

        button = wx.Button(self.p, wx.ID_ANY, 'run')
        button.Bind(wx.EVT_BUTTON, self.convert)
        
        self.sliderR1 = wx.Slider(self.p, style=wx.SL_LABELS)
        self.sliderR2 = wx.Slider(self.p, style=wx.SL_LABELS)
        self.sliderG1 = wx.Slider(self.p, style=wx.SL_LABELS)
        self.sliderG2 = wx.Slider(self.p, style=wx.SL_LABELS)
        self.sliderB1 = wx.Slider(self.p, style=wx.SL_LABELS)
        self.sliderB2 = wx.Slider(self.p, style=wx.SL_LABELS)
        
        self.sliderR1.SetMax(255)
        self.sliderR2.SetMax(255)
        self.sliderG1.SetMax(255)
        self.sliderG2.SetMax(255)
        self.sliderB1.SetMax(255)
        self.sliderB2.SetMax(255)
        
        self.sliderR1.Bind(wx.EVT_SLIDER, self.input_range1)
        self.sliderR2.Bind(wx.EVT_SLIDER, self.input_range2)
        self.sliderG1.Bind(wx.EVT_SLIDER, self.input_range3)
        self.sliderG2.Bind(wx.EVT_SLIDER, self.input_range4)
        self.sliderB1.Bind(wx.EVT_SLIDER, self.input_range5)
        self.sliderB2.Bind(wx.EVT_SLIDER, self.input_range6)
        
        sliderR.Add(s_text_R)
        sliderR.Add(self.sliderR1, wx.GROW)
        sliderR.Add(text_space1)
        sliderR.Add(self.sliderR2, wx.GROW)
        sliderG.Add(s_text_G)
        sliderG.Add(self.sliderG1, wx.GROW)
        sliderG.Add(text_space2)
        sliderG.Add(self.sliderG2, wx.GROW)
        sliderB.Add(s_text_B)
        sliderB.Add(self.sliderB1, wx.GROW)
        sliderB.Add(text_space3)
        sliderB.Add(self.sliderB2, wx.GROW)
        
        self.input_image_panel = ImagePanel(self.p, panel_size=(300, 300))
        self.input_image_panel.back_image.Bind(wx.EVT_LEFT_DOWN, self.MousePos)
        
        sizer.Add(sliderR, flag=wx.GROW | wx.LEFT | wx.RIGHT,border=10)
        sizer.Add(sliderG, flag=wx.GROW | wx.LEFT | wx.RIGHT,border=10)
        sizer.Add(sliderB, flag=wx.GROW | wx.LEFT | wx.RIGHT,border=10)
        
        #self.input_image_panel.Bind(wx.EVT_MOTION, self.MousePos)
        
        sizer.Add(button,flag = wx.SHAPED | wx.ALIGN_RIGHT |wx.RIGHT | wx.UP, border = 10)
        
        sizer.Add(self.input_image_panel, 0, wx.ALL, 50)
        
        self.p.SetSizer(sizer)

        self.rangeMin = [self.sliderB1.GetValue(), self.sliderG1.GetValue(), self.sliderR1.GetValue()]
        self.rangeMax = [self.sliderB2.GetValue(), self.sliderG2.GetValue(), self.sliderR2.GetValue()]
        dt = MyFileDropTarget(self.input_image_panel)
        self.input_image_panel.SetDropTarget(dt)
        self.Center()
        self.Show()

    def convert(self,event):
        self.input_image_panel.load_image(self.input_image_panel.image_path)
#        cv2.imshow('result', self.input_image_panel.cv_result)
    def MousePos(self,event):
        scr_pos = self.p.GetScreenPosition()
        ctr_pos = event.GetPosition()
        pos = self.input_image_panel.back_image.ScreenToClient(ctr_pos)
        relative_pos_x = pos[0] + scr_pos[0] + 50
        relative_pos_y = pos[1] + scr_pos[1] + 203
        print(relative_pos_x,relative_pos_y)
#        if (50 < ctr_pos.x < self.input_image_panel.panel_size[0] + 50) and (166 < ctr_pos.y < self.input_image_panel.panel_size[1] + 166):
        image_temp = cv2.imread(self.input_image_panel.image_path,-1)
        height,width,color = image_temp.shape
#            if (height > width)and(height > self.panel_size[1]):
#                myframe.PickUpColor([image_temp[(pos.y - 200)*height/self.panel_size[1], (pos.x - 50)*width/self.panel_size[0], 0], image_temp[(pos.y - 200)*height/self.panel_size[1], (pos.x - 50)*width/self.panel_size[0], 1], image_temp[(pos.y - 200)*height/self.panel_size[1], (pos.x - 50)*width/self.panel_size[0], 2]])
#            elif (width > height)and(width > self.panel_size[0]):
#                myframe.PickUpColor([image_temp[pos.y - 200, pos.x - 50, 0], image_temp[pos.y - 200, pos.x - 50, 1], image_temp[pos.y - 200, pos.x - 50, 2]])
#            elif (width == height)and(width > self.panel_size[0]):
#                myframe.PickUpColor([image_temp[pos.y - 200, pos.x - 50, 0], image_temp[pos.y - 200, pos.x - 50, 1], image_temp[pos.y - 200, pos.x - 50, 2]])
#            else:
#                myframe.PickUpColor([image_temp[pos.y - 200, pos.x - 50, 0], image_temp[pos.y - 200, pos.x - 50, 1], image_temp[pos.y - 200, pos.x - 50, 2]])
        myframe.PickUpColor([image_temp[int((relative_pos_y)*height/self.input_image_panel.img_height), int((relative_pos_x)*width/self.input_image_panel.img_width), 0], \
            image_temp[int((relative_pos_y)*height/self.input_image_panel.img_height), int((relative_pos_x)*width/self.input_image_panel.img_width), 1], \
                image_temp[int((relative_pos_y)*height/self.input_image_panel.img_height), int((relative_pos_x)*width/self.input_image_panel.img_width), 2]])

    def input_range1(self, event):
        obj = event.GetEventObject()
        self.rangeMin[0] = obj.GetValue()
        self.input_image_panel.rangeMin[0] = self.rangeMin[0]
    def input_range2(self, event):
        obj = event.GetEventObject()
        self.rangeMax[0] = obj.GetValue()
        self.input_image_panel.rangeMax[0] = self.rangeMax[0]
    def input_range3(self, event):
        obj = event.GetEventObject()
        self.rangeMin[1] = obj.GetValue()
        self.input_image_panel.rangeMin[1] = self.rangeMin[1]
    def input_range4(self, event):
        obj = event.GetEventObject()
        self.rangeMax[1] = obj.GetValue()
        self.input_image_panel.rangeMax[1] = self.rangeMax[1]
    def input_range5(self, event):
        obj = event.GetEventObject()
        self.rangeMin[2] = obj.GetValue()
        self.input_image_panel.rangeMin[2] = self.rangeMin[2]
    def input_range6(self, event):
        obj = event.GetEventObject()
        self.rangeMax[2] = obj.GetValue()
        self.input_image_panel.rangeMax[2] = self.rangeMax[2]

    def PickUpColor(self,colorlist):
        self.sliderR1.SetValue(colorlist[2])
        self.sliderR2.SetValue(colorlist[2])
        self.sliderG1.SetValue(colorlist[1])
        self.sliderG2.SetValue(colorlist[1])
        self.sliderB1.SetValue(colorlist[0])
        self.sliderB2.SetValue(colorlist[0])
        self.input_image_panel.rangeMin = [colorlist[2],colorlist[1],colorlist[0]]
        self.input_image_panel.rangeMax = [colorlist[2],colorlist[1],colorlist[0]]

if __name__ == '__main__':
    app = wx.App()
    myframe = MyFrame()
    app.MainLoop()