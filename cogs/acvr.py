"""
story_search.py: This cog is meant to provide functionality for searching the text of some books.
"""

from __future__ import annotations

import asyncio
import logging
import math
import re
from bisect import bisect_left
from copy import deepcopy
from pathlib import Path
from random import randint
from typing import ClassVar, Any

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING
from typing_extensions import Self


LOGGER = logging.getLogger(__name__)
EMOJI_URL = "https://cdn.discordapp.com/emojis/{0}.webp?size=128&quality=lossless"
PANIC_GUILD_ID = 801834790768082944


class PaginatedEmbed(discord.Embed):
    """A subclass of :class:`Embed` customized to create an embed 'page'.

    Parameters
    ----------
    page_content : :class:`tuple`, optional
        The content of an embed page.
    current_page : :class:`int`, optional
        The number of the current page.
    max_pages : :class:`int`, optional
        The total number of pages possible.
    story_data : dict, optional
        The information about the story to be put in the author field, including the story title, author, and link.
    **kwargs
        Keyword arguments for the normal initialization of an :class:`Embed`.
    """

    def __init__(
            self,
            *,
            page_content: tuple | None = MISSING,
            current_page: int | None = MISSING,
            max_pages: int | None = MISSING,
            story_data: dict | None = MISSING,
            **kwargs
    ) -> None:

        super().__init__(**kwargs)

        if page_content is not MISSING:
            self.set_page_content(page_content)

        if (current_page is not MISSING) and (max_pages is not MISSING):
            self.set_page_footer(current_page, max_pages)

        if story_data is not MISSING:
            self.set_page_author(story_data)

    def set_page_content(self, page_content: tuple | None = None) -> Self:
        """Sets the content field for this embed page.

        This function returns the class instance to allow for fluent-style chaining.

        Parameters
        ----------
        page_content : tuple
            A tuple with 3 elements (unless overriden) that contains the content for this embed page.
        """

        if page_content is None:
            self.title = "Nothing found"
            if self.fields:
                self.remove_field(0)

        else:
            self.title = str(page_content[0])
            chapter_name, quote = str(page_content[1]), str(page_content[2])
            self.add_field(name=chapter_name, value=quote)

        return self

    def set_page_footer(self, current_page: int | None = None, max_pages: int | None = None) -> Self:
        """Sets the footer for this embed page.

        This function returns the class instance to allow for fluent-style chaining.

        Parameters
        ----------
        current_page : :class:`int`
            The number of the current page.
        max_pages : :class:`int`
            The total number of pages possible.
        """

        if current_page is None:
            current_page = 0
        if max_pages is None:
            max_pages = 0

        self.set_footer(text=f"Page {current_page}/{max_pages}")

        return self

    def set_page_author(self, story_data: dict | None = None) -> Self:
        """Sets the author for this embed page.

        This function returns the class instance to allow for fluent-style chaining.
        """

        if story_data is None:
            self.remove_author()
        else:
            emoji_url = f"https://cdn.discordapp.com/emojis/{story_data['emoji_id']}.webp?size=128&quality=lossless"
            self.set_author(name=story_data["story_full_name"], url=story_data["story_link"], icon_url=emoji_url)

        return self


class PageNumEntryModal(discord.ui.Modal):
    """A discord modal that allows users to enter a page number to jump to in the view that references this.

    Parameters
    ----------
    page_limit : :class:`int`
        The maximum integer value of pages that can be entered.

    Attributes
    ----------
    input_page_num : :class:`TextInput`
        A UI text input element to allow users to enter a page number.
    interaction : :class:`discord.Interaction`
        The interaction of the user with the modal.
    page_limit : :class:`int`
        The maximum integer value of pages that can be entered.
    """

    input_page_num = discord.ui.TextInput(label="Page", placeholder="Enter page number here...", required=True, min_length=1)

    def __init__(self, page_limit: int) -> None:
        super().__init__(title="Page Jump", custom_id="page_entry_modal")
        self.interaction = None
        self.page_limit = page_limit

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        """Performs validation on the input and saves the interaction for a later response."""

        temp = int(self.input_page_num.value)
        if temp > self.page_limit or temp < 1:
            raise IndexError
        self.interaction = interaction

    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:
        if not isinstance(error, (ValueError, IndexError)):
            LOGGER.exception("Unknown Modal error.", exc_info=error)


class PaginatedEmbedView(discord.ui.View):
    """A view that handles paginated embeds and page buttons.

    Parameters
    ----------
    author : :class:`discord.User | :class:`discord.Member`
        The user that triggered this view. No one else can use it.
    all_pages_content : list[Any]
        The text content for every possible page.
    per_page : :class:`int`
        The number of entries to be displayed per page.
    story_data : dict
        The story's data and metadata, including full name, author name, and image representation.

    Attributes
    ----------
    message : :class:`discord.Message`
        The message to which the view is attached to, allowing interaction without a :class:`discord.Interaction`.
    author : :class:`discord.User | :class:`discord.Member`
        The user that triggered this view. No one else can use it.
    story_data : dict
        The story's data and metadata, including full name, author name, and image representation.
    per_page : :class:`int`
        The number of entries to be displayed per page.
    total_pages : :class:`int`
        The total number of pages.
    pages : list[Any | None]
        A list of content for pages, split according to how much content is wanted per page.
    page_cache : list[Any | None]
        A cache of pages for if they are visited again.
    current_page : :class:`int`
        The number for the current page.
    former_page : :class:`int`
        The number for the page just before the current one.
    current_page_content: tuple
        The content on the current page.
    """

    def __init__(self, *, author: discord.User | discord.Member, all_pages_content: list[Any], per_page: int = 1, story_data: dict) -> None:
        super().__init__()
        self.message = None
        self.author = author
        self.story_data = story_data

        # Page-related instance variables.
        self.per_page = per_page
        self.total_pages = math.ceil(len(all_pages_content) / per_page)
        self.pages = [all_pages_content[i: (i + per_page)] for i in range(0, len(all_pages_content), per_page)]
        self.page_cache: list[Any] = [None for _ in self.pages]

        self.current_page, self.former_page = 1, 1
        self.current_page_content = ()

        # Have the right buttons activated on instantiation.
        self.clear_items()
        self._set_page_buttons()
        self.update_page_buttons()

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        """Ensures that the user interacting with the view was the one who instantiated it."""

        check = (interaction.user is not None) and (self.author == interaction.user)
        if not check:
            await interaction.response.send_message("You cannot interact with this view.", ephemeral=True, delete_after=30)     # type: ignore  # PyCharm doesn't understand descriptors.
        return check

    async def on_timeout(self) -> None:
        """Disables all buttons when the view times out."""

        self.clear_items()
        if self.message:
            await self.message.edit(view=self)

        self.stop()

    def format_page(self) -> discord.Embed:
        """Makes, or retrieves from the cache, the quote embed 'page' that the user will see.

        Assumes a per_page value of 1.
        """

        embed_page = PaginatedEmbed(story_data=self.story_data, color=0x149cdf)

        if self.total_pages == 0:
            embed_page.set_page_content(("No quotes found!", "N/A", "N/A")).set_page_footer(0, 0)

        else:
            if self.page_cache[self.current_page - 1] is None:
                self.current_page_content = self.pages[self.current_page - 1][0]    # per_page value of 1 means parsing a list of length 1.
                embed_page.set_page_content(self.current_page_content).set_page_footer(self.current_page, self.total_pages)
                self.page_cache[self.current_page - 1] = embed_page

            else:
                return deepcopy(self.page_cache[self.current_page - 1])

        return embed_page

    def _set_page_buttons(self) -> None:
        """Only adds the necessary page buttons based on how many pages there are."""

        if self.total_pages > 2:
            self.add_item(self.turn_to_first)
        if self.total_pages > 1:
            self.add_item(self.turn_to_previous)
        if self.total_pages > 2:
            self.add_item(self.enter_page)
        if self.total_pages > 1:
            self.add_item(self.turn_to_next)
        if self.total_pages > 2:
            self.add_item(self.turn_to_last)

        self.add_item(self.quit_view)

    def update_page_buttons(self) -> None:
        """Enables and disables page-turning buttons based on page count, position, and movement."""

        # Disable buttons based on the total number of pages.
        if self.total_pages <= 1:
            for button in (self.turn_to_first, self.turn_to_next, self.turn_to_previous, self.turn_to_last, self.enter_page):
                button.disabled = True
            return
        else:
            self.enter_page.disabled = False

        # Disable buttons based on the page extremes.
        if self.current_page == 1:
            self.turn_to_previous.disabled = self.turn_to_first.disabled = True
        elif self.current_page == self.total_pages:
            self.turn_to_next.disabled = self.turn_to_last.disabled = True

        # Enable buttons based on movement relative to the page extremes.
        if self.former_page == 1 and self.current_page != 1:
            self.turn_to_previous.disabled = self.turn_to_first.disabled = False
        elif self.former_page == self.total_pages and self.current_page != self.total_pages:
            self.turn_to_next.disabled = self.turn_to_last.disabled = False

    def get_starting_embed(self) -> discord.Embed:
        """Get the embed of the first page."""

        self.former_page, self.current_page = 1, 1
        embed_page = self.format_page()
        return embed_page

    async def update_page(self, interaction: discord.Interaction, new_page: int) -> None:
        """Update and display the view for the given page."""

        self.former_page = self.current_page                                    # Update the page number.
        self.current_page = new_page
        embed_page = self.format_page()                                         # Update the page embed.
        self.update_page_buttons()                                              # Update the page buttons.
        await interaction.response.edit_message(embed=embed_page, view=self)    # type: ignore

    @discord.ui.button(label="≪", style=discord.ButtonStyle.blurple, disabled=True, custom_id="page_view:first")
    async def turn_to_first(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Skips to the first page of the view."""

        await self.update_page(interaction, 1)

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, disabled=True, custom_id="page_view:prev")
    async def turn_to_previous(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Turns to the previous page of the view."""

        await self.update_page(interaction, self.current_page - 1)

    @discord.ui.button(label="🕮", style=discord.ButtonStyle.green, disabled=True, custom_id="page_view:enter")
    async def enter_page(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Sends a modal that a user to enter their own page number into."""

        # Get page number from a modal.
        modal = PageNumEntryModal(self.total_pages)
        await interaction.response.send_modal(modal)    # type: ignore
        modal_timed_out = await modal.wait()

        if modal_timed_out or self.is_finished():
            return

        temp_new_page = int(modal.input_page_num.value)

        if self.current_page == temp_new_page:
            return

        await self.update_page(modal.interaction, temp_new_page)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="page_view:next")
    async def turn_to_next(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Turns to the next page of the view."""

        await self.update_page(interaction, self.current_page + 1)

    @discord.ui.button(label="≫", style=discord.ButtonStyle.blurple, custom_id="page_view:last")
    async def turn_to_last(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Skips to the last page of the view."""

        await self.update_page(interaction, self.total_pages)

    @discord.ui.button(label="✕", style=discord.ButtonStyle.red, custom_id="page_view:quit")
    async def quit_view(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Deletes the original message with the view after a slight delay."""

        await interaction.response.defer()  # type: ignore
        await asyncio.sleep(0.5)
        await interaction.delete_original_response()
        self.stop()


def is_in_panic(ctx: commands.Context):
    """A check to determine if this command was invoked in the Panic server."""

    if not ctx.guild:
        return False
    return ctx.guild.id == PANIC_GUILD_ID


class AVCRSearchCog(commands.Cog, name="ACVR Quote Search"):
    """A cog with commands for people to search the text of one or more M J Bradley works while in Discord.

    Parameters
    ----------
    bot : :class:`commands.Bot`
        The main Discord bot this cog is a part of.

    Attributes
    ----------
    bot : :class:`commands.Bot`
        The main Discord bot this cog is a part of.
    story_records : dict
        The dictionary holding the metadata and text for all stories being scanned.
    """

    story_records: ClassVar[dict] = {}

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        """Load whatever is necessary to avoid reading from files or querying a database during runtime."""
        # await self.bot.tree.sync(guild=discord.Object(id=801834790768082944))
        self.story_records.update({
            "acvr": {
                "story_acronym": "acvr",
                "story_full_name": "A Cadmean Victory",
                "author_name": "M J Bradley",
                "story_link": "https://www.fanfiction.net/s/13720575/",
                "emoji_id": 1021875940067905566,
                "text": [],
                "chapter_index": [],
                "collection_index": []
            }
        })

        # TODO: Change filepath for Ali's system.
        # Load story text from local markdown file(s).
        project_path = Path(__file__).resolve().parents[1]
        for file in project_path.glob("acvr_text.md"):
            if "text" in file.name:
                await self.load_story_text(file)

    @classmethod
    async def load_story_text(cls, filepath: Path):
        """Load the story metadata and text."""

        # Compile all necessary regex patterns for ACVR text.
        # More patterns would need to be added for other stories, depending on their formatting.
        re_acvr_chap_title = re.compile(r"(^# \w+)")
        re_volume_heading = re.compile(r"(^A Cadmean Victory Volume \w+)")

        # Start file copying and indexing.
        with filepath.open("r", encoding="utf-8") as f:

            # Instantiate index lists, which act as a table of contents of sorts.
            stem = str(filepath.stem)[:-5]
            temp_text = cls.story_records[stem]["text"] = [line for line in f if line.strip() != ""]
            temp_chap_index = cls.story_records[stem]["chapter_index"]
            temp_coll_index = cls.story_records[stem]["collection_index"]

            # Create a "table of contents"-esque index for the story.
            for index, line in enumerate(temp_text):

                # Prologue: A Quest for Europa is split among two lines and needs special parsing logic.
                if re.search(re_acvr_chap_title, line):
                    if "*A Quest for Europa*" in line:
                        temp_chap_index[0] += " A Quest for Europa"
                    else:
                        temp_chap_index.append(index)

                elif re.search(re_volume_heading, line):
                    # Add to the index if it's empty or if the newest possible entry is unique.
                    if (len(temp_coll_index) == 0) or (line != temp_text[temp_coll_index[-1]]):
                        temp_coll_index.append(index)
            
        LOGGER.info(f"Loaded file: {filepath.stem}")

    @classmethod
    def process_text(cls, story: str, terms: str, exact: bool = True) -> list[tuple]:
        """Collects all lines from story text that contain the given terms."""

        all_text = cls.story_records[story]["text"]
        results = []

        # Iterate through all text in the story.
        for index, line in enumerate(all_text):

            # Determine if searching based on exact words/phrases, or keywords.
            if exact:
                terms_presence = terms.lower() in line.lower()
            else:
                terms_presence = any([term.lower() in line.lower() for term in terms.split()])

            if terms_presence:
                # Connect the paragraph with the terms to the one following it.
                quote = "\n".join(all_text[index:index + 3])

                # Underline the terms.
                quote = re.sub(f'( |^)({terms})', r'\1__\2__', quote, flags=re.I)

                # Fit the paragraphs in the space of a Discord embed field.
                if len(quote) > 1024:
                    quote = quote[0:1020] + "..."

                # Get the "collection" and "chapter" text lines using binary search.
                quote_collection = cls._binary_search_text(story, cls.story_records[story]["collection_index"], index)
                quote_chapter = cls._binary_search_text(story, cls.story_records[story]["chapter_index"], index)

                # Take special care for ACVR.
                if story == "acvr":
                    acvr_title_with_space = "A Cadmean Victory "
                    quote_collection = quote_collection[len(acvr_title_with_space):]
                    quote_chapter = quote_chapter[2:]

                # Aggregate the quotes.
                results.append((quote_collection, quote_chapter, quote))

        return results

    @classmethod
    def _binary_search_text(cls, story: str, list_of_indices: list[int], index: int) -> str:
        """Finds the element in a list of elements closest to but less than the given element."""

        if len(list_of_indices) == 0:
            return "—————"

        # Get the element from the given list that's closest to and less than the given index value.
        i_of_index = bisect_left(list_of_indices, index)
        actual_index = list_of_indices[max(i_of_index - 1, 0)] if (i_of_index is not None) else -1

        # Use that element as an index in the story text list to get a quote, whether it's a chapter, volume, etc.
        value_from_index = cls.story_records[story]["text"][actual_index] if actual_index != -1 else "—————"

        return value_from_index

    @commands.hybrid_command()
    @commands.check(is_in_panic)                # To limit the prefix command version.
    @app_commands.guilds(PANIC_GUILD_ID)        # To limit the app command version. Requires manual sync with guild via .sync(guild=...).
    async def random_cadmean(self, ctx: commands.Context) -> None:
        """Display a random line from *A Cadmean Victory Remastered* by M J Bradley.

        Parameters
        ----------
        ctx : :class:`commands.Context`
            The invocation context where the command was called.
        """

        async with ctx.typing():
            # Randomly choose an M J Bradley story.
            story = "acvr"

            # Randomly choose two paragraphs from the story.
            rand_range = randint(2, len(self.story_records[story]["text"]) - 3)
            rand_sample = self.story_records[story]["text"][rand_range: (rand_range + 2)]

            # Get the chapter and collection of the quote.
            quote_year = self._binary_search_text(story, self.story_records[story]["collection_index"], (rand_range + 2))
            quote_chapter = self._binary_search_text(story, self.story_records[story]["chapter_index"], (rand_range + 2))

            # Bundle the quote in an embed.
            embed = PaginatedEmbed(
                color=0xdb05db,
                page_content=(quote_year, quote_chapter, "".join(rand_sample)),
                story_data=self.story_records[story]
            ).set_footer(text="Randomly chosen quote from *A Cadmean Victory Remastered* by M J Bradley.")

            await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.check(is_in_panic)                # To limit the prefix command version.
    @app_commands.guilds(PANIC_GUILD_ID)        # To limit the app command version. Requires manual sync with guild via .sync(guild=...).
    async def search_cadmean(self, ctx: commands.Context, *, query: str) -> None:
        """Search *A Cadmean Victory Remastered* by M J Bradley for a word or phrase.

        Parameters
        ----------
        ctx : :class:`commands.Context`
            The invocation context.
        query : :class:`str`
            The string to search for in the story.
        """

        async with ctx.typing():
            processed_text = self.process_text("acvr", query)
            story_data = self.story_records["acvr"]
            view = PaginatedEmbedView(author=ctx.author, all_pages_content=processed_text, story_data=story_data)
            message = await ctx.send(embed=view.get_starting_embed(), view=view)
            view.message = message


async def setup(bot: commands.Bot) -> None:
    """Connects cog to bot."""

    await bot.add_cog(AVCRSearchCog(bot))
