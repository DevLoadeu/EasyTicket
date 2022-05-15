import asyncio
import datetime
import time

import aiomysql
import chat_exporter
import discord
from discord.ext import commands
import os
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle


# ----------------------------------------------------------------------------------------------------------------------


bot = commands.Bot(command_prefix="+", intents=discord.Intents.all(), help_command=None)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


# ----------------------------------------------------------------------------------------------------------------------


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename} wurde geladen')


# ----------------------------------------------------------------------------------------------------------------------


loop = bot.loop
bot.pool = loop.run_until_complete(
    aiomysql.create_pool(
        host="45.155.76.193", port=3306, user="EasyTicket", password="EasyTicket2022$", db='EasyTicket',
        loop=loop, autocommit=True, maxsize=25)
)


# ----------------------------------------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f"Name: {bot.user.name}\n"
          f"Discriminator: {bot.user.discriminator}\n"
          f"ID: {bot.user.id}\n"
          f"Server: {len(bot.guilds)}")
    bot.loop.create_task(status_task())
    bot.loop.create_task(vote_reminder_check())
    chat_exporter.init_exporter(bot)


# ----------------------------------------------------------------------------------------------------------------------


async def status_task():
    while True:
        members = 0
        for x in bot.guilds:
            members += len(x.members)
        await bot.change_presence(activity=discord.Game(name=f"auf {len(bot.guilds)} Server mit {members} Member"),
                                  status=discord.Status.online)
        await asyncio.sleep(60)
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM Tickets")
                result = await cursor.fetchall()
        await bot.change_presence(activity=discord.Game(name=f"mit {len(result)} Tickets"),
                                  status=discord.Status.online)
        await asyncio.sleep(60)


@bot.event
async def vote_reminder_check():
    while True:
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM TopggVotes")
                result = await cursor.fetchall()
        for x in result:
            if (int(float(x[2])) + 43200) < int(float(time.time())):
                if f"{x[3]}" == "Ja":
                    user = bot.get_user(int(x[0]))
                    embed = discord.Embed(title=f"__Vote Reminder__",
                                          description=f"Hey, du kannst **[hier](https://top.gg/bot/{bot.user.id}/vote)** erneut für mich voten!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"{bot.user}", icon_url=bot.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    try:
                        await user.send(embed=embed, components=[
                            create_actionrow(
                                create_button(label="Vote", emoji=bot.get_emoji(927914707363455076), style=ButtonStyle.URL, url=f"https://top.gg/bot/{bot.user.id}/vote")
                            )
                        ])
                    except:
                        ""
                    async with bot.pool.acquire() as conn:
                        async with conn.cursor() as cursor:
                            await cursor.execute(f"UPDATE TopggVotes SET reminder= 'nein' WHERE user_id= {user.id}")
                    try:
                        guild = bot.get_guild(int(927591003764953158))
                        user1 = guild.get_member(user.id)
                        role = guild.get_role(int(937748061009109104))
                        await user1.remove_roles(role, reason="Topgg Vote")
                    except:
                        ""
                else:
                    user = bot.get_user(int(x[0]))
                    async with bot.pool.acquire() as conn:
                        async with conn.cursor() as cursor:
                            await cursor.execute(f"UPDATE TopggVotes SET reminder= 'nein' WHERE user_id= {user.id}")
                    try:
                        guild = bot.get_guild(int(927591003764953158))
                        user1 = guild.get_member(user.id)
                        role = guild.get_role(int(937748061009109104))
                        await user1.remove_roles(role, reason="Topgg Vote")
                    except:
                        ""
        await asyncio.sleep(30)


# ----------------------------------------------------------------------------------------------------------------------


bot.run("OTM0ODE3NDAzOTkxMzYzNjQ1.Ye1mjQ.Y7bM_sDvK1Pryz1UMQ9EFgTp-Hw") # EasyTicket


# ----------------------------------------------------------------------------------------------------------------------
