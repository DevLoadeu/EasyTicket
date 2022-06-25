import asyncio
import sqlite3
import time
from _datetime import datetime
from discord_slash import SlashContext, cog_ext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from discord.ext import commands
import discord
import dbl


class TopggVotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = ""
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True, webhook_path="/dblwebhook",
                                   webhook_auth="",
                                   webhook_port=)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        userid = data["user"]
        user = await self.bot.fetch_user(userid)
        server = self.bot.get_guild(927591003764953158)
        channel = server.get_channel(928642416469237800)
        role = server.get_role(937748061009109104)
        timelol = int(float(time.time()))
        wochenende = data["isWeekend"]
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT lastvote, votecount FROM TopggVotes WHERE user_id= {user.id}")
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute(
                        f"INSERT INTO TopggVotes (user_id, votecount, lastvote, reminder) VALUES(%s,%s,%s,%s)",
                        (user.id, 0, time.time(), "nein"))
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT lastvote, votecount FROM TopggVotes WHERE user_id= {user.id}")
                result = await cursor.fetchone()
                if result == None:
                    return
                await cursor.execute(
                    f"UPDATE TopggVotes SET votecount= {int(result[1]) + 1}, lastvote= {time.time()} WHERE user_id= {user.id}")
        embed = discord.Embed(title=f"__Vote System__",
                              description=f"Der User {user.mention} **|** `{user.name}` hat zum `{int(result[1]) + 1}.` mal für mich gevoted!\n"
                                          f"Vielen Dank, **[hier](https://top.gg/bot/{self.bot.user.id})** kannst du für mich in <t:{timelol + 43200}:R> erneut voten.",
                              color=0x00ffff,
                              timestamp=datetime.utcnow())
        embed.set_thumbnail(url=user.avatar_url)
        if wochenende == True:
            embed.add_field(name="✨ Wochenende ✨",
                            value=f"Es ist Wochende! Dein Vote zählt doppelt 🎉", inline=False)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url,
                         url=f"https://top.gg/bot/{self.bot.user.id}/vote")
        if user in server.members:
            try:
                member = server.get_member(int(user.id))
                await member.add_roles(role, reason="Topgg Vote")
                embed.set_footer(text=f"Als Dankeschön bekommst du die {role.name} Rolle für 12 Stunden!",
                                 icon_url=server.icon_url)
            except:
                embed.set_footer(text=f"Es gab leider einen Fehler beim hinzufügen der Voter Rolle!",
                                 icon_url=server.icon_url)
        else:
            embed.set_footer(text=f"Der User ist nicht auf diesem Server!",
                             icon_url=server.icon_url)

        embed2 = discord.Embed(title=f"__Vote System__",
                               description=f"Hey,\n"
                                           f"Vielen Dank für dein `{int(result[1]) + 1}.` Vote auf Top.gg!\n"
                                           f"Du kannst **[hier](https://top.gg/bot/{self.bot.user.id}/vote)** für mich in <t:{timelol + 43200}:R> erneut voten.",
                               color=0x00ffff,
                               timestamp=datetime.utcnow())
        embed2.set_thumbnail(url=user.avatar_url)
        embed2.set_footer(text=f"Vielen Dank für deine Unterstützung!", icon_url=self.bot.user.avatar_url)
        buttons = [
            create_actionrow(
                create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076), style=ButtonStyle.URL,
                              url=f"https://top.gg/bot/{self.bot.user.id}/vote"),
                create_button(label="Vote Reminder", emoji=self.bot.get_emoji(927937017625575424), style=ButtonStyle.green,
                              custom_id="vote_reminder_button")
            )
        ]
        await channel.send(embed=embed, components=[create_actionrow(
            create_button(label="Vote", emoji=self.bot.get_emoji(927937017625575424), style=ButtonStyle.URL,
                          url=f"https://top.gg/bot/{self.bot.user.id}/vote")
        )])
        try:
            mess = await user.send(embed=embed2, components=buttons)
        except:
            return

        def check(button_ctx):
            return button_ctx.author == user and button_ctx.channel == user.dm_channel and button_ctx.custom_id == "vote_reminder_button"

        try:
            button_ctx = await wait_for_component(self.bot, components=buttons, timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await mess.edit(components=[
                create_actionrow(
                    create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076),
                                  style=ButtonStyle.URL,
                                  url=f"https://top.gg/bot/{self.bot.user.id}/vote"),
                    create_button(label="Vote Reminder", emoji=self.bot.get_emoji(927937017625575424), style=ButtonStyle.green,
                                  custom_id="vote_reminder_button", disabled=True)
                )
            ])

        if button_ctx.custom_id == "vote_reminder_button":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT * FROM TopggVotes WHERE user_id= {user.id}")
                    result_vote = await cursor.fetchone()
                    if result_vote == None:
                        return await button_ctx.send(f"**ERROR**")
                    await cursor.execute(f"UPDATE TopggVotes SET reminder= 'Ja' WHERE user_id= {user.id}")
                    embed = discord.Embed(title=f"__Vote System__",
                                          description=f"<:yes:927908513114628116> Der Vote Reminder wurde Erfolgreich aktiviert <:yes:927908513114628116>\n"
                                                      f"Ich werde dich in 12 Stunden Informieren.",
                                          color=0x00ffff,
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=self.bot.user.avatar_url)
                    embed.set_footer(text=f"Angefordert von {button_ctx.author}",
                                     icon_url=button_ctx.author.avatar_url)
                    return await button_ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        userid = data["user"]
        user = await self.bot.fetch_user(userid)
        server = self.bot.get_guild(927591003764953158)
        channel = server.get_channel(928642416469237800)
        role = server.get_role(937748061009109104)
        timelol = int(float(time.time()))
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT lastvote, votecount FROM TopggVotes WHERE user_id= {user.id}")
                result = await cursor.fetchone()
                if result == None:
                    await cursor.execute(
                        f"INSERT INTO TopggVotes (user_id, votecount, lastvote, reminder) VALUES(%s,%s,%s,%s)",
                        (user.id, 0, timelol, "nein"))
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT lastvote, votecount FROM TopggVotes WHERE user_id= {user.id}")
                result = await cursor.fetchone()
                if result == None:
                    return
                await cursor.execute(
                    f"UPDATE TopggVotes SET votecount= {int(result[1]) + 1}, lastvote= {timelol} WHERE user_id= {user.id}")
        embed = discord.Embed(title=f"__Vote System__",
                              description=f"Der User {user.mention} **|** `{user.name}` hat zum `{int(result[1]) + 1}.` mal für mich gevoted!\n"
                                          f"Vielen Dank, **[hier](https://top.gg/bot/{self.bot.user.id})** kannst du für mich in <t:{timelol + 43200}:R> erneut voten.",
                              color=0x00ffff,
                              timestamp=datetime.utcnow())
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url,
                         url=f"https://top.gg/bot/{self.bot.user.id}/vote")
        if user in server.members:
            try:
                member = server.get_member(int(user.id))
                await member.add_roles(role, reason="Topgg Vote")
                embed.set_footer(text=f"Als Dankeschön bekommst du die {role.name} Rolle für 12 Stunden!",
                                 icon_url=server.icon_url)
            except:
                embed.set_footer(text=f"Es gab leider einen Fehler beim hinzufügen der Voter Rolle!",
                                 icon_url=server.icon_url)
        else:
            embed.set_footer(text=f"Der User ist nicht auf diesem Server!",
                             icon_url=server.icon_url)

        embed2 = discord.Embed(title=f"__Vote System__",
                               description=f"Hey,\n"
                                           f"Vielen Dank für dein `{int(result[1]) + 1}.` Vote auf Top.gg!\n"
                                           f"Du kannst **[hier](https://top.gg/bot/{self.bot.user.id}/vote)** für mich in <t:{timelol + 43200}:R> erneut voten.",
                               color=0x00ffff,
                               timestamp=datetime.utcnow())
        embed2.set_thumbnail(url=user.avatar_url)
        embed2.set_footer(text=f"Vielen Dank für deine Unterstützung!", icon_url=self.bot.user.avatar_url)
        buttons = [
            create_actionrow(
                create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076), style=ButtonStyle.URL,
                              url=f"https://top.gg/bot/{self.bot.user.id}/vote"),
                create_button(label="Vote Reminder", emoji=self.bot.get_emoji(927937017625575424),
                              style=ButtonStyle.green,
                              custom_id="vote_reminder_button")
            )
        ]
        await channel.send(embed=embed, components=[create_actionrow(
            create_button(label="Vote", emoji=self.bot.get_emoji(927937017625575424), style=ButtonStyle.URL,
                          url=f"https://top.gg/bot/{self.bot.user.id}/vote")
        )])
        try:
            mess = await user.send(embed=embed2, components=buttons)
        except:
            return

        def check(button_ctx):
            return button_ctx.author == user and button_ctx.channel == user.dm_channel and button_ctx.custom_id == "vote_reminder_button"

        try:
            button_ctx = await wait_for_component(self.bot, components=buttons, timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await mess.edit(components=[
                create_actionrow(
                    create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076),
                                  style=ButtonStyle.URL,
                                  url=f"https://top.gg/bot/{self.bot.user.id}/vote"),
                    create_button(label="Vote Reminder", emoji=self.bot.get_emoji(927937017625575424),
                                  style=ButtonStyle.green,
                                  custom_id="vote_reminder_button", disabled=True)
                )
            ])

        if button_ctx.custom_id == "vote_reminder_button":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f"SELECT * FROM TopggVotes WHERE user_id= {user.id}")
                    result_vote = await cursor.fetchone()
                    if result_vote == None:
                        return await button_ctx.send(f"**ERROR**")
                    await cursor.execute(f"UPDATE TopggVotes SET reminder= 'Ja' WHERE user_id= {user.id}")
                    await mess.edit(components=[
                        create_actionrow(
                            create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076),
                                          style=ButtonStyle.URL,
                                          url=f"https://top.gg/bot/{self.bot.user.id}/vote"),
                            create_button(label="Vote Reminder", emoji=self.bot.get_emoji(927937017625575424),
                                          style=ButtonStyle.green,
                                          custom_id="vote_reminder_button", disabled=True)
                        )
                    ])
                    embed = discord.Embed(title=f"__Vote System__",
                                          description=f"<:yes:927908513114628116> Der Vote Reminder wurde Erfolgreich aktiviert <:yes:927908513114628116>\n"
                                                      f"Ich werde dich in 12 Stunden Informieren.",
                                          color=0x00ffff,
                                          timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=self.bot.user.avatar_url)
                    embed.set_footer(text=f"Angefordert von {button_ctx.author}",
                                     icon_url=button_ctx.author.avatar_url)
                    return await button_ctx.reply(embed=embed)


# ----------------------------------------------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(TopggVotes(bot))
