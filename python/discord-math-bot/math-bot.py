import discord
import traceback
import asyncio
import os
import sys
from discord.ext import commands


BOT_PREFIX = ("?", "!", ">", "*", "-", "_", ":", ".", "^", "<", "+", "&")

TOKEN="token"
TOKEN=os.environ.get("DISCORD_BOT_SECRET")
PREFIX="!"

author_ids=[]
bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_message(message):
    # ------------- IMPORTANT ----------------
    # if you want to restrict access uncomment the next two line

    if message.author.id not in author_ids:
        print(message.author.id)
        return

    if message.author.bot:
        return
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("Math Bot is Online.")

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




@bot.group(name="calc")
async def _u(ctx):
    if not ctx.invoked_subcommand:
        return await ctx.send("Use a sub command like 'add', 'eval'")


@_u.command(name="add")
async def _uadd(ctx,first_num,second_num):
    return await ctx.send(f"{first_num}+{second_num}={int(first_num)+int(second_num)}")

@_u.command(name="eval")
async def _ueval(ctx,expresssion):
    return await ctx.send(f"{eval(expresssion)}")

bot.run(TOKEN)
