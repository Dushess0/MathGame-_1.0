import socket
import json
import threading
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        print('you are offline')

           
def send_message(ip,message,port):
    try:
        sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
        sock.sendto(message.encode(), (ip, port))
    except:
        print("error ip or port is not valid")

def question(text):
    a=input(text)
    if a.lower()=='yes' or a.lower()=='y':
        return True
    else:
        return False
class NetWork():
    def __init__(self,comm):
        self.comm=comm
        self.settings=self.comm.settings
        self.main_port=self.settings['port']
        #self.start_listening()
        self.host=False
    
    def start_listening(self):
         
         UDP_IP = "127.0.0.1"
         sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
         sock.bind(("0.0.0.0", self.main_port)) 
         print("YOUR IP ADDRES IS")
         print()
         print(get_ip_address())
         print()
         print("YOUR MAIN PORT IS")
         print()
         print(self.settings['port'])
         print()
         def listen():
          
        
           while True:
               
                   data, addr = sock.recvfrom(1024) # более чем достаточно
                   message= data.decode()
                   print(message)
                   data = self.data_from_string(message)
                   self.commands(data,message)
              
                   

             
               
         t2= threading.Thread(target=listen)
         t2.start()
    def start_battle(self,player,keys):
        print("started")
        self.local=player
        i=0
        self.enemies=[]
        for enemy in self.comm.players:
            if enemy!=self.local:
                enemy.ip=keys[i][1]
                enemy.sending_port=keys[i][2]+1
                self.enemies.append(enemy)
                i+=1

        UDP_IP = "127.0.0.1"
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind(("0.0.0.0", self.main_port+1)) 
        if self.host:
            self.game_init()
            print('host pidr')
        def listen():
          
        
           while True:
               
                   data, addr = sock.recvfrom(1024) # более чем достаточно
                   message= data.decode()
                   print(message)
                   data = self.data_from_string(message)
                   self.battle_commands()
              
                   

             
               
        t3= threading.Thread(target=listen)
        t3.start()
    def commands(self,data,message):
        if message.startswith('friend invite'):
            print("Player "+data[0]+" want to be your friend. Confirm?")
            if question("y/n "):
                self.comm.add_friend(data)
                self.friend_accept(data)
            else:
                self.friend_reject(data)
        elif message.startswith('friend accept'):
           self.comm.add_friend(data)
           print("You have new friend! "+data[0])
        elif message.startswith('battle request'):
             print("Player "+data[0]+" want fight with you. Confirm?")
             if question("y/n "):
                self.comm.load_game("multiplayer",data)
                self.battle_accept(data)
             else:
                self.battle_reject(data)
        elif message.startswith('battle accept'):
            self.host=True
            self.comm.load_game("multiplayer",data)
            
    def send_message_to_enemy(self,enemy,message):
        send_message(enemy.ip,message,enemy.sending_port)
    def send_sets(self):
        data = []
        for player in self.comm.players:
            data.append(player.exp.set)
        print(data)
        
        for enemy in self.enemies:
            self.send_message_to_enemy(enemy,"new sets"+self.str_data(data)+self.str_addres())
            print('sented to enemy')
    def first_turn_init(self):
        if self.host:
            for enemy in self.enemies:
                self.send_message_to_enemy("turn init ")
    def battle_commands(self,data,message):
          if message.startswith("end turn"):
              self.comm.end_turn()
              print('hoba')
          
          elif message.startswtih("init turn"):
              
              
              
              for player in self.comm.players:
              
                  print("loading")
                  player.exp.set=data[3][i]
                  i+=1
                     
                      
    def data_from_string(self,message):
          name = message[message.find("<")+1:message.find(">")]
          ip=message[message.find("[")+1:message.find("]")]
          port =  message[message.find("{")+1:message.find("}")]
          add = message[message.find("/")+1:message.find("#")]
          try:
              add=json.loads(add)
          except:
              pass
          return [name,ip,int(port),add]
    def str_data(self,data):

        return "/"+json.dumps(data)+"#"
    def str_addres(self):
        name="<"+self.settings['name']+">"
        ip="["+get_ip_address()+"]"
        port="{"+str(self.main_port)+"}"
        return name +ip + port
    def send_direct_request(self,*args):
        a=input("ENTER IP : ")
        b=input("ENTER PORT :")
       
        send_message(a,"battle request "+self.str_addres(),int(b))
        
    def battle_accept(self,data):
       
        send_message(data[1],"battle accept "+self.str_addres(),data[2])
    def battle_reject(self,data):
        send_message(data[1],"battle not accepted by user"+self.settings['name'],data[2])

    def friend_invite(self,instance=None):
        a=input("Enter IP : ")
        b=int(input("ENTER PORT: "))
        send_message(a,"friend invite "+self.str_addres(),b)
    def send_stats(self,data):
        
        send_message(data[1],'my user data'+json.dumps(self.settings['stats']+'data',data[2]))
 
    
    def friend_accept(self,data):
         send_message(data[1],"friend accept"+self.str_addres(),data[2])
         self.comm.add_friend(data)
         print("You have new friend!")
    def friend_reject(self,data):
        send_message(data[1],"FRIEND INVITATION wasn't accepted by "+self.settings['name'],data[2])


