import discord
import math
from tabs import *
from datetime import datetime
async def kick_user(self, message, params):
    if len(message.mentions) != 0:
        reason = ""
        for i in params:
            if "@" not in i:
                reason += i + " "
        for user in message.mentions:
            try:
                await user.kick(reason=reason)
            except discord.errors.Forbidden:
                await message.channel.send("{0} cannot be kicked because I don't have enough permission!".format(user.mention), delete_after=self.delt)
            else:
                if reason != "":
                    await message.channel.send("{0} kicked {1} from the server. Reason: {2}".format(message.author.mention, user.mention, reason), delete_after=self.delt)
                else:
                    await message.channel.send("{0} kicked {1} from the server. Reason: None".format(message.author.mention, user.mention), delete_after=self.delt)
    else:
        await message.channel.send("{mention}, you need to specify who you want to kick!".format(mention=message.author.mention), delete_after=self.delt)
async def ban_user(self, message, params):
    if len(message.mentions) != 0:
        reason = ""
        for i in params:
            if "@" not in i:
                reason += i + " "
        for user in message.mentions:
            try:
                await user.ban(reason=reason)
            except discord.errors.Forbidden:
                await message.channel.send("{0} cannot be banned because I don't have enough permission!".format(user.mention), delete_after=self.delt)
            else:
                if reason != "":
                    await message.channel.send("{0} banned {1} from the server. Reason: {2}".format(message.author.mention, user.mention, reason), delete_after=self.delt)
                else:
                    await message.channel.send("{0} banned {1} from the server. Reason: None".format(message.author.mention, user.mention), delete_after=self.delt)
    else:
        await message.channel.send("{mention}, you need to specify who you want to ban!".format(mention=message.author.mention), delete_after=self.delt)
async def help(self, message, params):
    pages = {}
    pages[0] = discord.Embed(title="Help for the help command")
    pages[0].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[0].add_field(name="!command:", value="*description* (!command *required arguments* [*optional arguments*])")
    pages[1] = discord.Embed(title="Information commands")
    pages[1].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[1].add_field(name="!help", value="I help you as I can, にゃあ~~! (!help)")
    pages[1].add_field(name="!latency", value="I can tell you my LATENCY! (!latency [precise])")
    pages[1].add_field(name="!about", value="I can tell everything ABOOUUUTT MYYYYYSEEEELLLLFFF *awkward singing noises* (!about)")
    pages[2] = discord.Embed(title="Moderation commands")
    pages[2].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[2].add_field(name="!kick", value="I can kick some... you know! (!kick @spam @eggs [Some reasoning...])")
    pages[2].add_field(name="!ban", value="This is the most painful thing I can to do someone... (!ban @eggs @spam @KaTsUzU [Some seasoning, I mean reasoning!])")
    currTab = await create_tab(self, message.author, pages, message.channel)
async def latency(self, message, params):
    if len(params) != 0 and params[0] == "precise":
        latency = self.latency * 1000
    else:
        latency = math.ceil((self.latency * 1000) * 100)/100
    await message.channel.send("Well, the latency is: {0}ms!".format(latency), delete_after=delt)
async def about(self, message, params):
    aboutEmbed = discord.Embed(title="Hi! I'm going to introduce myself!")
    aboutEmbed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
    aboutEmbed.add_field(name="What is my purpose?", value="Oh, I'm a multi-purpose bot! My mission is to entertain, defend and moderate communities!")
    aboutEmbed.add_field(name="Who is my creator?", value="I was written by {author}. He is the smartest, most beautiful, living human in the world. (His ego is reaaaaaally tiny. Right? RIGHT?!!!)".format(author=self.bot_info.owner.mention))
    await message.channel.send(embed=aboutEmbed, delete_after=self.delt)
