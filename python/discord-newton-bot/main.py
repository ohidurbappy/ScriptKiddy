import discord
import traceback
import os
import json
import sys
from discord.ext import commands
from discord.embeds import Embed
from flask import Flask
from threading import Thread


# load .env when in development mode
if os.name == 'nt':
    from dotenv import load_dotenv
    load_dotenv()

TOKEN=os.environ.get("DISCORD_BOT_SECRET")
PREFIX="!"

author_ids=[679306420587462667]
bot = commands.Bot(command_prefix=PREFIX)

app = Flask(__name__)

@app.route('/')
def main():
    return "Newton is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()



# helper functions for bot

def findWord(word:str):
    word=word.lower()

    src_file=open("dictionary1.json")

    dictionary=json.load(src_file)

    src_file.close()

    if word in dictionary:
        return dictionary[word]
    return


# bot handle functions

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id not in author_ids:
        print(message.author.id)
        return
    
    if message.content.lower() == 'hi':
            await message.channel.send('Hello!')
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("Newton is Online.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send('Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        original = error.original
        if not isinstance(original, discord.HTTPException):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(original.__traceback__)
            print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send(error)


@bot.event
async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)


@bot.command(name='calc')
async def calc(ctx,expr):
    return await ctx.send(f"{expr} = {eval(expr)}")


@bot.group(name="word")
async def word(ctx):
    if not ctx.invoked_subcommand:
        return await ctx.send("Ask me about meaning of a word")


@word.command(name="meaning")
async def meaning(ctx,word:str=""):
    return await ctx.send(f"The meaning of {word} is {findWord(word) or 'not found'}")

@bot.command(name='wm')
async def word_meaning(ctx,word:str=""):
    if word=="":
        return await ctx.send(f"Ask me a word")
    
    e=Embed()
    e.title="Word Meaning"
    e.colour = int("00ACEE", 16)

    meaning_of_word=findWord(word)

    if meaning_of_word==None:
        meaning_of_word="Not found in my dictionary!"

    e.add_field(name=word, value=meaning_of_word[:1024], inline=False)


    if len(meaning_of_word)>1024:
        n=1024
        for i in range(n, len(meaning_of_word), n):
            e.add_field(name="More",value=meaning_of_word[i:i+n],inline=False)


    return await ctx.send(embed=e)

if __name__ == "__main__":
    try:
        # start flask app
        keep_alive()

        bot.run(TOKEN)

    except KeyboardInterrupt:
        print("Quiting...")
        sys.exit(0)
    except:
        traceback.print_exc()

    


