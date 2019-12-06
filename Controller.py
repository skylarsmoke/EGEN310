''' RC Car Controller App By: Skylar Smoker and Austin Hull '''

import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.core.window import Window
import socket
from threading import Thread

# Connects to car via Python sockets
class Connect():
    
    def __init__(self, host = "10.200.9.93", port = 1235):
        self.sock = socket.socket()
        Window.bind(on_request_close=self.close_socket) 
        self.sock.connect((host, port))
    
    def close_socket(self, *largs, **kwargs):
        print("\nServer shut down.")
        self.sock.close()

    def get_data(self):
        return self.sock.recv(1024)

class GUI(GridLayout):
    
    #Window.clearcolor = (1, 1, 1, 1)
    
    def __init__(self, **kwargs):
        
        # Toggle to turn off WIFI for development
        self.wifi = True
        
        if self.wifi is True:
            self.sock = Connect()
            Thread(target=self.get_data).start()
        
        # Columns
        self.cols = 2
        
                
        super(GUI, self).__init__(**kwargs)
        
        # Settings Button
        self.speed = Button(text = "HIGH SPEED", font_size = 30, pos=(self.x, self.height))
        self.speed.bind(on_press = self.updateSpeed)
        
        # 4WD Button
        self.wheels = Button(text = "2WD", font_size = 30)
        self.wheels.bind(on_press = self.update4WD)
        
        '''
        # 4 Wheel Turn Button
        self.twoTurn = Button(text = "TURN: 2W", font_size = 30)
        self.twoTurn.bind(on_press = self.updateTurn)
        '''
        
        # Move Slider
        self.move = Slider(orientation='vertical', min = -100, max = 100, value = 0, step = 1, padding = 0)
        self.move.bind(value = self.moveValueChange)
        self.moveLabel = Label(font_size = 30)
        self.move.bind(on_touch_up = self.zeroMove)
        
        # Turn Slider
        self.turn = Slider(orientation = "horizontal", min = 10, max = 100, value = 60, step = 1, padding = 0)
        self.turn.bind(value = self.turnValueChange)
        self.turn.bind(on_touch_up = self.zeroTurn)
        self.turnLabel = Label(font_size = 30)
        
        # Adds GUI features to screen
        self.add_widget(self.speed)
        self.add_widget(self.wheels)
        self.add_widget(self.move)
        self.add_widget(self.turn)
        self.add_widget(self.moveLabel)
        self.add_widget(self.turnLabel)
        #self.add_widget(self.twoTurn)
        
        self.resetValTurn = False
        self.resetValMove = False
    
    
    # Changes turn value to zero when finger is lifted
    def zeroTurn(self, instance, touch):
        self.resetValTurn = True
        self.turn.value = 60
        self.sock.sock.send(bytes("turn " + str(self.turn.value), "utf-8"))
    
    # Changes move value to zero when finger is lifted
    def zeroMove(self, instance, touch):
        self.resetValMove = True
        self.move.value = 0
        self.sock.sock.send(bytes("Move: " + str(self.move.value), "utf-8"))
    
    # Detects turn value change and sends value to car
    def turnValueChange(self, instance, value):
        self.turnLabel.text = str(value)
        if self.resetValTurn is False:
            if value < 0:
                self.sock.sock.send(bytes("turn " + str(value), "utf-8"))
            else:
                self.sock.sock.send(bytes("turn " + str(value), "utf-8"))
        self.resetValTurn = False
    
    # Detects move value change and sends value to car
    def moveValueChange(self, instance, value):
        self.moveLabel.text = str(value)
        if self.resetValMove is False:
            if value < 0:
                self.sock.sock.send(bytes("moveback " + str(value), "utf-8"))
            else:
                self.sock.sock.send(bytes("Move " + str(value), "utf-8"))
        self.resetValMove = False
    
    # used for receiving data from car
    def get_data(self):
        while True:
            self.text = self.sock.get_data()
            
        self.sock.sock.close()
    
    # Used for switching between 4WD and 2WD    
    updateCount = 0
    
    # Sends an update to car to change from 4WD and 2WD
    def update4WD(self, *args):
        self.updateCount += 1
        if self.updateCount % 2 == 0:
            self.wheels.text = "2WD"
            self.sock.sock.send(bytes("2WDrive", "utf-8"))
        else:
            self.wheels.text = "4WD"
            self.sock.sock.send(bytes("4WDrive", "utf-8"))
    
    speedCount = 0
    
    def updateSpeed(self, *args):
        self.speedCount += 1
        if self.speedCount % 2 == 0:
            self.speed.text = "HIGH SPEED"
            self.move.max = 100
            self.move.min = -100
        else:
            self.speed.text = "LOW SPEED"
            self.move.max = 50
            self.move.min = -50
    '''
    turnCount = 0
            
    def updateTurn(self, *args):
        self.turnCount += 1
        if self.turnCount % 2 == 0:
            self.twoTurn.text = "TURN: 2W"
            self.sock.sock.send(bytes("changeturn2W", "utf-8"))
        else:
            self.twoTurn.text = "TURN: 4W"
            self.sock.sock.send(bytes("changeturn4W", "utf-8"))
            '''
            

# (Taken out for lack of update features) Contains all code for pop up menu and settings that can be changed 
'''
class SettingsMenu(object):

    def updateSpeed(self, *args):
        self.speed.text = "HIGH SPEED"
    
    def __init__(self, touch):
        self.layout = BoxLayout(orientation = 'vertical', padding = (10))
        self.exit = Button(text = "EXIT")
        self.speed = Button(text = "LOW SPEED")
        
        self.layout.add_widget(self.speed)
        self.layout.add_widget(self.exit)
    
        
        
        popup = Popup(title='Settings', title_size= (30), 
                      title_align = 'center', content = self.layout,
                      size_hint=(None, None), size=(400, 400),
                      auto_dismiss = True)
        
        self.exit.bind(on_press = popup.dismiss)
        self.speed.bind(on_press = self.updateSpeed)
        
        popup.open()
'''

       
class MyApp(App):

    def build(self):
        self.title = "F5 RC Controller App v1.5"
        self.icon = "icon.png"
        return GUI()


if __name__ == '__main__':
    MyApp().run()
    
    