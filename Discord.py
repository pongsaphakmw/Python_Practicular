import discord
import os
import requests
import json
import random
from replit import db

my_secret = os.environ['TOKEN']

client = discord.Client()

sad_word = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

compliment = ["good work", "well done", "เก่งมากบอท"]

starter_encouragements = [
  "Cheer Up!",
  "Hang in there",
  "You are a great person / bot !"
]

compliment_encouragements = [
  "Thank you!",
  "Thx"
]

def get_qoute():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  qoute = json_data[0]['q'] + " -" + json_data[0]['a']
  return(qoute)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index :
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith(';;inspire'):
    qoute = get_qoute()
    await message.channel.send(qoute)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_word):
    await message.channel.send(random.choice(options))

  if any(word in msg for word in compliment):
    await message.channel.send(random.choice(compliment_encouragements))

  if msg.startswith(";;new"):
    encouraging_message = msg.split(";;new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith(";;del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split(";;del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

client.run(os.getenv('TOKEN'))