import datetime
import discord
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option, wait_for_component, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext, SlashContext


class SettingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="log-channel", name="set", description="Setze den Log Channel für Tickets", options=[
        create_option(
            name="channel",
            description="Der Channel, wo alles geloggt werden soll",
            option_type=7,
            required=True
        )
    ])
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(read_messages=True, send_messages=True)
    async def log_channel_set(self, ctx: SlashContext, channel: discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
                                          color=0xff0000,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, components=[
                        create_actionrow(
                            create_button(label="Support Server", emoji=self.bot.get_emoji(929797411138854993), style=ButtonStyle.URL, url=f"https://discord.gg/Mzm8kK4a4q")
                        )
                    ], hidden=True)

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT channel_id FROM LogChannel WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute(f"INSERT INTO LogChannel (guild_id, channel_id) VALUES(%s,%s)",
                                         (ctx.guild.id, channel.id))
                    embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                          description=f"Alle Logs von Tickets werden nun in {channel.mention} gesendet!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)
                elif result != None:
                    await cursor.execute(f"UPDATE LogChannel SET channel_id= {channel.id} WHERE guild_id= {ctx.guild.id}")
                    embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                          description=f"Alle Logs von Tickets werden nun in {channel.mention} gesendet!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="log-channel", name="remove", description="Entferne den Log Channel von Tickets")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def log_channel_remove(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT channel_id FROM LogChannel WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Dieser Server hat keinen LogChannel gesetzt`",
                                          color=0xff0000,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, components=[
                        create_actionrow(
                            create_button(label="Support Server", emoji=self.bot.get_emoji(929797411138854993),
                                          style=ButtonStyle.URL, url=f"https://discord.gg/Mzm8kK4a4q")
                        )
                    ], hidden=True)
                elif result != None:
                    await cursor.execute(f"DELETE FROM LogChannel WHERE guild_id= {ctx.guild.id}")
                    embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                          description=f"Der Log Channel (<#{int(result[0])}>) wurde Erfolgreich entfernt!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="log-channel", name="show", description="Siehe den Log Channel von Tickets")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def log_channel_show(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT channel_id FROM LogChannel WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Dieser Server hat keinen LogChannel gesetzt`",
                                          color=0xff0000,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, components=[
                        create_actionrow(
                            create_button(label="Support Server", emoji=self.bot.get_emoji(929797411138854993),
                                          style=ButtonStyle.URL, url=f"https://discord.gg/Mzm8kK4a4q")
                        )
                    ], hidden=True)
                elif result != None:
                    embed = discord.Embed(title=f"<:channel:934837655273898054> LogChannel",
                                          description=f"Der LogChannel auf diesem Server ist {self.bot.get_channel(int(result[0])).mention}!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="panel", name="create", description="Erstelle ein Support Panel", options=[
        create_option(
            name="channel",
            description="Der Channel, wo das Panel sein soll",
            option_type=7,
            required=True
        ),
        create_option(
            name="thema",
            description="Das Thema vom Ticket",
            option_type=3,
            required=True
        )
    ])
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_guild_permissions(send_messages=True, manage_channels=True, read_messages=True)
    async def panel_create(self, ctx: SlashContext, channel: discord.TextChannel, thema: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
        embed = discord.Embed(title=f"__Ticket Support__",
                              description=f"**Thema:** {thema}\n\r"
                                          f"Bitte klicke unten auf den Button, um ein Ticket zum Thema zu erstellen!",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        message = await channel.send(embed=embed, components=[
            create_actionrow(
                create_button(label="Ticket erstellen", emoji=self.bot.get_emoji(929797411138854993), style=ButtonStyle.blue, custom_id="create_ticket")
            )
        ])
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"INSERT INTO TicketPanels (guild_id, channel_id, message_id, thema) VALUES(%s,%s,%s,%s)",
                                     (ctx.guild.id, channel.id, message.id, thema))
                embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                      description=f"Das Panel mit dem Thema **{thema}** wurde Erfolgreich im Channel {channel.mention} erstellt!",
                                      color=0x00ffff,
                                      timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="panel", name="delete", description="Lösche ein Support Panel", options=[
        create_option(
            name="channel",
            description="Der Channel, wo das Panel ist",
            option_type=7,
            required=True
        ),
        create_option(
            name="thema",
            description="Das Thema vom Ticket",
            option_type=3,
            required=True
        )
    ])
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def panel_delete(self, ctx: SlashContext, channel: discord.TextChannel, thema: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT message_id FROM TicketPanels WHERE guild_id= {ctx.guild.id} AND channel_id= {channel.id} AND thema= '{thema}'")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Es wurde im angegebenen Channel kein Panel mit dem Thema gefunden`",
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
                elif result != None:
                    mess = await channel.fetch_message(int(result[0]))
                    await cursor.execute(f"DELETE FROM TicketPanels WHERE guild_id= {ctx.guild.id} AND channel_id= {channel.id} AND message_id= {mess.id} AND thema= '{thema}'")
                    try:
                        await mess.delete()
                    except:
                        ""
                    embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                          description=f"Das Panel mit dem Thema **{thema}** wurde Erfolgreich im Channel {channel.mention} gelöscht!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="panel", name="show", description="Siehe eine Liste mit allen Panels!")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def panel_show(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT * FROM TicketPanels WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
        liste = ""
        count = 1
        if result != None:
            for x in result:
                try:
                    channel = self.bot.get_channel(int(x[1]))
                    message = await channel.fetch_message(int(x[2]))
                    thema = str(x[3])
                    liste += f"{count}. `|` {channel.mention} `|` [klick]({message.jump_url}) `|` {thema}\n"
                    count += 1
                except:
                    ""
            if liste == "":
                liste = "Dieser Server hat keine Panel erstellt!"
            embed = discord.Embed(title=f"<:support:929797411138854993> Panel",
                                  description=liste,
                                  color=0x00ffff,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed, hidden=False)
        else:
            embed = discord.Embed(title=f"<:support:929797411138854993> Panel",
                                  description="Dieser Server hat keine Panel erstellt!",
                                  color=0x00ffff,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="team", name="set", description="Setze die Team Rolle für Tickets", options=[
        create_option(
            name="role",
            description="Die neue Team Rolle",
            option_type=8,
            required=True
        )
    ])
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def team_set(self, ctx: SlashContext, role: discord.Role):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT role_id FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute(f"INSERT INTO TeamRollen (guild_id, role_id) VALUES(%s,%s)",
                                         (ctx.guild.id, role.id))
                else:
                    await cursor.execute(f"UPDATE TeamRollen SET role_id= {role.id} WHERE guild_id= {ctx.guild.id}")
                embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                      description=f"Die Team Rolle wurde Erfolgreich auf {role.mention} aktualisiert!",
                                      color=0x00ffff,
                                      timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="team", name="remove", description="Entferne die Team Rolle für Tickets")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def team_remove(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT role_id FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server hat keine Team Rolle hinzugefügt`",
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
                else:
                    await cursor.execute(f"DELETE FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                    embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                          description=f"Die Team Rolle wurde Erfolgreich entfernt!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="team", name="show", description="Zeige die Team Rolle für Tickets an")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def team_show(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT role_id FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server hat keine Team Rolle hinzugefügt`",
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
                else:
                    embed = discord.Embed(title=f"<:role:934853217832026112> Team Role",
                                          description=f"Die Team Rolle für diesen Server ist {ctx.guild.get_role(int(result[0])).mention}!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="kategorie", name="set", description="Setze die Ticket Kategorie", options=[
        create_option(
            name="kategorie",
            description=f"Wähle die Ticket Kategorie",
            option_type=7,
            required=True
        )
    ])
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def kategorie_set(self, ctx: SlashContext, kategorie: discord.CategoryChannel):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                if kategorie not in ctx.guild.categories:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Unbekannte Kategorie (stelle sicher, dass es kein Channel war)`",
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
                await cursor.execute(f"SELECT channel_id FROM TicketKategorien WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute(f"INSERT INTO TicketKategorien (guild_id, channel_id) VALUES(%s,%s)",
                                         (ctx.guild.id, kategorie.id))
                else:
                    await cursor.execute(f"UPDATE TicketKategorien SET channel_id= {kategorie.id} WHERE guild_id= {ctx.guild.id}")
                embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                      description=f"Die Kategorie wurde Erfolgreich auf `{kategorie.name}` aktualisiert!",
                                      color=0x00ffff,
                                      timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="kategorie", name="remove", description="Entferne die Ticket Kategorie")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def kategorie_remove(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT channel_id FROM TicketKategorien WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server hat keine Ticket Kategorie hinzugefügt`",
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
                else:
                    await cursor.execute(f"DELETE FROM TicketKategorien WHERE guild_id= {ctx.guild.id}")
                    embed = discord.Embed(title=f"<a:verify:928217775175000074> Erfolgreich",
                                          description=f"Die Kategorie wurde Erfolgreich gelöscht!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_subcommand(base="kategorie", name="show", description="Siehe die Ticket Kategorie")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def kategorie_show(self, ctx: SlashContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server wurde vom Bot gesperrt`",
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

                await cursor.execute(f"SELECT reason FROM block_users WHERE user_id= {ctx.author.id}")
                result_block_users = await cursor.fetchone()
                if result_block_users != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Du wurdest vom Bot gesperrt`",
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
                await cursor.execute(f"SELECT channel_id FROM TicketKategorien WHERE guild_id= {ctx.guild.id}")
                result = await cursor.fetchone()
                if result == None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** {ctx.command}\n"
                                                      f"**User:** {ctx.author}\n\r"
                                                      f"**Error:** `Der Server hat keine Ticket Kategorie hinzugefügt`",
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
                else:
                    embed = discord.Embed(title=f"<:role:934853217832026112> Kategorie",
                                          description=f"Die Kategorie für diesen Server ist `{self.bot.get_channel(int(result[0])).name}`!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed, hidden=False)


# ----------------------------------------------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(SettingCommands(bot))
