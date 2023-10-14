# cogs / ao3.py
import traceback

import aiohttp
import discord
from discord import Embed
from discord.ext import commands

from utils.fic_scrape import main
import utils.checks
from typing import Any

from utils import pagination

from utils.const_hell import *

A03_View_Fields = [(MAIN,"https://cdn.discordapp.com/attachments/1039953198842122382/1154545431607521380/tMKOZTh.png"),
                   (INTRO,"https://cdn.discordapp.com/attachments/1039953198842122382/1155239778615312394/cCUk0kC.png"),
                   (SORTING,"https://cdn.discordapp.com/attachments/1039953198842122382/1154545431234224219/WI1J2fp.png"),
                   (RATINGS,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174778060157018/n4CtcHS.png"),
                   (WARNINGS,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174778328600617/ZpgUlKz.png"),
                   (CATEGORIES,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174778546700359/6zt0Myl.png"),
                   (FANDOMS,"https://cdn.discordapp.com/attachments/1039953198842122382/1155249529914925127/UfnMKmd.png"),
                   (CHARACTERS_AND_RELATIONSHIPS,"https://cdn.discordapp.com/attachments/1039953198842122382/1155249529118007316/prP882Z.png"),
                   (ADDITIONAL,"https://cdn.discordapp.com/attachments/1039953198842122382/1155249529684230225/ayBQG9n.png"),
                   (OTHER,"https://cdn.discordapp.com/attachments/1039953198842122382/1155337464282615888/LmQmSlO.png"),
                   (CROSSOVER,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174778735439913/rDijWD0.png"),
                   (COMPLETION,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174778961940591/ViMkLtY.png"),
                   (WORD_COUNT,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174779217789119/zqAYSCq.png"),
                   (UPDATED,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174779448471572/K8lFC5w.png"),
                   (SEARCH,"https://cdn.discordapp.com/attachments/1039953198842122382/1155249529352892416/jXDXRRS.png"),
                   (LANGUAGE,"https://cdn.discordapp.com/attachments/1039953198842122382/1155334347629527090/vgEMnQh.png"),
                   (ANY_FIELD,"https://cdn.discordapp.com/attachments/1039953198842122382/1155174779674972280/1gR2HBo.png")
                   ]


class A03_Guide_View(pagination.PaginatedSelectView[tuple[str,str]]):
    def __init__(self, me: discord.User | discord.Member, author_id: int, pages_content: list[tuple[str,str]], *, timeout: float | None = 180) -> None:
        super().__init__(author_id,pages_content,timeout=timeout)
        self.me = me
    def populate_select(self) -> None:
        self.select_page.placeholder = "Choose guide section here"
        for i, page in enumerate(self.pages):
            self.select_page.add_option(label=page[0].partition("\n")[0].replace("# ",""), value=str(i))
    def format_page(self) -> Embed:
        embed_var = Embed(title="An Incomplete AO3 Filtering Guide", colour=0xa80000)
        embed_var.set_footer(text=f"Page {self.page_index + 1}/{self.total_pages}")
        embed_var.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/8/88/Archive_of_Our_Own_logo.png")
        # print(self.me)
        try:
            embed_var.set_author(name=self.me.display_name, icon_url=self.me.display_avatar)
        except Exception:
            embed_var.set_author(name=self.me.name, icon_url=self.me.avatar)
        embed_var.description = self.pages[self.page_index][0]
        embed_var.set_image(url=self.pages[self.page_index][1])
        return embed_var

class AO3(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)
        if ctx.guild.id == 1039953198359781446:
            error = getattr(error, "original", error)
            await ctx.send(embed=Embed(title=f"{type(error).__name__}", description=f"{error}", colour=0xC70039))

    @commands.hybrid_command()
    async def ao3_filtering_explanation(self, ctx):
        """Explains AO3 Filtering"""
        # if ctx.guild.id not in [801834790768082944,1029951199958540372] :
        me = ctx.guild.get_member(self.client.owner_id)
        if me is None:
            me = self.client.get_user(self.client.owner_id)
        view = A03_Guide_View(me, ctx.author.id, A03_View_Fields)
        view.message = await ctx.reply(embed=await view.get_first_page(), view=view)
        # else:
        #     await ctx.reply("Command disabled on this server, apologies for any inconvenience caused")

    @utils.checks.in_test_guild()
    @commands.hybrid_command()
    async def plspls(self, ctx, fic: str):
        if len(fic.split(".")) != 2:
            await ctx.reply(embed=Embed(description="Link does not work, please try again"), ephemeral=True)

        elif "archiveofourown.org" in fic.split("/")[2].lower():
            await ctx.reply("Grabbing Meta", ephemeral=True)
            meta = await main(fic, self.client.web_client)
            if "/works/" in fic.lower():

                if len(meta) == 2:
                    fic = fic + "?view_adult=true"
                if len(meta) == 3:
                    fic = str(fic).split("?")[0] + "?view_adult=true&"
                if 'Private' in meta[fic].keys():
                    if meta[fic]['Private'] == "yes":
                        await ctx.reply(embed=Embed(
                            description="This story is private\nThis command does not work on private stories"))

                sum_var = ""
                if 'Summary' in meta[fic].keys() and meta[fic]["sum length"] >= 1024:
                    sum_var = f"\n\n**Summary:**\n{meta[fic]['Summary']}"

                authors = meta[fic]['authors']
                author_list = []
                for author in authors.values():
                    author_list.append(
                        f"[{author['author_name']}](https://archiveofourown.org{author['author_link']})")

                embed_var = Embed(
                    description=f"**by {', '.join(author_list)}**{sum_var}",
                    title=f"{meta[fic]['title']}",
                    url=fic,
                    colour=0xa80000
                )

                embed_var.set_thumbnail(
                    url="https://upload.wikimedia.org/wikipedia/commons/8/88/Archive_of_Our_Own_logo.png")
                embed_var.add_field(name="Rating:", value=", ".join(meta[fic]['rating']), inline=True)
                embed_var.add_field(name="Categories:", value=", ".join(meta[fic]['category']), inline=True)
                embed_var.add_field(name="Warnings:", value=", ".join(meta[fic]['warning']), inline=False)
                embed_var.add_field(name="Fandoms:", value=", ".join(meta[fic]['fandom']), inline=False)
                embed_var.add_field(name="Characters:", value=f"{', '.join(meta[fic]['character'][:4])}, ...",
                                    inline=False)
                embed_var.add_field(name="Relationships:", value=f"{', '.join(meta[fic]['relationship'][:4])}, ...",
                                    inline=False)
                embed_var.add_field(name="Additional Tags:", value=f"{', '.join(meta[fic]['freeform'][:4])}, ...",
                                    inline=False)
                if 'Summary' in meta[fic].keys() and 0 < meta[fic]["sum length"] < 1024:
                    embed_var.add_field(name="Summary:", value=f"{meta[fic]['Summary']}", inline=False)
                embed_var.add_field(name="Published Date:", value=meta[fic]['published'], inline=True)
                if 'completed' in meta[fic].keys():
                    embed_var.add_field(name="Date Completed:", value=meta[fic]['completed'], inline=True)
                if 'updated' in meta[fic].keys():
                    embed_var.add_field(name="Date Updated:", value=meta[fic]['updated'], inline=True)
                embed_var.add_field(name="Words", value=meta[fic]['words'], inline=True)
                embed_var.add_field(name="Chapters", value=meta[fic]['chapters'], inline=True)
                if "?" in meta[fic]['chapters']: # ToDo add functionality for x/y incomplete fics
                    embed_var.add_field(name="Complete:", value="No", inline=True)
                else:
                    embed_var.add_field(name="Complete:", value="Yes", inline=True)
            elif "/series/" in fic.lower():
                await ctx.reply("is a series", ephemeral=True)
                authors = meta[fic]['authors']
                author_list = []
                # [print(author) for author in authors.values()]
                for author in authors.values():
                    author_list.append(
                        f"[{author['author_name']}](https://archiveofourown.org{author['author_link']})")

                # print(author_list)
                if 'series summary' in meta[fic].keys():
                    des = f"**by {', '.join(author_list)}\n\n**Summary**\n{meta[fic]['series summary']}**"
                else:
                    des = f"**by {', '.join(author_list)}**"

                embed_var = Embed(
                    description=des,
                    title=f"{meta[fic]['series title']}",
                    url=fic,
                    colour=0xa80000
                )
                embed_var.set_thumbnail(
                    url="https://upload.wikimedia.org/wikipedia/commons/8/88/Archive_of_Our_Own_logo.png")
                embed_var.add_field(name="Published Date", value=meta[fic]['series begun'], inline=True)
                if 'series updated' in meta[fic].keys():
                    embed_var.add_field(name="Date Updated", value=meta[fic]['series updated'], inline=True)
                embed_var.add_field(name="Words", value=meta[fic]['words'], inline=True)
                embed_var.add_field(name="Works", value=meta[fic]['works'], inline=True)
                embed_var.add_field(name="Completed", value=meta[fic]['complete'])
            elif "/works/" not in fic.lower() or "/series/" not in fic.lower():
                embed_var = Embed(description="3 Link does not work, please try again")
            await ctx.channel.send(embed=embed_var)
            print(embed_var.__len__())
        else:  # "arc" not in fic.split("/")[2].lower():
            await ctx.reply(embed=Embed(description="2 Link does not work, please try again"), ephemeral=True)


async def setup(client):
    await client.add_cog(AO3(client))
