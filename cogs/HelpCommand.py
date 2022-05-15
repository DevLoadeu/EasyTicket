import datetime
from discord.ext import commands
import discord
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, create_select, create_select_option, wait_for_component
from discord_slash.model import ButtonStyle


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="help", description="Zeigt Hilfe über den Bot an")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _help(self, ctx: SlashContext):
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

        embed = discord.Embed(title=f"__Help Menü__",
                              description=f"Hey! Vielen Dank, dass du dir die Funktionen vom Bot anschauen möchtest 😄.\n"
                                          f"Falls du Fragen zu irgendwelchen Funktionen hast, kannst du dich gerne auf dem **[Support Server](https://discord.gg/Mzm8kK4a4q)** melden!\n\r"
                                          f"> **Support Panel**\n"
                                          f"<:bluearrow:927967329298571334> /panel create [channel] [thema]\n"
                                          f"<:bluearrow:927967329298571334> /panel delete [channel] [thema]\n"
                                          f"<:bluearrow:927967329298571334> /panel show\n\r"
                                          f"> **Team Rolle**\n"
                                          f"<:bluearrow:927967329298571334> /team set [role]\n"
                                          f"<:bluearrow:927967329298571334> /team remove\n"
                                          f"<:bluearrow:927967329298571334> /team show\n\r"
                                          f"> **Ticket Kategorie**\n"
                                          f"<:bluearrow:927967329298571334> /kategorie set [kategorie]\n"
                                          f"<:bluearrow:927967329298571334> /kategorie remove\n"
                                          f"<:bluearrow:927967329298571334> /kategorie show\n\r"
                                          f"> **Log Channel**\n"
                                          f"<:bluearrow:927967329298571334> /log-channel set [channel]\n"
                                          f"<:bluearrow:927967329298571334> /log-channel remove\n"
                                          f"<:bluearrow:927967329298571334> /log-channel show\n\r"
                                          f"> **Sonstige Commands**\n"
                                          f"<:bluearrow:927967329298571334> /help\n"
                                          f"<:bluearrow:927967329298571334> /info\n"
                                          f"<:bluearrow:927967329298571334> /invite",
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)
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


# ----------------------------------------------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(HelpCommand(bot))
