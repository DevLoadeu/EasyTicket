import datetime
from discord.ext import commands
import discord
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option, wait_for_component
from discord_slash.model import ButtonStyle


class SonstigeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="info", description="Siehe Informationen über den Bot an")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _info(self, ctx: SlashContext):
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

        members = 0
        bots = 0
        channel = 0
        roles = 0
        categories = 0
        boosts = 0
        for x in self.bot.guilds:
            boosts += int(x.premium_subscription_count)
            for y in x.members:
                if y.bot:
                    bots += 1
                elif not y.bot:
                    members += 1
            channel += len(x.channels)
            roles += len(x.roles) - 1
            categories += len(x.categories)
        embed = discord.Embed(title=f"__Informations about {self.bot.user.name}__",
                              description=f"**Name:** `{self.bot.user.name}`\n"
                                          f"**Discriminator:** `{self.bot.user.discriminator}`\n"
                                          f"**ID:** `{self.bot.user.id}`\n"
                                          f"**Prefix:** `/ (Slash Commands)`\n"
                                          f"**Server:** `{len(self.bot.guilds)}`\n"
                                          f"**Members:** `{members}`\n"
                                          f"**Bots:** `{bots}`\n"
                                          f"**Categories:** `{categories}`\n"
                                          f"**Channel:** `{channel}`\n"
                                          f"**Roles:** `{roles}`\n"
                                          f"**Boosts:** `{boosts}`\n"
                                          f"**Database:** `MySQL`\n"
                                          f"**Developer:** `ToXy`\n"
                                          f"**Programming language:** `Python`",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, components=[
            create_actionrow(
                create_button(label="Invite", emoji=self.bot.get_emoji(927913230335098901), style=ButtonStyle.URL,
                              url=f"https://discord.com/api/oauth2/authorize?client_id=934817403991363645&permissions=1099801422928&scope=bot%20applications.commands"),
                create_button(label="Support", emoji=self.bot.get_emoji(929797411138854993), style=ButtonStyle.URL,
                              url=f"https://discord.gg/Mzm8kK4a4q"),
                create_button(label="Vote", emoji=self.bot.get_emoji(927914707363455076), style=ButtonStyle.URL,
                              url=f"https://top.gg/bot/{self.bot.user.id}/vote")
            )
        ])

    @cog_ext.cog_slash(name="invite", description=f"Sendet den Invite vom Bot!")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _invite(self, ctx: SlashContext):
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

        embed = discord.Embed(title=f"__System__",
                              description=f"Du möchtest meine Funktionen auch auf deinem Server nutzen?\n"
                                          f"**Dann lade mich noch heute ein!**",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, components=[
            create_actionrow(
                create_button(label="Benötigte Perms", style=ButtonStyle.URL, url=f"https://discord.com/api/oauth2/authorize?client_id=934817403991363645&permissions=1099801422928&scope=bot%20applications.commands"),
                create_button(label="Admin Perms (Empfohlen)", style=ButtonStyle.URL, url=f"https://discord.com/api/oauth2/authorize?client_id=934817403991363645&permissions=8&scope=bot%20applications.commands")
            )
        ])


# ----------------------------------------------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(SonstigeCommands(bot))
