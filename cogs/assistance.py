# cogs / help.py
from collections.abc import Mapping

import discord
from discord import app_commands
from discord.ext import commands

from typing import Any

from discord.ext.commands import Group


class HelpCogDropdownWrapper(discord.ui.View):
    def __init__(
            self,
            author: discord.User | discord.Member,
            clean_prefix: str,
            invoked_with: str,
            mapping: Mapping[commands.Cog | None, list[commands.Command[Any, ..., Any]]],
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.author = author
        self.clean_prefix = clean_prefix
        self.invoked_with = invoked_with
        self.mapping = mapping

        # Populate the select options.
        self.cog_dropdown.add_option(
            label="Help Index", value="Help Index", description="How to Navigate the Help Menu.", emoji="🔰",
            default=True
        )
        for cog, cmds in mapping.items():
            qualified_name = getattr(cog, "qualified_name", "No Category")
            description = getattr(cog, "description", "...")[:100]
            if len(description) == 100:
                description = description[:97] + "..."
            emoji = getattr(cog, "cog_emoji", None)
            self.cog_dropdown.add_option(label=qualified_name, value=qualified_name, description=description,
                                         emoji=emoji)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.id not in (self.author.id, interaction.client.owner_id):
            return False
        return True

    def format_page(self, choice: str) -> discord.Embed:
        """Makes the help embed 'page' that the user will see."""

        if choice != "Help Index":
            cog_choice = next(
                (cog, cog_commands) for cog, cog_commands in self.mapping.items()
                if getattr(cog, "qualified_name", "No Category") == choice
            )

            embed_page = discord.Embed(
                color=0x16a75d,
                title=f"Help - {getattr(cog_choice[0], 'qualified_name', 'No Category')}",
                description=getattr(cog_choice[0], "description", "..."),
                colour=0xa80000
            )
            for command in cog_choice[1]:
                embed_page.add_field(name=f"{self.clean_prefix}{command.name}", value=f"{command.help}", inline=False)
        else:
            embed_page = discord.Embed(
                colour=0xa80000,
                title=f"Help Index",
                description=(
                    "Use the dropdown below to navigate between different cogs.\n\n"
                    f"To be more specific, use `{self.clean_prefix}{self.invoked_with} [command]` for more info on a command.\n"
                    f"You can also use `{self.clean_prefix}{self.invoked_with} [category]` for more info on a category."
                )
            )
        return embed_page

    @discord.ui.select(placeholder="Choose the command category here...", min_values=1, max_values=1)
    async def cog_dropdown(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]
        result_embed = self.format_page(choice)
        await interaction.response.edit_message(embed=result_embed, view=self)  # type: ignore


class MyHelpCommand(commands.MinimalHelpCommand, discord.ui.Select):
    """Custom help class"""

    def __init__(self, **options: Any) -> None:
        super().__init__(**options)

    async def send_bot_help(self, mapping: Mapping[commands.Cog | None, list[commands.Command[Any, ..., Any]]],
                            /) -> None:
        view = HelpCogDropdownWrapper(self.context.author, self.context.clean_prefix, self.invoked_with, mapping)
        channel = self.get_destination()
        first_embed = view.format_page("Help Index")
        await channel.send(embed=first_embed, view=view)

    # async def send_bot_help(self, mapping):
    #     """Main help command"""
    #     embed = discord.Embed(title="Help", colour=0xa80000)
    #     options = []
    #     for cog, commands in mapping.items():
    #        command_signatures = [self.get_command_signature(c) for c in commands]
    #        if command_signatures:
    #             cog_name = getattr(cog, "qualified_name", "No Category")
    #             options.append(discord.SelectOption(label=cog_name, description=f"{', '.join(command_signatures)}"))
    #             embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
    #     [print(c) for c in options]
    #     channel = self.get_destination()
    #     await channel.send(embed=embed)

    async def send_command_help(self, command):
        """command specific help"""
        embed = discord.Embed(title=self.get_command_signature(command), colour=0xa80000)
        embed.add_field(name="Help", value=command.short_doc)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        """cog specific help"""
        embed = discord.Embed(title=f"{cog.qualified_name}", colour=0xa80000)
        commands = cog.get_commands()
        for command in commands:
            embed.add_field(name=f"{self.context.clean_prefix}{command.name}", value=f"{command.short_doc}",
                            inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group: Group[Any, ..., Any], /) -> None:
        """group specific help"""
        embed = discord.Embed(title=f"{group.qualified_name}", colour=0xa80000)
        embed.add_field(name="Help", value=group.short_doc)
        alias = group.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        for command in group.commands:
            embed.add_field(name=f"{self.context.clean_prefix}{command.name}", value=f"{command.short_doc}",
                            inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

class Assistance(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand()
        client.help_command.cog = self

    @app_commands.command()
    async def help(self, interaction: discord.Interaction, command: str | None = None) -> None:
        """Access the help commands through the slash system."""
        # Create the view containing our dropdown

        ctx = await self.client.get_context(interaction, cls=commands.Context)
        # view = DropdownView(ctx.author)
        # await ctx.reply('Select the command', view=view, ephemeral=True)

        # Sending a message containing our view
        # await ctx.reply('Pick your favourite colour:', view=view, ephemeral=True)

        if command is not None:
            # if command is commands.Cog:
            print(command)
            await ctx.send_help(command)
        else:
            await ctx.send_help()

        await interaction.response.send_message(content="Help dialogue sent!", ephemeral=True)  # type: ignore

    def cog_unload(self):
        self.client.help_command = self._original_help_command

    @help.autocomplete("command")
    async def command_autocomplete(self, interaction: discord.Interaction, current: str) -> list[
        app_commands.Choice[str]]:
        """Autocompletes the help command."""

        assert self.client.help_command
        ctx = await self.client.get_context(interaction, cls=commands.Context)
        help_command = self.client.help_command.copy()
        help_command.context = ctx

        if not current:
            return [
                       app_commands.Choice(name=cog_name, value=cog_name)
                       for cog_name, cog in self.client.cogs.items()
                       if await help_command.filter_commands(cog.get_commands())
                   ][:25]

        current = current.lower()
        return [
                   app_commands.Choice(name=command.qualified_name, value=command.qualified_name)
                   for command in await help_command.filter_commands(self.client.walk_commands(), sort=True)
                   if current in command.qualified_name
               ][:25]


async def setup(client):
    await client.add_cog(Assistance(client))
