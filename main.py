import discord
import os
import datetime
import pytz

token = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$time help'):
    await message.channel.send("**WELCOME TO TIMEZONE BOT**\n\nTo search for a city's time, **`<$time City>`**. If city has multiple words, use _, example New_York, El_Salvador. Keep the first letter uppercase for the cities.\nTo search for a GMT timezone, for example GMT+11, **`<$time GMT+11>`**.\nTo search for a timezone, for example EST, **`<$time EST>`**.\n\nTo search for time difference between two cities (or two timezones, or a timezone and a city) **`<$time City1 City2>`**.\n\nTo convert timezones, **`<$time Given_City City_To_Search Time Date>`**.\nFor when you want to know, \"What's the time in London when it is 9 PM in New York?\", use `<$time New_York London 21:00 22-07-2021>`. \nNote the `time is in 24 hour format` and `date is dd-mm-yyyy`.")
  if message.content.startswith('$time'):
    m = list(str(message.content).split())
    if len(m) == 2:
      for i in pytz.all_timezones:
        if i.endswith(m[1]):
          d = datetime.datetime.now(pytz.timezone(i))
          #fmt = "%H:%M:%S\n%I:%M %p\n%d-%b-%Y\n%A \nTimezone: %Z\nUTC offset: %z"
          fmt2 = "%I:%M %p. The date is %d-%b-%Y, %A. Timezone: %Z, UTC offset: %z. Military time: %H:%M:%S"
          dat = d.strftime(fmt2)
          await message.channel.send(f'Hello! Time in {m[1]} right now is `{dat}`')
        

    if len(m) == 3:
      for i in pytz.all_timezones:
        if i.endswith(m[1]):
          d1 = datetime.datetime.now(pytz.timezone(i))
      for i in pytz.all_timezones:
        if i.endswith(m[2]):
          d2 = datetime.datetime.now(pytz.timezone(i))
          fmt = "%z"
          os1 = d1.strftime(fmt)
          os2 = d2.strftime(fmt)

          num1 = int(os1[1:])
          num2 = int(os2[1:])
          if(os1[0] == "-"):
            num1 = num1 * -1
          if(os2[0] == "-"):
            num2 = num2 * -1
          print(num1)
          print(num2)
          if(num1 > num2):
            ahead = m[1] + " is ahead in time."
          elif(num2 > num1):
            ahead = m[2] + " is ahead in time."
          else:
            ahead = m[1] + " and "
            ahead = ahead + m[2] + " are in the same timezone."
          diff = abs(num1-num2)
          await message.channel.send(f'Hello! Time in difference between {m[1]} and {m[2]} is `{diff//100} hours`. {ahead}')
    
    if len(m) == 5:
      for i in pytz.all_timezones:
        if i.endswith(m[1]):
          d1 = pytz.timezone(i)
      for i in pytz.all_timezones:
        if i.endswith(m[2]):
          d2 = pytz.timezone(i)
      t = m[3] + m[4]
      dt = datetime.datetime.strptime(t, "%H:%M%d-%m-%Y")
      dt = d1.localize(dt)
      dt = dt.astimezone(d2)
      dt = dt.strftime(f"{m[2]} - `%H:%M` on `%d-%m-%Y` \n(Both 24-Hour time)")
      await message.channel.send(f'Time in {m[2]} when it is `{m[3]}` on `{m[4]}` in {m[1]} is -')
      await message.channel.send(dt)
client.run(token)
