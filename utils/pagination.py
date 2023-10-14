"""
pagination.py: A collection of views that together create a view that uses embeds, is paginated, and allows
easy navigation.
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeAlias, TypeVar

import discord
from discord.utils import maybe_coroutine


if TYPE_CHECKING:
    from typing_extensions import Self
else:
    Self: TypeAlias = Any

_LT = TypeVar("_LT")


__all__ = ("OwnedView", "PageSeekModal", "PaginatedEmbedView", "PaginatedSelectView")

LOGGER = logging.getLogger(__name__)


class QuitButton(discord.ui.Button[discord.ui.View]):
    """A button subclass that deletes original message it's attached to after a short delay.

    Default label is an X symbol, and default style is red.
    """

    def __init__(**kwargs: Any):
        kwargs["style"] = kwargs.get("style", discord.ButtonStyle.red)
        kwargs["label"] = kwargs.get("label", "\N{MULTIPLICATION X}")
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None

        await interaction.response.defer()
        await asyncio.sleep(0.25)
        await interaction.delete_original_response()
        self.view.stop()


class OwnedView(discord.ui.View):
    """A view that is owned by the user who triggered its creation. Only they can use it.

    Parameters
    ----------
    author : :class:`int`
        The Discord ID of the user that triggered this view. No one else can use it.
    timeout: :class:`float` | None, optional
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    """

    def __init__(self, author_id: int, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        """Allows to the interaction to be processed if the user interacting is the view owner."""

        check = self.author_id == interaction.user.id
        if not check:
            await interaction.response.send_message("You cannot interact with this view.", ephemeral=True)
        return check


class PageSeekModal(discord.ui.Modal, title="Page Jump"):
    """A discord modal that allows users to enter a page number to jump to in the view that references this.

    Attributes
    ----------
    input_page_num : :class:`TextInput`
        A UI text input element to allow users to enter a page number.
    parent : :class:`PaginatedEmbedView`
        The paginated view that this modal was called from.
    interaction : :class:`discord.Interaction`
        The interaction of the user with the modal. Only populates on submission.
    """

    input_page_num: discord.ui.TextInput[Self] = discord.ui.TextInput(
        label="Page",
        placeholder="Enter page number here...",
        required=True,
    )

    def __init__(self, *, parent: PaginatedEmbedView[Any], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.parent = parent
        self.interaction: discord.Interaction | None = None

    def modify_text_input(self, label: str | None, placeholder: str | None = None) -> Self:
        if label is not None:
            self.input_page_num.label = label
        if placeholder is not None:
            self.input_page_num.placeholder = placeholder
        return self

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        """Saves the interaction for a later response."""

        self.interaction = interaction
        self.stop()


class PaginatedEmbedView(ABC, Generic[_LT], OwnedView):
    """A view that handles paginated embeds and page buttons.

    Parameters
    ----------
    author_id : :class:`int`
        The Discord ID of the user that triggered this view. No one else can use it.
    pages_content : list[Any]
        The content for every possible page.
    per : :class:`int`
        The number of entries to be displayed per page.
    timeout: :class:`float`, optional
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.

    Attributes
    ----------
    message : :class:`discord.Message`
        The message to which the view is attached to, allowing interaction without a :class:`discord.Interaction`.
    per_page : :class:`int`
        The number of entries to be displayed per page.
    pages : list[Any]
        A list of content for pages, split according to how much content is wanted per page.
    page_index : :class:`int`
        The index for the current page.
    page_modal_strings : tuple[:class:`str`, ...], default=()
        Tuple of strings to modify the page seek modal with if necessary. Empty by default.
    total_pages
    """

    message: discord.Message

    def __init__(self, author_id: int, pages_content: list[_LT], per: int = 1, *, timeout: float | None = 180) -> None:
        super().__init__(author_id, timeout=timeout)
        self.per_page = per
        self.pages = [pages_content[i : (i + per)] for i in range(0, len(pages_content), per)]
        self.page_index: int = 0
        self.page_modal_strings: tuple[str, ...] = ()

        # Activate the right buttons on instantiation.
        self.clear_items().add_page_buttons().add_item(QuitButton())
        self.disable_page_buttons()

    @property
    def total_pages(self) -> int:
        """:class:``int`: The total number of pages."""

        return len(self.pages)

    async def on_timeout(self) -> None:
        """Deletes all buttons when the view times out."""

        self.clear_items()
        await self.message.edit(view=self)
        self.stop()

    @abstractmethod
    def format_page(self) -> Any:
        """|maybecoro|

        Makes, or retrieves from the cache, the embed 'page' that the user will see.

        Must be implemented in a subclass.
        """

        msg = "Page formatting must be set up in a subclass."
        raise NotImplementedError(msg)

    def add_page_buttons(self) -> Self:
        """Only adds the necessary page buttons based on how many pages there are.

        This function returns the class instance to allow for fluent-style chaining.
        """

        if self.total_pages > 2:
            (
                self.add_item(self.turn_to_first)
                .add_item(self.turn_to_previous)
                .add_item(self.enter_page)
                .add_item(self.turn_to_next)
                .add_item(self.turn_to_last)
            )
        elif self.total_pages > 1:
            self.add_item(self.turn_to_previous).add_item(self.turn_to_next)

        return self

    def disable_page_buttons(self) -> None:
        """Enables and disables page-turning buttons based on page count, position, and movement."""

        if self.total_pages <= 1:
            self.turn_to_next.disabled = self.turn_to_last.disabled = True
            self.turn_to_previous.disabled = self.turn_to_first.disabled = True
            self.enter_page.disabled = True
        else:
            self.turn_to_previous.disabled = self.turn_to_first.disabled = self.page_index == 0
            self.turn_to_next.disabled = self.turn_to_last.disabled = self.page_index == self.total_pages - 1
            self.enter_page.disabled = False

    async def get_first_page(self) -> discord.Embed:
        """Get the embed of the first page."""

        temp = self.page_index
        self.page_index = 0
        embed = await maybe_coroutine(self.format_page)
        self.page_index = temp
        return embed

    async def update_page(self, interaction: discord.Interaction) -> None:
        """Update and display the view for the given page."""

        embed_page = await maybe_coroutine(self.format_page)
        self.disable_page_buttons()
        await interaction.response.edit_message(embed=embed_page, view=self)

    def validate_page_entry(self, value: str) -> int | None:
        """Validate that input from a modal would result in a valid page."""

        try:
            temp = int(value)
        except ValueError:
            return None
        if temp > self.total_pages or temp < 1 or self.page_index == (temp - 1):
            return None
        return temp

    @discord.ui.button(label="\N{MUCH LESS-THAN}", style=discord.ButtonStyle.blurple)
    async def turn_to_first(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Skips to the first page of the view."""

        self.page_index = 0
        await self.update_page(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def turn_to_previous(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Turns to the previous page of the view."""

        self.page_index -= 1
        await self.update_page(interaction)

    @discord.ui.button(label="\N{BOOK}", style=discord.ButtonStyle.green)
    async def enter_page(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Sends a modal that a user to enter their own page number into."""

        # Get page number from a modal.
        modal = PageSeekModal(parent=self).modify_text_input(*self.page_modal_strings)
        await interaction.response.send_modal(modal)
        modal_timed_out = await modal.wait()

        if modal_timed_out or self.is_finished():
            return

        assert modal.interaction is not None  # The modal had to be submitted to reach this point.

        if (actual_value := self.validate_page_entry(modal.input_page_num.value)) is None:
            return

        self.page_index = actual_value - 1
        await self.update_page(modal.interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def turn_to_next(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Turns to the next page of the view."""

        self.page_index += 1
        await self.update_page(interaction)

    @discord.ui.button(label="\N{MUCH GREATER-THAN}", style=discord.ButtonStyle.blurple)
    async def turn_to_last(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Skips to the last page of the view."""

        self.page_index = self.total_pages - 1
        await self.update_page(interaction)


class PaginatedSelectView(ABC, Generic[_LT], OwnedView):
    """A view that handles paginated embeds and page buttons.

    Parameters
    ----------
    author_id : :class:`int`
        The Discord ID of the user that triggered this view. No one else can use it.
    pages_content : list[Any]
        The content for every possible page.
    timeout: :class:`float` | None, optional
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.

    Attributes
    ----------
    message : :class:`discord.Message`
        The message to which the view is attached to, allowing interaction without a :class:`discord.Interaction`.
    pages : list[Any]
        A list of content for pages.
    page_index : :class:`int`
        The index for the current page.
    total_pages
    """

    message: discord.Message

    def __init__(self, author_id: int, pages_content: list[_LT], *, timeout: float | None = 180) -> None:
        super().__init__(author_id, timeout=timeout)
        self.pages = pages_content
        self.page_index: int = 0

        self.populate_select()

        # Activate the right buttons on instantiation.
        self.clear_items().add_page_buttons()
        self.disable_page_buttons()

    @property
    def total_pages(self) -> int:
        """:class:``int`: The total number of pages."""

        return len(self.pages)

    async def on_timeout(self) -> None:
        """Deletes all buttons when the view times out."""

        self.clear_items()
        await self.message.edit(view=self)
        self.stop()

    @abstractmethod
    def format_page(self) -> Any:
        """|maybecoro|

        Makes the embed 'page' that the user will see.
        """

        msg = "Page formatting must be set up in a subclass."
        raise NotImplementedError(msg)

    @abstractmethod
    def populate_select(self) -> None:
        """Populates the select with relevant options."""

        msg = "Select populating must be set up in a subclass."
        raise NotImplementedError(msg)

    def add_page_buttons(self) -> Self:
        """Only adds the necessary page buttons based on how many pages there are.

        This function returns the class instance to allow for fluent-style chaining.
        """
        self.add_item(self.select_page)

        # Done in a weird way to preserve button order.
        if self.total_pages > 1:
            self.add_item(self.turn_to_previous).add_item(self.turn_to_next)

        return self

    def disable_page_buttons(self) -> None:
        """Enables and disables page-turning buttons based on page count, position, and movement."""

        self.turn_to_previous.disabled = self.page_index == 0
        self.turn_to_next.disabled = self.page_index == self.total_pages - 1

    async def get_first_page(self) -> discord.Embed:
        """Get the embed of the first page."""

        temp = self.page_index
        self.page_index = 0
        embed = await maybe_coroutine(self.format_page)
        self.page_index = temp
        return embed

    async def update_page(self, interaction: discord.Interaction) -> None:
        """Update and display the view for the given page."""

        embed_page = await maybe_coroutine(self.format_page)
        self.disable_page_buttons()
        await interaction.response.edit_message(embed=embed_page, view=self)

    @discord.ui.select()
    async def select_page(self, interaction: discord.Interaction, select: discord.ui.Select[Any]) -> None:
        """Dropdown that displays all the Patreon tiers and provides them as choices to navigate to."""

        self.page_index = int(select.values[0])
        await self.update_page(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def turn_to_previous(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Turns to the previous page of the view."""

        self.page_index -= 1
        await self.update_page(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def turn_to_next(self, interaction: discord.Interaction, _: discord.ui.Button[Self]) -> None:
        """Turns to the next page of the view."""

        self.page_index += 1
        await self.update_page(interaction)
