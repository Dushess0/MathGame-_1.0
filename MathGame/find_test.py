import json
def send_sets():
        data = 'x+5-4+z-y; y-4+5'
        
      
        message="/"+data+"#"
       
        return message

    
def get_s(message):
    print('aaa')
    data=message[message.find("/")+1:message.find("#")]
    print(data)
    
    print(data.split(';'))
data=send_sets()
get_s(data)
