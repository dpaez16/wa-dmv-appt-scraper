# WA State DMV Appointment Scraper
Python script that automatically searches the official WA State DMV website for open appointment slots.  
Motivation behind this script was not being able to find open locations in WA state (due to COVID-19) and how tedious searching for locations was.
  
The script requires the following packages:
- ```selenium```
- ```twilio```
  
Usage: ```python3 bot.py <location 1> ... <location n>```

You will need a [Twilio](https://www.twilio.com) account. A free trial account can be made from their website.
If the script sees that a location has open spots, then it will text your phone:  
___Sent from your Twilio trial account - "\<Location X\>" has spots!___  
  
