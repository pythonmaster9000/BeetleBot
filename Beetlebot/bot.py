from utils import chat
import discord
from discord.ext import commands, tasks
import time

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='yo ', case_insensitive=True, intents=intents)
conversations = {}


@client.event
async def on_ready():
    clear_chats.start()


@tasks.loop(seconds=30)
async def clear_chats():
    for convo in conversations:
        if int(time.time())-conversations[convo].last_interaction > 600:
            del conversations[convo]


@client.command()
async def beet(ctx, *args):
    prompt = ' '.join(args)
    if not conversations.get(str(ctx.message.author.id)):
        conversations[str(ctx.message.author.id)] = chat.NewChat(preface=chat.beetlejuice_preface,
                                                                 reassurance=chat.beetlejuice_reassurance)
    chat_object = conversations[str(ctx.message.author.id)]
    response = chat_object.chat(prompt)
    await ctx.send(response)


client.run('TOKEN HERE')
