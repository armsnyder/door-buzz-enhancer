#Door Buzz Enhancer
In our apartment no one can hear the door buzzer because it's lame and quiet. This program can run continuously on a 
Raspberry Pi with a USB microphone to detect when the buzzer sounds and send us a text alert us so that we know if 
someone is at the door no matter where we are.

Is this really necessary, or is someone just looking for an excuse to use his Raspberry Pi for something?

##Setup
You must create a ``config.json`` file in the same directory as the python script, and fill it in as follows:
```
{  
  "login":{  
    "username":"<email address>",  
    "password":"<email password>"  
  },  
  "destinations":[  
    "<email / email-to-sms-gateway>"  
  ]  
}  
```
