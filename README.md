# WA State DMV Appointment Scraper
Python script that automatically searches the official WA State DMV website for open appointment slots.  
Motivation behind this script was not being able to find open locations in WA state (due to COVID-19) and how tedious searching for locations was.
  
The script requires the following packages:
- ```selenium```
- ```twilio```
  
You will need a [Twilio](https://www.twilio.com) account. A free trial account can be made from their website.  
You will also need an account from the DMV [website](https://secure.dol.wa.gov/).  
Before using the script, you will need to set up the following environment variables:
- ```export DOL_USERNAME=...```
- ```export DOL_PASSWORD=...```
- ```export EMAIL=...```
- ```export PHONE_NUMBER=...```
- ```export FROM_NUM=...``` (Phone number that Twilio assigns to your account)
- ```export TO_NUM=...``` (Phone number that is verified by Twilio to send text messages to) 
- ```export ACCOUNT_SID=...``` (from Twilio)
- ```export AUTH_TOKEN=...``` (from Twilio)
  
Usage: ```python3 bot.py <location 1> ... <location n>```
  
If the script sees that a location has open spots, then it will text your phone:  
___Sent from your Twilio trial account - "\<Location X\>" has spots!___  
  
