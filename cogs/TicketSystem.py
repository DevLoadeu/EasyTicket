import asyncio
import datetime
import io
import time
import chat_exporter
import discord
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option, \
    wait_for_component, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext, SlashContext


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT reason FROM block_guilds WHERE guild_id= {ctx.guild.id}")
                result_block_guilds = await cursor.fetchone()
                if result_block_guilds != None:
                    embed = discord.Embed(title=f"__Error__",
                                          description=f"**Command:** Button Click\n"
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
        if ctx.custom_id == "create_ticket":
            await ctx.defer(hidden=True)
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT thema FROM TicketPanels WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id} AND message_id= {ctx.origin_message.id}")
                    result = await cursor.fetchone()
            if result == None:
                return
            thema = f"{result[0]}"

            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT * FROM Tickets WHERE guild_id= {ctx.guild.id} AND user_id= {ctx.author.id} AND thema= '{thema}'")
                    result = await cursor.fetchone()
            if result != None:
                return await ctx.reply(
                    content=f"<:no:928217870498938940> **Du kannst nur ein Ticket pro Thema öffnen!** <:no:928217870498938940>",
                    hidden=True)

            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT role_id FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                    result_team = await cursor.fetchone()
                    await cursor.execute(f"SELECT channel_id FROM TicketKategorien WHERE guild_id= {ctx.guild.id}")
                    result_kategorie = await cursor.fetchone()
                    await cursor.execute(f"SELECT channel_id FROM LogChannel WHERE guild_id= {ctx.guild.id}")
                    result_log = await cursor.fetchone()
            if result_team == None:
                return await ctx.reply(
                    content=f"<:no:928217870498938940> **Der Server hat keine Team Rolle hinzugefügt!** <:no:928217870498938940>", hidden=True)
            if result_kategorie != None:
                kategorie1 = self.bot.get_channel(int(result_kategorie[0]))
                if kategorie1 in ctx.guild.categories:
                    kategorie = kategorie1
                else:
                    kategorie = None
            else:
                kategorie = None
            team_role = ctx.guild.get_role(int(result_team[0]))
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                team_role: discord.PermissionOverwrite(view_channel=True, send_messages=False, read_messages=True),
                ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
                self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, manage_messages=True, manage_channels=True)
            }
            try:
                ticket = await ctx.guild.create_text_channel(name=f"『🚨』{ctx.author}", overwrites=overwrites,
                                                             reason="Ticket eröffnet", category=kategorie)
            except Exception as e:
                embed = discord.Embed(title=f"__Error__",
                                      description=f"**Command:** Button klick\n"
                                                  f"**User:** {ctx.author}\n\r"
                                                  f"**Error:** `{e}`",
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
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"INSERT INTO Tickets (guild_id, channel_id, user_id, mod_id, thema) VALUES(%s,%s,%s,%s,%s)",
                        (ctx.guild.id, ticket.id, ctx.author.id, 0, thema))
            embed_log = discord.Embed(title=f"__Neues Ticket__",
                                      description=f"**User:** {ctx.author.mention} (`{ctx.author}`)\n"
                                                  f"**ID:** {ctx.author.id}\n\r"
                                                  f"**Ticket Channel:** {ticket.mention} (`{ticket.name}`)\n"
                                                  f"**Ticket Grund:** {thema}\n"
                                                  f"**Ticket erstellt:** <t:{int(float(time.time()))}> (<t:{int(float(time.time()))}:R>)",
                                      color=0x00ffff,
                                      timestamp=datetime.datetime.utcnow())
            embed_log.set_thumbnail(url=ctx.author.avatar_url)
            embed_log.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed_log.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            if result_log != None:
                try:
                    await self.bot.get_channel(int(result_log[0])).send(embed=embed_log)
                except:
                    ""
            embed = discord.Embed(title=f"__Ticket Support__",
                                  description=f"**Thema:** {thema}\n\r"
                                              f"**User:** {ctx.author}\n"
                                              f"**ID:** {ctx.author.id}\n\r"
                                              f"**Ticket erstellt:** <t:{int(float(time.time()))}> (<t:{int(float(time.time()))}:R>)",
                                  color=0x00ffff,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url,
                             url="https://discord.com/api/oauth2/authorize?client_id=934817403991363645&permissions=1099801422928&scope=bot%20applications.commands")
            try:
                mess = await ticket.send(f"**Team:** {team_role.mention} | **User:** {ctx.author.mention}", embed=embed,
                                         components=[
                                             create_actionrow(
                                                 create_button(emoji=self.bot.get_emoji(929821713485688922),
                                                               custom_id="ticket_close",
                                                               style=ButtonStyle.red),
                                                 create_button(emoji=self.bot.get_emoji(929807213189529731),
                                                               custom_id="ticket_claim",
                                                               style=ButtonStyle.green),
                                                 create_button(emoji=self.bot.get_emoji(929822715609747526),
                                                               custom_id="ticket_info",
                                                               style=ButtonStyle.blue)
                                             )
                                         ])
                await mess.pin()
            except Exception as e:
                embed = discord.Embed(title=f"__Error__",
                                      description=f"**Command:** Button klick\n"
                                                  f"**User:** {ctx.author}\n\r"
                                                  f"**Error:** `{e}`",
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
            await ctx.send(
                f"<a:information:928176894564794369> Das Ticket wurde Erfolgreich erstellt! <a:information:928176894564794369>\n"
                f"Dein Ticket: {ticket.mention}", hidden=True)

        elif ctx.custom_id == "ticket_close":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT * FROM Tickets WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id}")
                    result_ticket = await cursor.fetchone()
                    await cursor.execute(f"SELECT role_id FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                    result_team = await cursor.fetchone()
            if result_ticket == None:
                return
            if result_team == None:
                team_role = ctx.guild.default_role
            else:
                try:
                    team_role = ctx.guild.get_role(int(result_team[0]))
                except:
                    team_role = ctx.guild.default_role
            if team_role not in ctx.author.roles:
                return await ctx.reply(
                    content=f"<:no:928217870498938940> **Nur Teammitglieder können Tickets schließen!** <:no:928217870498938940>", hidden=True)
            embed = discord.Embed(title=f"Soll das Ticket wirklich geschlossen werden?",
                                  color=0x00ffff)
            buttons = create_actionrow(
                create_button(emoji=self.bot.get_emoji(927908513114628116), custom_id="ticket_close_yes",
                              style=ButtonStyle.green),
                create_button(emoji=self.bot.get_emoji(928217870498938940), custom_id="ticket_close_no",
                              style=ButtonStyle.red)
            )
            mess1 = await ctx.send(embed=embed, components=[buttons], hidden=False)
            try:
                button_ctx: ComponentContext = await wait_for_component(self.bot, components=buttons, timeout=120)
            except asyncio.TimeoutError:
                return await mess1.delete()
            if button_ctx.custom_id == "ticket_close_yes":
                embed_close = discord.Embed(title=f"__Ticket Support__",
                                            description=f"<a:loading:929777766340120657> Ticket Transkript wird erstellt, dieser Vorgang kann einige Sekunden dauern <a:loading:929777766340120657>",
                                            color=0x00ffff)
                mess_close = await button_ctx.send(embed=embed_close)
                embed = discord.Embed(title=f"__Ticket Support__",
                                      description=f"Das Ticket wird in 5 Sekunden gelöscht!",
                                      color=0x00ffff,
                                      timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

                embed2 = discord.Embed(title=f"__Ticket System__",
                                       description=f"**Ticket Owner:** {self.bot.get_user(int(result_ticket[2])).mention} ({self.bot.get_user(int(result_ticket[2]))})\n"
                                                   f"**Ticket Name:** {ctx.channel.name}\n"
                                                   f"**Ticket Thema:** {str(result_ticket[4])}\n"
                                                   f"**Ticket Server:** {ctx.guild.name}\n\r"
                                                   f"**Geschlossen von:** {ctx.author.mention} ({ctx.author})\n"
                                                   f"**Geschlossen am:** <t:{int(float(time.time()))}> (<t:{int(float(time.time()))}:R>)",
                                       color=0x00ffff,
                                       timestamp=datetime.datetime.utcnow())
                embed2.set_thumbnail(url=ctx.guild.icon_url)
                embed2.set_author(name=self.bot.get_user(int(result_ticket[2])),
                                  icon_url=self.bot.get_user(int(result_ticket[2])).avatar_url)
                embed2.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
                transcript = await chat_exporter.export(
                    ctx.channel,
                    limit=1000,
                )

                if transcript is None:
                    return

                transcript_file = discord.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{ctx.channel.name}.html",
                )
                try:
                    await self.bot.get_user(int(result_ticket[2])).send(embed=embed2, file=transcript_file)
                except:
                    ""
                async with self.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(f"SELECT channel_id FROM LogChannel WHERE guild_id= {ctx.guild.id}")
                        result_log = await cursor.fetchone()
                if result_log != None:
                    transcript1 = await chat_exporter.export(
                    	ctx.channel,
                    	limit=1000,
                    )
                    transcript_file1 = discord.File(
                        io.BytesIO(transcript1.encode()),
                        filename=f"transcript-{ctx.channel.name}.html",
                    )
                    channel_log = self.bot.get_channel(int(result_log[0]))
                    await channel_log.send(embed=embed2, file=transcript_file1)
                try:
                    await ctx.channel.edit(overwrites={
                        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        self.bot.get_user(int(result_ticket[2])): discord.PermissionOverwrite(view_channel=True,
                                                                                              send_messages=False,
                                                                                              read_messages=True),
                        team_role: discord.PermissionOverwrite(view_channel=True, send_messages=False,
                                                               read_messages=True),
                        self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                                   read_messages=True, manage_messages=True, manage_channels=True)
                    })
                except:
                    ""
                await mess_close.edit(embed=embed)
                async with self.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(f"DELETE FROM Tickets WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id}")
                await asyncio.sleep(5)
                await ctx.channel.delete()
            elif button_ctx.custom_id == "ticket_close_no":
                await mess1.delete()
        elif ctx.custom_id == "ticket_claim":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT * FROM Tickets WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id}")
                    result = await cursor.fetchone()
                    await cursor.execute(f"SELECT role_id FROM TeamRollen WHERE guild_id= {ctx.guild.id}")
                    result_team_role = await cursor.fetchone()
            if result == None:
                return
            if result_team_role == None:
                await ctx.defer(hidden=True)
                return await ctx.reply(content=f"Ich konnte keine Team Rolle finden!", hidden=True)
            team = ctx.guild.get_role(int(result_team_role[0]))
            if team not in ctx.author.roles:
                await ctx.defer(hidden=True)
                return await ctx.send(f"<:no:928217870498938940> **Nur Teammitglieder können Tickets claimen!**", hidden=True)
            if int(result[3]) == 0:
                await ctx.defer()
                user = ctx.guild.get_member(int(result[2]))
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    team: discord.PermissionOverwrite(view_channel=False),
                    ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                            read_messages=True),
                    user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
                    self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True, manage_messages=True, manage_channels=True)
                }
                await ctx.channel.edit(overwrites=overwrites)
                async with self.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(
                            f"UPDATE Tickets SET mod_id= {ctx.author.id} WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id}")
                embed = discord.Embed(title=f"__Ticket System__",
                                      description=f"Das Ticket wurde Erfolgreich von **{ctx.author}** geclaimt!",
                                      color=0x00ffff,
                                      timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            elif int(result[3]) != 0:
                if int(result[3]) == ctx.author.id:
                    await ctx.defer()
                    team = ctx.guild.get_role(int(result_team_role[0]))
                    user = ctx.guild.get_member(int(result[2]))
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        team: discord.PermissionOverwrite(view_channel=True, send_messages=False,
                                                          read_messages=True),
                        user: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                          read_messages=True),
                        self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                                   read_messages=True, manage_messages=True, manage_channels=True)
                    }
                    await ctx.channel.edit(overwrites=overwrites)
                    async with self.bot.pool.acquire() as conn:
                        async with conn.cursor() as cursor:
                            await cursor.execute(
                                f"UPDATE Tickets SET mod_id= 0 WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id}")
                    embed = discord.Embed(title=f"__Ticket System__",
                                          description=f"Das Ticket wurde Erfolgreich von **{ctx.author}** freigegeben!",
                                          color=0x00ffff,
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed)
                else:
                    await ctx.defer(hidden=True)
                    return await ctx.send(
                        f"<:no:928217870498938940> **Das Ticket ist bereits geclaimt!** <:no:928217870498938940>",
                        hidden=True)
        elif ctx.custom_id == "ticket_info":
            await ctx.defer(hidden=True)
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT * FROM Tickets WHERE guild_id= {ctx.guild.id} AND channel_id= {ctx.channel.id}")
                    result = await cursor.fetchone()
            if result == None:
                return
            user = ctx.guild.get_member(int(result[2]))

            rollen = ""
            for u in user.roles:
                rollen += f"{u.mention}"
            if user in ctx.guild.premium_subscribers:
                booster = f"<t:{int(float(user.premium_since.timestamp()))}> [<t:{int(float(user.premium_since.timestamp()))}:R>]"
            else:
                booster = "`None`"
            if user.activities:
                Activity = ""
                for activity in user.activities:
                    if activity.type == discord.ActivityType.custom:
                        Activity += f"**Custom:** {user.activity}\n"
                    if activity.type == discord.ActivityType.playing:
                        Activity += f"**Play:** {activity.name}\n"
                    if activity.type == discord.ActivityType.streaming:
                        Activity += f"**Stream:** [{activity.name} | {activity.twitch_name}]({activity.url})\n"
                    if activity.type == discord.ActivityType.listening:
                        url = f'https://open.spotify.com/track/{activity.track_id}'
                        Activity += f"**Listen:** [{activity.title} | {activity.artist}]({url})\n"
            else:
                Activity = "None"

            embed = discord.Embed(title=f"__Userinfo - {user}__",
                                  description=f"Hier sind paar Infos über `{user}`",
                                  color=0x00ffff,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)

            embed.add_field(name=f"Name:", value=f"<:user:928211789466963988> `{user.name}`", inline=True)
            embed.add_field(name=f"Nickname:", value=f"<:person:928211829698756669> `{user.nick}`", inline=True)
            embed.add_field(name=f"ID:", value=f"<:idee:928211874548428810> `{user.id}`", inline=True)
            embed.add_field(name=f"Avatar URL:", value=f"[Link]({user.avatar_url})", inline=True)
            embed.add_field(name=f"Status:", value=f":desktop: Desktop: `{user.desktop_status}`\n"
                                                   f":mobile_phone: Mobile: `{user.mobile_status}`\n"
                                                   f":link: Web: `{user.web_status}`", inline=True)
            embed.add_field(inline=False, name="⠀", value="⠀")
            embed.add_field(name=f"Erstellt am:",
                            value=f"<a:timer:927937017625575424> <t:{int(float(user.created_at.timestamp()))}> [<t:{int(float(user.created_at.timestamp()))}:R>]",
                            inline=True)
            embed.add_field(name=f"Gejoint am:",
                            value=f"<:server_owner:928211980634947604> <t:{int(float(user.joined_at.timestamp()))}> [<t:{int(float(user.joined_at.timestamp()))}:R>]",
                            inline=True)
            embed.add_field(inline=False, name="⠀", value="⠀")
            try:
                embed.add_field(name=f"Beschreibung/Spiel:", value=f"{Activity}", inline=True)
            except:
                embed.add_field(name=f"Beschreibung/Spiel:", value=f"None", inline=True)
            embed.add_field(name=f"Booster:", value=f"<:boost:928212105335816213> {booster}", inline=True)
            return await ctx.send(embed=embed, hidden=True)


# ----------------------------------------------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(TicketSystem(bot))
