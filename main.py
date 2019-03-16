import discord
import asyncio
import database
from command import Command
from bot_func import *
from tabs import *
from json_handler import *
token = "NTU0MzYxMDU2Mjk0ODYyODgw.D2bg_g.yS0qkSdQUPJHAea6ul086yd-GZo"
prefix = "!"
class Client(discord.Client):   
    open_tabs = {}
    delt = 60
    minfsb = 2
    async def on_ready(self):
        self.starboard_channel = self.get_channel(id=556228271872671744)
        self.bot_info = await self.application_info()
        print("///=----------------------------------=///")
        print("Logged in as {username} with ID {id}".format(username=self.user.name, id=self.user.id))
        print("///=----------------------------------=///")        
    commands = {
            "kick": Command(kick_user, discord.Permissions(permissions=2)),
            "ban": Command(ban_user, discord.Permissions(permissions=4)),
            "help": Command(help),
            "latency": Command(latency),
            "about": Command(about)
    }
    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return
        try:
            if user == self.open_tabs[reaction.message.id].owner:
                offset = 0
                if reaction.emoji == "➡":
                    if self.open_tabs[reaction.message.id].currentPage == len(self.open_tabs[reaction.message.id].pages) - 1:
                        offset = 0
                    else:
                        offset = 1
                elif reaction.emoji == "⬅":
                    if self.open_tabs[reaction.message.id].currentPage == 0:
                        offset = 0
                    else:
                        offset = -1
                else:
                    return
            await change_tab_page(self, reaction.message.id, reaction.message.channel, self.open_tabs[reaction.message.id].currentPage + offset)
            return
        except KeyError:
            if reaction.emoji == "👍":
                starboard = await get_starboard()
                if starboard != []:
                    for v in starboard:
                        if v["msgId"] == reaction.message.id:
                            await change_starboard(reaction.message.id, reaction.count)
                            return
                if reaction.count >= self.minfsb:
                    starMessageEmbed = discord.Embed(title="👍 " + str(reaction.count), description=str(reaction.message.content), timestamp=reaction.message.created_at)
                    starMessageEmbed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
                    starMessage = await self.starboard_channel.send(embed=starMessageEmbed)
                    await save_starboard(reaction.message.id, starMessage.id, reaction.count)
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji == "👍":
                starboard = await get_starboard()
                if starboard != []:
                    for v in starboard:
                        if v["msgId"] == reaction.message.id:
                            await change_starboard(reaction.message.id, reaction.count)
                            if reaction.count < self.minfsb:
                                starMessage = await self.starboard_channel.get_message(int(v["starMsgId"]))
                                await starMessage.delete()
                                await remove_starboard(v["msgId"])
                            return
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith(prefix):
            com, sep, params = message.content.partition(" ")
            com = com[1:]
            params = list(filter(None, params.split(" ")))
            try:
                v = self.commands[com]
            except KeyError:
                await message.channel.send("{mention}, try the **!help** command, because this command doesn't exist!".format(mention=message.author.mention), delete_after=self.delt)
            else:
                if message.author.top_role.permissions >= v.perms:
                    await v.func(self, message, params)
                else:
                    await message.channel.send("{mention}, you don't have enough permission to do this!".format(mention=message.author.mention), delete_after=self.delt)
client = Client(activity=discord.Activity(name="your behaviour!", type=3))
client.run(token)