ILOSC_CARD=64

from kivy.uix.image import Image
from kivy.core.window import Window

from kivy.clock import Clock
import threading
import winsound
import random


SOUND_FOLDER="data\\sound\\"
IMG_FOLDER="data\\img\\"
ART_IMG=IMG_FOLDER+"artifacts\\"
EVENTS_IMG=IMG_FOLDER+"events\\"
SORCERY_IMG=IMG_FOLDER+"sorcery\\"
BACK_IMG=IMG_FOLDER+"back.jpg"
NUMBER_IMG=IMG_FOLDER+"numbers\\"

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

def update_and_delete(w,main):
    main.main.remove_widget(w)
    main.active_card=None
    for player in main.players:
        player.exp.update()

def play_sound(name):
    t1= threading.Thread(target=winsound.PlaySound,args=(name,winsound.SND_FILENAME))
    t1.start()
class Card(Image):
    def __init__(self,type,main,**kwargs):
        super().__init__(**kwargs)
        self.main=main
        self.targets=[]
               
        self.back=True
        
        self.width=128
        self.height=128
        self.source=BACK_IMG
        self.reload()
        
        self.main.main.add_widget(self)

        self.to_deck()
   
                  
    def appear(self,player):
            self.flip()
           
            
            
           
           
            cords=player.calculate_card_pos()
            delta_x=cords['x']-self.pos[0]
            delta_y=cords['y']-self.pos[1]
            smooth=100

        

           
            speed=(delta_x/smooth,delta_y/smooth)
            
            def animation():
                self.pos[0]+=speed[0]
                self.pos[1]+=speed[1]
            do_something(animation,2,self)
            self.player=player     
    def disenchant(self):
        update_and_delete(self,self.main)
       # play_sound("data\\sound\\disenchant.wav")
    def action(self,expression,widget,mode):
          
          index =expression.widgets.index(widget)
         
          if  self.value>0:
                 add="+"
          else:
                 add="-"
          exp=expression.set
        
        
       
          if mode=="right":               
                 exp.insert(index+1,add)
                 exp.insert(index+2,abs(self.value))
                
          elif mode=="left":
                    
                    if exp[index-1]=="+"  or str(exp[index-1]).isnumeric() or str(exp[index-1]).isalpha() :
                        prev='+'
                       
                    elif exp[index-1]=="-":
                        prev="-"

                    if  exp[index]==")":
                        prev=''
                      

                    if prev!='':
                            exp.insert(index,prev)
                            
                    
                 
                    exp.insert(index,str(abs(self.value)))
                   
                    if index!=0:
                            if prev!='':
                             exp[index-1]=add
                            else:
                              exp.insert(index,add)
                    else:                 
                        if add!='+':
                           exp.insert(index,add)
                       

          self.player.hand.remove(self)   
          update_and_delete(self,self.main) 
    def to_deck(self):
        self.main.deck.append(self)
        move(self,len(self.main.deck),300)
    
         

          
        
        

    def flip(self):
        if self.back:
            self.back=False
            self.source=self.img
        else:
            self.back=True
            self.source=BACK_IMG
        self.reload()
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if not self.back:
            if self.collide_point(touch.x,touch.y):
                if self.player==self.main.current_player:
                    self.become_active()
                    
                    
                  
    def become_active(self):
        
        self.player.comm.UI.highlight(self)
        if self.main.active_card!=self:
            self.main.active_card=self  
        else:
            self.main.active_card=None
            self.player.comm.UI.clear_highlight()
class Brackets(Card):
    def __init__(self,main,**kwargs):
        self.type ="bracket"
        super().__init__(self.type,main,**kwargs)
        self.img = IMG_FOLDER + "brackets.jpg"
        self.targets=["variable","number","operation"]
      
        self.charges=["(",")"]
        self.left_pos=0
        self.right_pos=0
        
        
    def action(self, expression, widget, mode):
             def deleting():
                 
                 
                 for player in self.main.players:
                     player.exp.update()
                 del self.charges[0]
                
                 if self.charges==[]: 
                     print('ending')
                     i=0
                     once=False
                     
                     for player in self.main.players:
                         if player.score.status=="error":
                             player.exp.set=player.exp.reserve
                             print(player.exp.set)
                             
                             once=True
                             print('error')
                             i+=1
                     if not once:
                         update_and_delete(self,self.main) 
                         self.player.hand.remove(self)
                     else:
                         self.charges=["(",")"]
                    
                 for player in self.main.players:
                         player.exp.update()
         
             index =expression.widgets.index(widget)
             exp=expression.set
             if self.charges==["(",")"]:
               
                 for player in self.main.players:
                    
                    player.exp.reserve=player.exp.set.copy()
             cur =self.charges[0]
             
             if mode=="right":      
                 exp.insert(index+1,cur)
             elif mode=="left":                      
                 exp.insert(index,cur)

             deleting()
                              
                   
                        

               
                 
            
  



class NumberCard(Card):
    def __init__(self,main,rand="random",**kwargs):
        self.type="number"
        super().__init__(self.type,main,**kwargs)
        
        while True:
                if rand=="random":
                  self.value = random.randint(-10,10)
                elif rand=="plus":
                     self.value = random.randint(0,10)
                elif rand=="minus":
                     self.value = random.randint(-10,0)
                if self.value>0:
                    add ="+"
                else:
                    add=''
                if self.value!=0:
                    break
           
        self.img=NUMBER_IMG+add+str(self.value)+".jpg"
        self.targets=["variable","number","bracket"]
       
class Sorcery(Card):
     

    def __init__(self,main,name='',**kwargs):
         self.type="sorcery"
         super().__init__(self.type,main,**kwargs)
        
         self.events=["+to-","-to+","var+","var-","var=var","reverse","double_var","swap",'zero']
         if name=='':
             self.name =random.choice(self.events)
         else:
             self.name = name
         if self.name =="reverse":
             self.targets=["operation"]
         elif self.name=="+to-":
             self.targets=["+"]
         elif self.name=="-to+":
             self.targets=["-"]
         elif self.name in ["var+","var-","var=var","double_var","swap",'zero']:
             self.targets=["variable"]
         if self.name!="var+" and self.name!="var-":
           self.img = SORCERY_IMG+ self.name +".jpg"
         else:
             self.add = random.choice([3,6,9])
             self.img = SORCERY_IMG+ self.name+str(self.add) +".jpg"
         self.succes=True
         print(self.targets)
        
    def equal(self,w,exp):
        
        if self.main.buffer==None:
            self.main.buffer=w.text
        else:
            add=self.main.buffer
         
           
          
            part="self.main."+w.text.capitalize()
            exec(part+"="+"self.main."+add.capitalize())
            
            print('completed')
            self.main.buffer=None
            self.player.hand.remove(self)
            update_and_delete(self,self.main)           
    def swap(self,w,exp):
        
        if self.main.buffer==None:
            self.main.buffer=w.text
        else:
            add=self.main.buffer
         
         
           
            part="self.main."+w.text.capitalize()
            exec("self.main."+add.capitalize()+","+part+"="+part+","+"self.main."+add.capitalize())
            
            print('completed')
            self.main.buffer=None
            self.player.hand.remove(self)
            update_and_delete(self,self.main)      
            
    def action(self,expression,widget,mode):
        print('hoba')
        index=expression.widgets.index(widget)
        if self.name=="+to-":
           
            if widget.text=="+":           
                expression.set[index]='-'
        elif self.name=="-to+":
            old=[]
           
            if widget.text=="-":           
                expression.set[index]='+'

        elif self.name=="reverse":
             if widget.text=="-":           
                expression.set[index]='+'
             elif widget.text=="+":           
                expression.set[index]='-'
        elif self.name=="var+":
            exec("self.main."+widget.text.capitalize()+"+= self.add")
         
        elif self.name=="var-":
          exec("self.main."+widget.text.capitalize()+"-= self.add")
        elif self.name=="double_var":
          exec("self.main."+widget.text.capitalize()+"*= 2")
        elif self.name=="zero":
            exec("self.main."+widget.text.capitalize()+"= 0")
        elif self.name=="swap":
             self.swap(widget,expression)
        elif self.name=="var=var":
            self.equal(widget,expression)
        if  self.name!="swap" and self.name!='var=var':
            self.player.hand.remove(self)
            update_and_delete(self,self.main) 


class Artifact(Card):
    def __init__(self,main,name='',**kwargs):
         self.type="artifact"
         super().__init__(self.type,main,**kwargs)
         self.artifact_list=['equal','fair','slow_death','light_balance','dark_balance','looser']
         self.turn =['equal','fair','slow_death']
         self.update =['light_balance','dark_balance']
         if name =='':
             self.name =random.choice(self.artifact_list)
         else:
             self.name =name
         if self.name in self.turn:
             self.way ='turn'
             self.action=self.turn_action
         elif self.name in self.update:
             self.way ='update'
             self.action=self.update_action
         else:
             self.way="end"
         self.img = ART_IMG+self.name+".jpg"
    def appear(self,player):

            self.flip()
            if self.name=="equal":
               
                play_sound(SOUND_FOLDER+"equal.wav")
               
            delta_x=770-self.pos[0]
            delta_y=240-self.pos[1]
            smooth=100
            delta_x_2=0-770
            delta_y_2=440-240
            if self.way=="update":
                Clock.schedule_interval(self.update_action,0.2)
            speed_2=(delta_x_2/smooth,delta_y_2/smooth)

           
            speed=(delta_x/smooth,delta_y/smooth)
            
            def animation():
                self.pos[0]+=speed[0]
                self.pos[1]+=speed[1]
            def move_to_eff(dt):
                self.pos[0]+=speed_2[0]
                self.pos[1]+=speed_2[1]
            do_something(animation,2,self)
            
            Clock.schedule_once(self.deleting,8)
            self.player=player
            print(str(self.player.name.text))



    def deleting(self,dt=None):
         
                self.main.main.remove_widget(self)
                cords=self.player.calculate_art_pos()
                move(self,cords['x'],cords['y'])
          
    def   turn_action(self):
        
         if self.name=="slow_death":
             for player in self.main.players:
                 if player.name!=self.player.name:
                     player.delta-=1
                   
         elif self.name=="fair":
                    
                     self.player.delta+=1
                    
                    
         elif self.name=="equal":       #back to ussr
             avg=0
             for player in self.main.players:
                 avg += player.score.score/len(self.main.players)
             for player in self.main.players:
                 if player.score.score>avg:     #значит буржуй
                     player.delta-=1
                 elif player.score.score<avg: # честный пролетариат
                     player.delta+=1



    def update_action(self,dt=None):
        try:
            if self.name=="dark_balance":
                for player in self.main.players:
                    if player.score.score<self.player.score.score:
                        self.player.artifacts.remove(self)
            elif self.name=="light_balance":
                for player in self.main.players:
                    if player.score.score>self.player.score.score:
                        self.player.artifacts.remove(self)
        except:
            pass



    
   
   
class EventCard(Card):
    def __init__(self,main,name='',**kwargs):
         self.type="event"
         super().__init__(self.type,main,**kwargs)
         
         self.events=["reverse 3","destroy all brackets","boost"]
         if name=='':
           self.name = random.choice(self.events)
         else:
             self.name=name
         self.img =EVENTS_IMG
         if self.name =="reverse 3":
             self.img +="reverse_3.jpg"
         elif self.name=="destroy all brackets":
             self.img+="brackets_destroy.jpg"
         elif self.name=="boost":
             self.img+="boost.jpg"
    def reverse_3(self):
        
        
        i=0
        used=[]
        while i<3:
           
           indecies=[]
           player = random.choice(self.main.players)
           for sign in player.exp.widgets:
               if sign.type=="operation":
                   indecies.append(player.exp.widgets.index(sign))
           
           index = random.choice(indecies)
           if [player.number, index] not in used:
               if player.exp.set[index]=='+':
              
                  player.exp.set[index]='-'
                 
               elif player.exp.set[index]=='-':
                   player.exp.set[index]="+"
               used.append([player.number, index])
               i+=1
        for player in self.main.players:
             player.exp.update()
       
            





                      
             
  
    def brackets_destroy(self):
        for player in self.main.players:
            for symbol in player.exp.set:
                if symbol=="(" or symbol==")":
                     player.exp.set.remove(symbol)
            player.exp.update()

    def boost(self):
        self.main.time.turn_time=15
        play_sound(SOUND_FOLDER+"boost.wav")
       

    def appear(self,player=None):
            self.flip()
            
            delta_x=770-self.pos[0]
            delta_y=240-self.pos[1]
            smooth=100

        

           
            speed=(delta_x/smooth,delta_y/smooth)
            
            def animation():
                self.pos[0]+=speed[0]
                self.pos[1]+=speed[1]
         
            do_something(animation,2,self)
        #    Clock.schedule_once(self.action,3)
            self.action()
            Clock.schedule_once(self.deleting,8)
           
    def deleting(self,dt=None):
         
                self.main.main.remove_widget(self)
                
    def action(self,dt=None):
        if self.name =="reverse 3":
            self.reverse_3()
        elif self.name=="destroy all brackets":
            self.brackets_destroy()
        elif self.name=="boost":
            self.boost()


       
       
             



