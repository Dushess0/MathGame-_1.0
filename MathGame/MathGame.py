



#import platform

def w_to_u(number,mode='v'):
    if mode=='v':
        w=1000
        sc=Window.size[0]
    else:
        w=600
        sc=Window.size[1]
    return (number/w)*sc
    
#if platform.platform()=="Windows" or platform.platform()=="Linux":
MODE="normal"
CARD_SIZE=(128,128)
from kivy.config import Config
Config.set('graphics','resizable',False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.core.window import Window
Window.size=(1000,600)
#else:
 #   MODE="phone"
  #  from kivy.core.window import Window
  #  CARD_SIZE=(w_to_u(128),w_to_u(128,''))


    


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.widget import WidgetException
from kivy.uix.layout import Layout
from kivy.graphics import (Color,Rectangle,Line)
from kivy.clock import Clock
from kivy.uix.textinput import TextInput


import copy
import threading
import time
import random
from functools import partial
import json
import socket


from cards import ILOSC_CARD
from cards import NumberCard, EventCard, Brackets, Sorcery, Artifact
from network import NetWork, get_ip_address
from player import Player
IMG_FOLDER="data\\img\\"

BACK_IMG=IMG_FOLDER+"back.jpg"
NUMBER_IMG=IMG_FOLDER+"test.jpg"




def move(widget,x,y):
    y+=widget.height/2
    widget.pos_hint=pixel_to_hint(x,y)
    widget.pos=(x,Window.size[1]-y)
def pixel_to_hint(width,height,mode="tuple",invert=True):
    if invert: 
              height=Window.size[1]-height
    data = width/Window.size[0],height/Window.size[1]
   
    if mode=="tuple":
        return (data)
    elif mode=="dict":    
        return {"x":data[0],"y":data[1]}
def do_something(action,duration,object,smooth=100):
      object.i=0
      def effect(dt):
                    
                        if object.i<smooth:
                            action()
                            object.i+=1
                        else:
                           
                            Clock.unschedule(event)
                            
                

      event=Clock.schedule_interval(effect,(1/smooth)*duration)
def split(data,page,by=10):
        splitted=[]
        showing=[]
        times=0
        if len(data)<=by:
            splitted=[data]
            showing = splitted[0]
        else:

            while times<=len(data)//10:
                splitted.append(data[times*by:(times+1)*by])
               
                times+=1
            try:
              showing = splitted[page]
            except:
                page=0
                showing=splitted[0]
                
        return showing


     

def hint_to_pixel(x,y,mode="tuple",invert=False):
      if mode=="tuple":
        return (x*Window.size[0],y*Window.size[1])
      elif mode=="dict":
           return {"x":x*Window.size[0],"y":y*Window.size[1]}


     
class UI():
    def __init__(self,main):
        self.draw=main.main
        self.comm=main
        self.turn_label=Label(font_size=50,color=(1,0,0,1))
        self.draw.add_widget(self.turn_label)
        self.turn_label.pos=(400,300)
        self.art_labels=[]
        
       
    def show_battle_request(self,data):
         pass
  

    def start_duel(self):
            self.draw.add_widget(self.turn_label)
            move(self.comm.players[0].name,w_to_u(835),w_to_u(180,''))
            move(self.comm.players[1].name,w_to_u(835),w_to_u(420,''))
            move(self.comm.players[0].score,w_to_u(930),w_to_u(225,''))
            move(self.comm.players[1].score,w_to_u(930),w_to_u(375,''))
            with self.draw.canvas:
                Color(1,.27,0)
                Line(points=[0,0,0,w_to_u(160,''),Window.size[0],w_to_u(160,''),Window.size[0],0],width=3,close=True)
                Line(points=[0,Window.size[1],Window.size[0],Window.size[1],Window.size[0],w_to_u(440,''),0,w_to_u(440,'')],width=2,close=True)
               
                Line(points=[w_to_u(830),w_to_u(200,''),w_to_u(830),w_to_u(160,''),Window.size[0],w_to_u(160,''),Window.size[0],w_to_u(200,'')],width=2,close=True)
                Line(points=[w_to_u(830),w_to_u(400,''),w_to_u(830),w_to_u(440,''),Window.size[0],w_to_u(440,''),Window.size[0],w_to_u(400,'')],width=2,close=True)
                
                Line(points=[w_to_u(900),w_to_u(245,''),w_to_u(900),w_to_u(200,''),Window.size[0],w_to_u(200,''),Window.size[0],w_to_u(245,'')],width=2,close=True)
                Line(points=[w_to_u(900),w_to_u(355,''),w_to_u(900),w_to_u(400,''),Window.size[0],w_to_u(400,''),Window.size[0],w_to_u(355,'')],width=2,close=True)


            effects_button=Button(text ="Show Artifacts",on_press=self.show_players_artifacts)
            effects_button.width=w_to_u(170)
            effects_button.height=w_to_u(60,'')
            move(effects_button,0,w_to_u(190,''))
            self.draw.add_widget(effects_button)
            self.turn_button=Button(text ="End Turn",on_press=self.comm.end_turn)
            self.turn_button.width=170
            self.turn_button.height=60


           

            move(self.turn_button,0,w_to_u(410,''))
            self.draw.add_widget(self.turn_button)


            move(self.comm.time,w_to_u(900,''),w_to_u(300,''))
           

          
            self.draw.add_widget(self.comm.time)
            
            
            
            self.comm.players[0].exp.update()
            self.comm.players[1].exp.update()
        
    def load_menu(self,instance=None):

        try:
            with open("data\\settings.json") as file:
                self.comm.settings=json.load(file)
        except:
             print()
             print("WWWWARNING NICKNAME IS VERY IMPORTANT IN SECURITY OF THIS GAME")
             print("PLEASE DONT CHANGE IT IN settings.json")
             print()
             print("REMEMBER : I DONT WANT YOUR DATA, I WANT TO PLAY AND DEVELOP MY GAME")
             print()
             a=input("ENTER YOUR NICKNAME : ")
             while True:
                 b=int(input("ENTER YOUR PORT (from 2000 to 8000): "))
                 if b>=2000 and b<=8000:
                     break

             self.comm.settings={"name":a,"ip":get_ip_address(),"friends":[],"score":[],'port':b}
             with open("data\\settings.json",'w') as file:
               json.dump(self.comm.settings,file)

        img =Image(source="data\\img\\menu.jpg")
        move(img,0,600)
        img.size=(1000,700)
        self.draw.clear_widgets()
        self.draw.add_widget(img)
        self.draw.add_widget(MenuLabel(self.comm,"Hello "+self.comm.settings["name"]))
        self.draw.add_widget(MenuLabel(self.comm,"local"))
        self.draw.add_widget(MenuLabel(self.comm,"multiplayer"))
        self.draw.add_widget(MenuLabel(self.comm,"stats"))
      #  self.draw.add_widget(MenuLabel(self.comm,"food"))
        self.draw.add_widget(MenuLabel(self.comm,"Math Game"))
    def load_multiplayer(self,instance=None):
        self.draw.clear_widgets()
        i=0
        if instance!=None:
            self.page+=1
        else:
            self.page=0
        def add_buttons():

            tmp =Label(text ="Friends",font_size=30)
            move(tmp,50,50)
            self.draw.add_widget(tmp)
            tmp =Label(text ="ONLINE",font_size=30)
            move(tmp,350,50)
            self.draw.add_widget(tmp)
            tmp =Label(text ="STATUS",font_size=30)
            move(tmp,650,50)
            self.draw.add_widget(tmp)


            tmp =Button(text ="Add Friend",size=(250,100),font_size=20,on_press=self.comm.network.friend_invite)
            move(tmp,0,550)
            self.draw.add_widget(tmp)
            tmp =Button(text ="Direct Connection",size=(250,100),font_size=20,on_press=self.comm.network.send_direct_request)
            move(tmp,750,550)
            self.draw.add_widget(tmp)
            tmp =Button(text ="Back",size=(250,100),font_size=20,on_press=self.load_menu)
            move(tmp,250,550)
            self.draw.add_widget(tmp)
            tmp =Button(text ="Next page",size=(250,100),font_size=20)
            move(tmp,500,550)
            self.draw.add_widget(tmp)
        add_buttons()


        showing=  split(self.comm.settings["friends"],self.page) 
        
        for player in showing:
          
            name = Label(text =player["name"],font_size=30)
            
           # online=Label(text =)
            
            self.draw.add_widget(name)
        #    self.draw.add_widget(online)
        #    self.draw.add_widget(status)
            move(name,50,100+i*40)
        #    move(online,300,100+i*40)
         #   move(status,550,100+i*40)

            i+=1
         
    def show_stats(self,instance=None,page=0):
        self.draw.clear_widgets()
        i=0
        if instance!=None:
            self.page+=1
        else:
            self.page=0
        next =Button(text ="NEXT PAGE",on_press=self.show_stats)
        self.draw.add_widget((Button(text ="BACK",on_press=self.load_menu)))
        move(next,900,550)
        self.draw.add_widget(next)
        
        all = []
        temp=[]
        splitted=[]
        
        #sort by winrate
        def get_winrate(data):
            try :
              win = round(data["score"][0]/data["score"][2],5)
            except:
                  win=0
            return win

        self.comm.settings['friends']=sorted(self.comm.settings["friends"],key = get_winrate)
        self.comm.settings["friends"]=self.comm.settings["friends"][::-1]
        


        
         
    


        tmp =Label(text ="NAME",font_size=30)
        move(tmp,50,50)
        self.draw.add_widget(tmp)
        tmp =Label(text ="WINRATE",font_size=30)
        move(tmp,300,50)
        self.draw.add_widget(tmp)
        tmp =Label(text ="WINS/LOSES",font_size=30)
        move(tmp,550,50)
        self.draw.add_widget(tmp)
        tmp =Label(text ="BATTLES",font_size=30)
        move(tmp,800,50)
        self.draw.add_widget(tmp)

       
        showing =split(self.comm.settings["friends"],self.page)
        
        for player in showing:
            ad = str(self.comm.settings["friends"].index(player))+") "
            name = Label(text =ad+player["name"],font_size=30)
            w_t = str(player["score"][0])+"/"+str(player["score"][1])
            wins_loses=Label(text =w_t,font_size=30)
            wr_t=str(get_winrate(player))
            winrate=Label(text =wr_t,font_size=30)

            
            self.draw.add_widget(name)
            self.draw.add_widget(winrate)
            self.draw.add_widget(wins_loses)
            move(name,50,100+i*40)
            move(winrate,300,100+i*40)
            move(wins_loses,550,100+i*40)

            i+=1
    def show_players_artifacts(self,instance):
        
            try:
                for player in self.comm.players:
                    for art in player.artifacts:
                        self.draw.add_widget(art)
                
                
            except WidgetException:
                pass
            Clock.schedule_once(self.change_state,5)
       
    def change_state(self,dt=None):
        for player in self.comm.players:
                    for art in player.artifacts:
                        self.draw.remove_widget(art)
      

    def hide_players_artifacts(self,instance):
       
       for lbl in self.art_labels:
           self.draw.remove_widget(lbl)
           del lbl
       self.art_labels=[]
       Clock.schedule_once(self.change_state,.3)

    def highlight(self,card):
        self.clear_highlight()
       
        if card.type!="artifact" and card.type!="event":
            for player in self.comm.players:
            
                for w in player.exp.widgets:
                    
                    if w.type in card.targets or w.text in card.targets:
                        w.color=(0,1,0,1)

        
            card.color=(1,0,0,1)

    def clear_highlight(self):
        for player in self.comm.players:
            for card in player.hand:
                card.color=(1,1,1,1)
            for w in player.exp.widgets:                
                    w.color=(1,1,1,1)
    def show_turn(self):
         
         def delete(dt,deleter):
             deleter.text=''

         for player in self.comm.players:
             player.name.color=(1,1,1,1)
         output="CURRENT TURN "+str(self.comm.current_turn)+" : "+self.comm.current_player.name.text
         self.turn_label.pos=(Window.size[0]/2-self.turn_label.width/2,Window.size[1]/2-self.turn_label.height/2)
        
         self.comm.current_player.name.color=(1,0,0,1)
         for player in self.comm.players:
             for card in player.hand:
                 card.color=(1,1,1,1)
                 
             for w in player.exp.widgets:
                 w.color=(1,1,1,1)
         self.turn_label.text=output
         
          
         
             
             
         Clock.schedule_once(partial(delete,deleter =self.turn_label),3)

   
    

        
class TimeLabel(Label):
    def __init__(self,main, **kwargs):
         super().__init__(**kwargs)
         self.text ='60'
         self.main = main
         self.time =0
         self.turn_time=60
         self.font_size=50
         Clock.schedule_interval(self.update,0.25)
    def update(self,dt):
        self.time +=dt
        self.delta=self.turn_time-self.time
        self.text =str(int(self.delta))
        if self.delta<=0:
            self.main.end_turn()
           
 

class MenuLabel(Label):
     def __init__(self,main,type, **kwargs):
       super().__init__(**kwargs) 
       self.main = main
       self.output=Label()
      
       self.type=type
       self.text=self.type
       self.font_size=45
       if self.type=="local":
           move(self,40,300)
       elif self.type=="multiplayer":
           move(self,130,400)
       elif self.type=="stats":
           move(self,40,500)
       elif self.type=="food":
           self.font_size=25
           self.text="money for tea"
           self.color=(.6,0,0,1)
           move(self,830,590)
       elif self.type=="Math Game":
            self.color=(.6,0,0,1)
            move(self,450,70)
            self.font_size=80
       else:
            self.font_size=40
            
            move(self,500,200)
       
       
       self.font_name="data\\Fonts\\Red October.ttf"
       
       
       

     def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if self.collide_point(touch.x,touch.y):
            if self.type=="multiplayer":
                self.main.UI.load_multiplayer()
            elif self.type=="local":
                self.main.load_game()
            elif self.type=="stats":
                self.main.UI.show_stats()
            elif self.type=="food":
                
                self.main.show_pay()








class WtF(Layout): 
    def __init__(self, **kwargs):
         super().__init__(**kwargs)
    def do_layout(self, *largs):
        pass

   


class MathApp(App):
    def build(self):
        self.main = WtF()
        self.buffer=None
        self.UI =UI(self)
        self.main.clear_widgets()
        self.UI.load_menu()
        self.network=NetWork(self)
        
        
        
        return self.main
    def fill(self,type,add,times):
        data =[type+"(self,"+add+")",times]
        self.list_of_cards.append(data) 
    def filling_deck(self):
         self.list_of_cards=[]
         self.fill("Sorcery","name='var+'",4)
         self.fill("Sorcery","name='var-'",4)
         self.fill("NumberCard","rand='plus'",6)
         self.fill("NumberCard","rand='minus'",6)
         self.fill("EventCard","name='reverse 3'",1)
         #self.fill("EventCard","name='boost'",1)
         self.fill("Sorcery","name='+to-'",2)
         self.fill("Sorcery","name='+to-'",2)
         self.fill("Brackets",'',8)
         self.fill("Artifact","name='equal'",1)
         self.fill("Artifact","name='fair'",1)
         self.fill("Artifact","name='light_balance'",1)
         self.fill("Artifact","name='dark_balance'",1)
         self.fill("Artifact","name='looser'",1)
         self.fill("Artifact","name='slow_death'",1)
         self.fill("Sorcery","name='var=var'",1)
         self.fill("Sorcery","name='reverse'",4)
         self.fill("Sorcery","name='zero'",1)
         self.fill("Sorcery","name='double_var'",1)
         self.fill("Sorcery","name='swap'",1)
         
       
         #random.shuffle(self.list_of_cards)
         


          
                     
                        
                        





         for data in self.list_of_cards:
             i=0
             while i< data[1]:
               exec(data[0])
               i+=1

         random.shuffle(self.deck)
    def load_game(self,mode="local",data=None):
        self.main.clear_widgets()
        
        self.players=[]
        self.deck =[]
        self.filling_deck()
        


        self.X=3
        self.Y=3
        self.Z=3
        self.mode="duel"
        self.type_of_conn=mode
        
        if self.mode=="duel":
            if mode=="local":
                self.players.append(Player(main=self))
                self.players.append(Player(name=self.settings['name'],main=self))
            elif mode=="multiplayer":
                self.players.append(Player(main=self,name = data[0]))
               
                
                keys=[data]
                self.local_player=Player(name=self.settings['name'],main=self)
                self.players.append(self.local_player)
                self.network.start_battle(self.local_player,keys)
                
        
       
               
        self.time = TimeLabel(self)

        self.UI.start_duel()
        Clock.schedule_interval(self.game_loop_update,.5)
        self.current_turn=0
        self.player_turn=0
        self.active_card=None
        for player in self.players:
            player.exp.update()
    def add_friend(self,data):
        self.settings['friends'].append({"name":data[0],"ip":data[1],"port":data[2],"score":[0,0,0]})
        self.save_settings()
    def save_settings(self):
        with open('data\\settings.json','w') as file:
            json.dump(self.settings,file)
        
    def end_turn(self,instance=None):
         self.active_card=None
         
         self.current_turn+=1
         self.player_turn=self.current_turn%len(self.players)
         self.current_player=self.players[self.player_turn]
         self.current_player.take_card()
      
         self.UI.show_turn()
            

         for player in self.players:
            
             for art in player.artifacts:
                 if art.way=="turn":
                     art.turn_action()
         for player in self.players:
            player.exp.update()
  
        
          
       
         self.time.time=0
         print("Cards left: "+str(len(self.deck)))
    def end_game(self):
        l=False
        choosen=None
        for player in self.players:
            for card in player.artifacts:
                if card.name=="light_balance":
                    l =True
                    choosen=player
                     
                elif card.name=="dark_balance":
                    player.delta+=10
        if l:
            for player in self.players:
                if player!=choosen:
                    player.delta-=10
                    
        pls=[]
    
        for player in self.players:
            player.exp.update()
            pls.append(eval(player.score.text))
        winner = max(pls)
        winner = pls.index(winner)
        winner=self.players[winner]
        print(winner.name.text.upper()+" is winner")
   
    def game_loop_update(self,dt):
         pass
  
      
 

       
        
      
       
        
      
        
        
        
       





MathApp().run()
