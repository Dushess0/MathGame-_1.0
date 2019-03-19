import socket
import random
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

class Player():
    def __init__(self, name="local",main=None,data=None):
        self.comm=main
       
        self.name=NickName(self,name)
        self.number=len(self.comm.players)+1
        self.delta=0
        self.hand=[]
        self.expression_clear='0'
        self.exp = Expression(self)
        self.score=Score(self)
        self.artifacts=[]
       
        
       

      
      

    def get_localname(self):
        self.comm.main.add_widget()
    def calculate_card_pos(self):
        print(self.name.text)
       
        if self.number==1:
      
         
           return ({"x":10+138*(len(self.hand)),"y":460})
        elif self.number==2:
             return ({"x":10+138*(len(self.hand)),"y":15})
    def calculate_art_pos(self):
         if self.number==2:
      
         
           return ({"x":40+138*(len(self.artifacts)),"y":360})
         elif self.number==1:
             return ({"x":40+138*(len(self.artifacts)),"y":115})
    def take_card(self):
        if len(self.comm.deck)!=0:
            
                card=self.comm.deck.pop()
                card.appear(self)
            
          
                if card.type!="event" and card.type!="artifact":
                    if len(self.hand)<7:
                         self.hand.append(card)
                    else:
                          card.disenchant()
             
                 
                elif card.type=="artifact":
                    self.artifacts.append(card)
            
        else:
            self.comm.end_game()


    def update(self):
        self.score.update()
        copy = self.hand.copy()
        self.hand=[]
        for art in self.artifacts:
            if art.way=="update":
                art.update_action()
        for card in copy:
            card.appear(self)
            card.appear(self)
            self.hand.append(card)

           
class Score(Label):
    def __init__(self,player, **kwargs):
         super().__init__(**kwargs)
         self.player =player
         self.score=0
         self.width=50
         self.height=35
         self.font_size=30
         self.player.comm.main.add_widget(self)
         self.update()
         self.status='ok'
 
        

    def update(self):
         x= self.player.comm.X
         y= self.player.comm.Y
         z= self.player.comm.Z
         print(self.player.delta)
         try:
           self.score=self.player.delta+eval(self.player.expression_clear)
           self.status='ok'

         except:
             self.status='error'
            

         if self.score>0:
             add='+'
         else:
             add=''
         self.text=add+str(self.score)
         
class NickName(Label):
     def __init__(self,player,text, **kwargs):
        super().__init__(**kwargs)
        self.text=text
        self.width=150
        self.height=40       
        self.font_size=24
        self.player = player
        self.player.comm.main.add_widget(self)
class Expression(Label):
    def __init__(self,player):
        super().__init__()
        self.player=player
        self.widgets_font_size=30
        self.player.comm.main.add_widget(self)
        sets =[['+',"x","+","y","-","z"],["-","x","+","y","+","z"],['+',"x","-","y","+","z"]]
        self.widgets =[]
        self.set= random.choice(sets)
        if self.player.number==1:
            self.data =(140,225)
        elif self.player.number==2:
            self.data =(140,375)
        self.reserve=''
              
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        mode = touch.button
      
        active=self.player.comm.active_card
        
        for w in self.widgets:
           
           if self.player.comm.active_card!=None:
             
              if  w.type in active.targets or w.text in active.targets:
                  
                  if w.collide_point(touch.x,touch.y) and mode!="middle":
                  
                      active.action(self,w,mode)
                      
                      self.player.comm.UI.clear_highlight()
          
                 
    def update_font_size(self):
        if len(self.widgets)<10:
            pass
        elif len(self.widgets)<20:
           self.widgets_font_size=25
        elif len(self.widgets)<30:
             self.widgets_font_size=20
        elif len(self.widgets)>40:
             self.widgets_font_size=15
      
            

    def update(self,dt=None):
        self.update_font_size()
        x=self.data[0]
        y=self.data[1]
        step=self.widgets_font_size
        width = 700
        start_pos=(x,y)
        start_pos=(start_pos[0]+(width-(len(self.set)*step))/2,start_pos[1])
        for w in self.widgets:
            self.player.comm.main.remove_widget(w)
        self.widgets=[]
        
        
        i=0
        self.player.expression_clear=''
        
        for part in self.set:
            part=str(part)
            lbl=Mini_Label(self.player.comm,text=part)
            
            if part.isnumeric():
                lbl.type="number"
                
               
            elif part.isalpha():
                 lbl.type="variable"
                 
                 

            else:
                 if part=="(" or part==")":
                     lbl.type="bracket"
                 else:
                    lbl.type="operation"
            lbl.font_size=self.widgets_font_size
            lbl.width = 20
            lbl.height=20
            self.player.expression_clear+=part
            move(lbl,start_pos[0]+step*i,start_pos[1])
            self.player.comm.main.add_widget(lbl)
            self.widgets.append(lbl)
            i+=1
        for player in self.player.comm.players:
                          player.update()





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
class Mini_Label(Label):
    def __init__(self,main, **kwargs):
       super().__init__(**kwargs) 
       self.main = main
       self.output=Label()
       self.output.font_size=40
       self.main.main.add_widget(self.output)
       self.output.text=''
       
       
      
    def show_value(self):
        if self.main.active_card==None:
            if self.text =='x':
                add =str(self.main.X)
            elif self.text=='y':
                add =str(self.main.Y)
            elif self.text=='z':
                add =str(self.main.Z)
            else:
                add=''
            self.output.text=add
      
            move( self.output, self.pos[0]-40,Window.size[1]-(self.pos[1]+40))
        
            Clock.schedule_once(self.delete,3)
    def delete(self,dt):
        self.output.text=''
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if self.collide_point(touch.x,touch.y):
            self.show_value()