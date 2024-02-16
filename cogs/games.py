import discord
from discord.ext import commands
from discord import app_commands
from devLogging import devLogging
from hypixelAPI import hypixelAPI
import os
import random
from asyncio import sleep as asyncio_sleep
        
def legacy_permission_check(self, ctx: commands.Context):
    for role in (self.bot.staffRole, self.bot.adminRole, self.bot.developerRole):
        if role in ctx.author.roles:
            return True
    return False

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name='on_ready')
    async def on_ready(self):
        await self.bot.tree.sync()
        devLogging.info(msg='Cog finished loading', module=__name__)

    @commands.command(name='duck')
    async def duck(self, ctx):
        if (ctx.channel.id == 1143310823754825738) and (legacy_permission_check(self, ctx) == False):
            embed = discord.Embed(description="Sorry, a developer has disabled this command for this channel!", colour=discord.Colour.red())
            reply = await ctx.send(embed=embed)
            await asyncio_sleep(3)
            await reply.delete()
            return
        duck_jokes = ["Sure, I can send a picture, but who's paying the bill?", "I swear, I'm going have to get up at the quack of dawn to keep doing this", "I hadn't prepared for this.. oh well I'll just wing it", "Did you know this was a command? Its not bill-t in or anything so maybe you didn't", "Why do you all use this command so much? Its not as educational as a duck-umentary", "Hey did you watch those really old movies? I think they are called 'Lord of the Wings' or something", "I just realised I basically control the internet, I have the web on my feet right?", "I never liked board games but I could totally play bill-iards or something", "Humans are so uncivilised, they store money on _bills_!?"]
        saved_images = os.listdir('JackBlight/images/ducks')

        selected_image = random.choice(saved_images)

        with open(f'JackBlight/images/ducks/{selected_image}', 'rb') as f:
            image = discord.File(f)
            await ctx.send(random.choice(duck_jokes), file=image)





async def setup(bot):
    await bot.add_cog(Games(bot))