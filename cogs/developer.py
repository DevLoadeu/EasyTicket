import datetime
import math
import os
import io
import random
import sys
from discord.ext import commands
import discord
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option, wait_for_component
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import ButtonStyle
from contextlib import redirect_stdout
import inspect
import textwrap
import traceback
from collections import Counter



def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


class developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        embed1 = discord.Embed(title=f"__Vielen Dank__",
                               description=f"Hey, vielen Dank, dass ihr mich [eingeladen](https://discord.com/api/oauth2/authorize?client_id=934817403991363645&permissions=1099801422928&scope=bot%20applications.commands) habt!\n"
                                           f"Mit **/help** seht ihr alle Befehle, um mich startklar zumachen ;)\n\r"
                                           f"**Mit freundlichen Grüßen**\n"
                                           f"**{self.bot.user.name}**",
                               color=0x00ffff,
                               timestamp=datetime.datetime.utcnow())
        embed1.set_thumbnail(url=self.bot.user.avatar_url)
        embed1.set_footer(text=guild.name, icon_url=guild.icon_url)
        count = 1
        while True:
            channel = random.choice(guild.text_channels)
            count += 1
            try:
                await channel.send(embed=embed1, components=[
                    create_actionrow(
                        create_button(label="Invite", emoji=self.bot.get_emoji(927913230335098901), style=ButtonStyle.URL,
                                      url=f"https://discord.com/api/oauth2/authorize?client_id=934817403991363645&permissions=1099801422928&scope=bot%20applications.commands"),
                        create_button(label="Support", emoji=self.bot.get_emoji(929797411138854993), style=ButtonStyle.URL,
                                      url=f"https://discord.gg/Mzm8kK4a4q"),
                        create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076), style=ButtonStyle.URL,
                                      url=f"https://top.gg/bot/{self.bot.user.id}/vote")
                    )
                ])
                break
            except:
                if count == len(guild.text_channels):
                    break
                else:
                    ""

        member = 0
        bots = 0
        total = len(guild.members)
        rollen = len(guild.roles)
        text_channel = len(guild.text_channels)
        voice_channel = len(guild.voice_channels)
        channels = len(guild.channels)
        categorys = len(guild.categories)
        for x in guild.members:
            if x.bot:
                bots += 1
            else:
                member += 1
        embed = discord.Embed(title=f"__Neuer Server__",
                              description=f"Ich bin einem neuen Server beigetreten!",
                              color=0x26ff00,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text="Beigetreten:", icon_url=self.bot.user.avatar_url)
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Server Name", value=f"`{guild.name}`", inline=True)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Guild Icon", value=f"[klick]({guild.icon_url})", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False) # Platzhalter
        embed.add_field(name="Menschen", value=f"`{member}`", inline=True)
        embed.add_field(name="Bots", value=f"`{bots}`", inline=True)
        embed.add_field(name="Insgesamt", value=f"`{total}`", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Text Channel", value=f"`{text_channel}`", inline=True)
        embed.add_field(name="Voice Channel", value=f"`{voice_channel}`", inline=True)
        embed.add_field(name="Kategorien", value=f"`{categorys}`", inline=True)
        embed.add_field(name="Alle Channel", value=f"`{channels}`", inline=True)
        embed.add_field(name="Rollen", value=f"`{rollen}`", inline=True)
        embed.add_field(name="Inhaber", value=f"{guild.owner.mention} (`{guild.owner}`)", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Erstellt", value=f"<t:{int(float(guild.created_at.timestamp()))}> (<t:{int(float(guild.created_at.timestamp()))}:R>)")
        await self.bot.get_channel(934923267913945189).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        member = 0
        bots = 0
        total = len(guild.members)
        rollen = len(guild.roles)
        text_channel = len(guild.text_channels)
        voice_channel = len(guild.voice_channels)
        channels = len(guild.channels)
        categorys = len(guild.categories)
        for x in guild.members:
            if x.bot:
                bots += 1
            else:
                member += 1
        embed = discord.Embed(title=f"__Server verlassen__",
                              description=f"Ich bin einem Server geleavt!",
                              color=0xff0000,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text="Beigetreten:", icon_url=self.bot.user.avatar_url)
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Server Name", value=f"`{guild.name}`", inline=True)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Guild Icon", value=f"[klick]({guild.icon_url})", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Menschen", value=f"`{member}`", inline=True)
        embed.add_field(name="Bots", value=f"`{bots}`", inline=True)
        embed.add_field(name="Insgesamt", value=f"`{total}`", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Text Channel", value=f"`{text_channel}`", inline=True)
        embed.add_field(name="Voice Channel", value=f"`{voice_channel}`", inline=True)
        embed.add_field(name="Kategorien", value=f"`{categorys}`", inline=True)
        embed.add_field(name="Alle Channel", value=f"`{channels}`", inline=True)
        embed.add_field(name="Rollen", value=f"`{rollen}`", inline=True)
        embed.add_field(name="Inhaber", value=f"{guild.owner.mention} (`{guild.owner}`)", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Erstellt",
                        value=f"<t:{int(float(guild.created_at.timestamp()))}> (<t:{int(float(guild.created_at.timestamp()))}:R>)")
        await self.bot.get_channel(934923267913945189).send(embed=embed)

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(f"DELETE FROM LogChannel WHERE guild_id= {guild.id}")
                except:
                    ""
                try:
                    await cursor.execute(f"DELETE FROM TeamRollen WHERE guild_id= {guild.id}")
                except:
                    ""
                try:
                    await cursor.execute(f"DELETE FROM TicketKategorien WHERE guild_id= {guild.id}")
                except:
                    ""
                try:
                    await cursor.execute(f"DELETE FROM TicketPanels WHERE guild_id= {guild.id}")
                except:
                    ""
                try:
                    await cursor.execute(f"DELETE FROM Tickets WHERE guild_id= {guild.id}")
                except:
                    ""

    @cog_ext.cog_subcommand(base="developer", name="block-guild", description="Blockiere einen Server", options=[
        create_option(
            name="guildid",
            description="Die ID vom Server",
            required=True,
            option_type=3
        ),
        create_option(
            name="grund",
            description=f"Der Grund für die blockierung",
            required=False,
            option_type=3
        )
    ])
    @commands.is_owner()
    async def developer_block_guild(self, ctx: SlashContext, guildid: str, grund: str = None):
        if not grund:
            grund = "Nicht angegeben"
        try:
            guild = self.bot.fetch_guild(int(guildid))
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {guild.id}")
                    result = await cursor.fetchone()
                    if result != None:
                        return await ctx.reply(f"**Der Server ist bereits blockiert!**")
                    else:
                        await cursor.execute(f"INSERT INTO block_guilds (guild_id, reason) VALUES(%s,%s)",
                                             (guild.id, grund))
                        return await ctx.reply(f"Der Server **{guild.name}** wurde Erfolgreich blockiert!")
        except:
            ""

    @cog_ext.cog_subcommand(base="developer", name="block-user", description="Blockiere einen User", options=[
        create_option(
            name="userid",
            description="Die ID vom User",
            required=True,
            option_type=3
        ),
        create_option(
            name="grund",
            description=f"Der Grund für die blockierung",
            required=False,
            option_type=3
        )
    ])
    @commands.is_owner()
    async def developer_block_user(self, ctx: SlashContext, userid: str, grund: str = None):
        if not grund:
            grund = "Nicht angegeben"
        try:
            guild = self.bot.fetch_user(int(userid))
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {guild.id}")
                    result = await cursor.fetchone()
                    if result != None:
                        return await ctx.reply(f"**Der User `{guild}` ist bereits blockiert!**")
                    else:
                        await cursor.execute(f"INSERT INTO block_users (user_id, reason) VALUES(%s,%s)",
                                             (guild.id, grund))
                        return await ctx.reply(f"Der User **{guild.name}** wurde Erfolgreich blockiert!")
        except:
            ""

    @cog_ext.cog_subcommand(base="developer", name="unblock-guild", description="Entblockiere einen Server", options=[
        create_option(
            name="guildid",
            description="Die ID vom Server",
            required=True,
            option_type=3
        )
    ])
    @commands.is_owner()
    async def developer_unblock_guild(self, ctx: SlashContext, guildid: str):
        try:
            guild = self.bot.fetch_guild(int(guildid))
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {guild.id}")
                    result = await cursor.fetchone()
                    if result == None:
                        return await ctx.reply(f"**Der Server ist nicht blockiert!**")
                    else:
                        await cursor.execute(f"DELETE FROM block_guilds WHERE guild_id= {guild.id}")
                        return await ctx.reply(f"Der Server **{guild.name}** wurde Erfolgreich entblockiert!")
        except:
            ""

    @cog_ext.cog_subcommand(base="developer", name="unblock-user", description="unnlockiere einen User", options=[
        create_option(
            name="userid",
            description="Die ID vom User",
            required=True,
            option_type=3
        )
    ])
    @commands.is_owner()
    async def developer_block_guild(self, ctx: SlashContext, userid: str):
        try:
            guild = self.bot.fetch_user(int(userid))
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {guild.id}")
                    result = await cursor.fetchone()
                    if result != None:
                        return await ctx.reply(f"**Der User `{guild}` ist nicht blockiert!**")
                    else:
                        await cursor.execute(f"DELETE FROM block_users WHERE user_id= {guild.id}")
                        return await ctx.reply(f"Der User **{guild.name}** wurde Erfolgreich entblockiert!")
        except:
            ""

    @cog_ext.cog_subcommand(base="developer", name="serverinfo", options=[
        create_option(
            name="guildid",
            description="Die ID vom Server",
            required=False,
            option_type=3
        )
    ])
    @commands.is_owner()
    async def developer_serverinfo(self, ctx: SlashContext, guildid: str = None):
        if not guildid:
            guildid = ctx.guild.id
        guild = self.bot.get_guild(int(guildid))
        member = 0
        bots = 0
        total = len(guild.members)
        rollen = len(guild.roles)
        text_channel = len(guild.text_channels)
        voice_channel = len(guild.voice_channels)
        channels = len(guild.channels)
        categorys = len(guild.categories)
        for x in guild.members:
            if x.bot:
                bots += 1
            else:
                member += 1
        embed = discord.Embed(title=f"__Serverinfo__",
                              description=f"Hier sind Infos über den Server!",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text="Beigetreten:", icon_url=self.bot.user.avatar_url)
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Server Name", value=f"`{guild.name}`", inline=True)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Guild Icon", value=f"[klick]({guild.icon_url})", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Menschen", value=f"`{member}`", inline=True)
        embed.add_field(name="Bots", value=f"`{bots}`", inline=True)
        embed.add_field(name="Insgesamt", value=f"`{total}`", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Text Channel", value=f"`{text_channel}`", inline=True)
        embed.add_field(name="Voice Channel", value=f"`{voice_channel}`", inline=True)
        embed.add_field(name="Kategorien", value=f"`{categorys}`", inline=True)
        embed.add_field(name="Alle Channel", value=f"`{channels}`", inline=True)
        embed.add_field(name="Rollen", value=f"`{rollen}`", inline=True)
        embed.add_field(name="Inhaber", value=f"{guild.owner.mention} (`{guild.owner}`)", inline=True)
        embed.add_field(name="⠀", value="⠀", inline=False)  # Platzhalter
        embed.add_field(name="Erstellt",
                        value=f"<t:{int(float(guild.created_at.timestamp()))}> (<t:{int(float(guild.created_at.timestamp()))}:R>)")
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_subcommand(base="developer", name="restart", description="Restarte den kompletten Bot")
    @commands.is_owner()
    async def developer_restart(self, ctx: SlashContext):
        embed = discord.Embed(title=f"__Restart__",
                              description=f"Der Bot restartet sich jetzt!\n"
                                          f"<a:loading:929777766340120657> Bitte warte einen Moment... <a:loading:929777766340120657>",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="restarting..."))
        restart_program()

    @cog_ext.cog_subcommand(base="developer", name="shutdown", description=f"Fahre den Bot herunter")
    @commands.is_owner()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _developer_shutdown(self, ctx: SlashContext):
        await ctx.send(f"Der Bot geht nun offline!")
        await self.bot.change_presence(status=discord.Status.offline)
        await self.bot.logout()

    @cog_ext.cog_subcommand(base="developer", name="leave-guild", description=f"Leave einen Server mit dem Bot",
                            options=[
                                create_option(
                                    name="guildid",
                                    description="the guild id",
                                    required=True,
                                    option_type=3
                                )
                            ])
    @commands.guild_only()
    @commands.is_owner()
    async def _leaveguild(self, ctx, *, guildid: str):
        guild = self.bot.get_guild(guildid)
        await guild.leave()
        await ctx.reply(f"Ich bin dem Server `{guild.name}` Erfolgreich geleavt!")

    @cog_ext.cog_subcommand(base="developer", name="reload", description=f"Reload all cogs")
    @commands.guild_only()
    @commands.is_owner()
    async def _reload(self, ctx):
        liste = ""
        await ctx.send(f"Ich restarte mich nun!")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
                liste += f"{filename[:-3]}\n"
        embed = discord.Embed(title=f"__System - Restart__",
                              description=f"The following files were successfully restarted:\n\r"
                                          f"```{liste}```",
                              color=0x00ffff,
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="developer", name="load-cog", description=f"Load a cog", options=[
        create_option(
            name="filename",
            description="The Filename of the cog",
            required=True,
            option_type=3
        )
    ])
    @commands.guild_only()
    @commands.is_owner()
    async def _loadcog(self, ctx, filename: str):
        if filename.endswith('.py'):
            cog = ""
            for filename1 in os.listdir('./cogs'):
                if filename.lower() == filename1.lower():
                    cog += filename1[:-3]
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.reply(f"Der cog **{cog}** wurde erfolgreich geladen!")
        else:
            await ctx.reply(f"Die Angegebene Datei endet nicht mit .py!")

    @cog_ext.cog_subcommand(base="developer", name="reload-cog", description=f"Reload a cog", options=[
        create_option(
            name="filename",
            description="The Filename of the cog",
            required=True,
            option_type=3
        )
    ])
    @commands.guild_only()
    @commands.is_owner()
    async def _reloadcog(self, ctx, filename: str):
        if filename.endswith('.py'):
            cog = ""
            for filename1 in os.listdir('./cogs'):
                if filename.lower() == filename1.lower():
                    cog += filename1[:-3]
            self.bot.reload_extension(f'cogs.{cog}')
            await ctx.reply(f"Der cog **{cog}** wurde erfolgreich reloaded!")
        else:
            await ctx.reply(f"Die Angegebene Datei endet nicht mit .py!")

    @cog_ext.cog_subcommand(base="developer", name="unload-cog", description=f"Unload a cog", options=[
        create_option(
            name="filename",
            description="The Filename of the cog",
            required=True,
            option_type=3
        )
    ])
    @commands.guild_only()
    @commands.is_owner()
    async def _unloadcog(self, ctx, filename: str):
        if filename.endswith('.py'):
            cog = ""
            for filename1 in os.listdir('./cogs'):
                if filename.lower() == filename1.lower():
                    cog += filename1[:-3]
            self.bot.unload_extension(f'cogs.{cog}')
            await ctx.reply(f"Der cog **{cog}** wurde erfolgreich entladen!")
        else:
            await ctx.reply(f"Die Angegebene Datei endet nicht mit .py!")

    @cog_ext.cog_subcommand(base="developer", name="guilds", description=f"Show all guilds")
    @commands.guild_only()
    @commands.is_owner()
    async def _guilds(self, ctx):
        msg = ""
        page = 1
        items_per_page = 10
        pages = math.ceil(len(self.bot.guilds) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue = ''
        thingies = []
        for i, guild in enumerate(self.bot.guilds[start:end], start=start):
            thingies.append(
                '**{}** `|` **{}** `|` **{}** User `|` **{}** \n\r'.format(guild.name, guild.id,
                                                                           guild.member_count,
                                                                           guild.owner))
        thingies.sort()
        msg += ''.join(thingies)
        msg += ''
        embed = discord.Embed(title=f"__System - Server__",
                              description=f"{msg} {queue}",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'Page: {page}/{pages}')
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        buttons = [
            create_actionrow(
                create_button(emoji="◀", custom_id="links", style=ButtonStyle.blue),
                create_button(emoji="🏠", custom_id="home", style=ButtonStyle.green),
                create_button(emoji="▶", custom_id="rechts", style=ButtonStyle.blue),
                create_button(emoji="❌", custom_id="stop", style=ButtonStyle.red)
            )
        ]
        mess = await ctx.send(embed=embed, components=buttons)
        page1 = 1
        while True:
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=buttons,
                                                                    timeout=120)
            if button_ctx.custom_id == "links":
                if page1 != 1:
                    page1 -= 1
                elif page1 == 1:
                    page1 += pages - 1
            elif button_ctx.custom_id == "home":
                page1 -= page1 - 1
            elif button_ctx.custom_id == "rechts":
                if page1 != pages:
                    page1 += 1
                elif page1 == pages:
                    page1 -= pages
                    page1 += 1
            elif button_ctx.custom_id == "stop":
                await mess.edit(embed=embed, components=[
                    create_actionrow(
                        create_button(emoji="◀", custom_id="links", style=ButtonStyle.blue, disabled=True),
                        create_button(emoji="🏠", custom_id="home", style=ButtonStyle.green, disabled=True),
                        create_button(emoji="▶", custom_id="rechts", style=ButtonStyle.blue, disabled=True),
                        create_button(emoji="❌", custom_id="stop", style=ButtonStyle.red, disabled=True)
                    )
                ])
                return
            try:
                await button_ctx.reply(
                    content="",
                    hidden=True
                )
            except:
                ""
            items_per_page1 = 10
            msg1 = ""
            pages1 = math.ceil(len(self.bot.guilds) / items_per_page)
            start1 = (page1 - 1) * items_per_page1
            end1 = start1 + items_per_page1
            queue1 = ''
            thingies1 = []
            for i, guild in enumerate(self.bot.guilds[start1:end1], start=start1):
                thingies1.append(
                    '**{}** `|` **{}** `|` **{}** User `|` **{}** \n\r'.format(guild.name, guild.id,
                                                                               guild.member_count,
                                                                               guild.owner))
            thingies1.sort()
            msg1 += ''.join(thingies1)
            msg1 += ''
            embed1 = discord.Embed(title=f"__System - Server__",
                                   description=f"{msg1} {queue1}",
                                   color=0x00ffff,
                                   timestamp=datetime.datetime.utcnow())
            embed1.set_author(name=f'Page: {page1}/{pages1}')
            embed1.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await mess.edit(embed=embed1)

    @cog_ext.cog_subcommand(base="developer", name="datenbank")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def db(self, ctx: SlashContext):
        dever = [473737542630637569, 441260395416780820]  # ToXy ; Fabio
        if ctx.author.id in dever:
            pool = self.bot.pool
            embed = discord.Embed(color=0x00ffff)
            embed.add_field(name="Minsize", value=pool.minsize, inline=False)
            embed.add_field(name="Maxsize", value=pool.maxsize, inline=False)
            embed.add_field(name="Size", value=pool.size, inline=False)
            embed.add_field(name="Freesize", value=pool.freesize, inline=False)
            embed.add_field(name="Used", value=pool.size - pool.freesize, inline=False)
            await ctx.send(embed=embed)
        if ctx.author.id not in dever:
            notdevembed = discord.Embed(title=':attention~2: | **Error**', description='You are not a developer!',
                                        color=discord.colour.Color.dark_red())
            await ctx.send(embed=notdevembed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, ex):
        embed = discord.Embed(title=f"__Error__",
                              description=f"**Command:** {ctx.command}\n"
                                          f"**User:** {ctx.author}\n\r"
                                          f"**Error:** `{ex}`",
                              color=0xff0000,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed, components=[
            create_actionrow(
                create_button(label="Support Server", emoji=self.bot.get_emoji(929797411138854993),
                              style=ButtonStyle.URL, url=f"https://discord.gg/Mzm8kK4a4q")
            )
        ], hidden=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            embed = discord.Embed(title=f"__Error__",
                                  description=f"**Command:** {ctx.command}\n"
                                              f"**User:** {ctx.author}\n\r"
                                              f"**Error:** `{error}`",
                                  color=0xff0000,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed, components=[
                create_actionrow(
                    create_button(label="Support Server", emoji=self.bot.get_emoji(929797411138854993),
                                  style=ButtonStyle.URL, url=f"https://discord.gg/Mzm8kK4a4q")
                )
            ], delete_after=10.0)

    @commands.Cog.listener()
    async def on_slash_command(self, ctx: SlashContext):
        if ctx.subcommand_name:
            await self.bot.get_channel(934923390979039272).send(f"⠀\n> **/{ctx.command} {ctx.subcommand_name}**\n\r"
                                                                f"**User:** `{ctx.author}`\n"
                                                                f"**ID:** `{ctx.author.id}`\n\r"
                                                                f"**Server:** `{ctx.guild.name}`\n"
                                                                f"**ID:** `{ctx.guild.id}`")
        else:
            await self.bot.get_channel(934923390979039272).send(
                f"⠀\n> **/{ctx.command}**\n\r"
                f"**User:** `{ctx.author}`\n"
                f"**ID:** `{ctx.author.id}`\n\r"
                f"**Server:** `{ctx.guild.name}`\n"
                f"**ID:** `{ctx.guild.id}`")

    @commands.command(name='eval')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _eval(self, ctx, *, body):
        devs = [473737542630637569]
        if ctx.author.id in devs:
            """Evaluates python code"""
            env = {
                'self': self,
                'ctx': ctx,
                'bot': self.bot,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                'source': inspect.getsource,
                '_channel': ctx.channel
            }

            def cleanup_code(content):
                """Automatically removes code blocks from the code."""
                # remove ```py\n```
                if content.startswith('```') and content.endswith('```'):
                    return '\n'.join(content.split('\n')[1:-1])

                # remove `foo`
                return content.strip('` \n')

            env.update(globals())

            body = cleanup_code(body)
            stdout = io.StringIO()
            err = out = None

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            def paginate(text: str):
                """Simple generator that paginates text."""
                last = 0
                pages = []
                for curr in range(0, len(text)):
                    if curr % 1980 == 0:
                        pages.append(text[last:curr])
                        last = curr
                        appd_index = curr
                if appd_index != len(text)-1:
                    pages.append(text[last:curr])
                return list(filter(lambda a: a != '', pages))

            try:
                exec(to_compile, env)
            except Exception as e:
                err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
                return await ctx.message.add_reaction('\u2049')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                if ret is None:
                    if value:
                        try:

                            out = await ctx.send(f'```py\n{value}\n```')
                        except:
                            paginated_text = paginate(value)
                            for page in paginated_text:
                                if page == paginated_text[-1]:
                                    out = await ctx.send(f'```py\n{page}\n```')
                                    break
                                await ctx.send(f'```py\n{page}\n```')
                else:
                    try:
                        out = await ctx.send(f'```py\n{value}{ret}\n```')
                    except:
                        paginated_text = paginate(f"{value}{ret}")
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')

            if out:
                await ctx.message.add_reaction('\u2705')  # tick
            elif err:
                await ctx.message.add_reaction('\u2049')  # x
            else:
                await ctx.message.add_reaction('\u2705')
        if not ctx.author.id in devs:
            notdevembed = discord.Embed(title='<a:warning:928177073363746847> | **Error**',
                                        description='You are not a developer!', color=discord.colour.Color.dark_red())
            await ctx.send(embed=notdevembed)



# ----------------------------------------------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(developer(bot))
