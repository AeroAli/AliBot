"""
db.py: Utility functions for interacting with the database.
"""

from __future__ import annotations

import logging
import traceback

import discord
from aiomysql import cursors

__all__ = ("upsert_users", "upsert_guilds")

LOGGER = logging.getLogger(__name__)

async def upsert_users(cur: cursors.Cursor, *users: discord.User | discord.Member | discord.Object | tuple) -> None:
    """Upsert a Discord user in the appropriate database table.

    Parameters
    ----------
    cur : :Cursor:
    users : tuple[:class:`discord.User` | :class:`discord.Member` | :class:`discord.Object` | tuple]
        One or more users, members, discord objects, or tuples of user ids and blocked statuses, to use for upsertion.
    """
    print("users")
    upsert_query = """
        INSERT INTO users (user_id, is_blocked) 
        VALUES (%s, %s) as new
        ON DUPLICATE KEY UPDATE is_blocked=new.is_blocked
    """
    # Format the users as minimal tuples.

    values = [
        (user.id, False) if isinstance(user, discord.User | discord.Member | discord.Object) else user for user in users
    ]
    try:
        await cur.executemany(upsert_query, values)
        print("user executed")
    except Exception as e1:
        traceback.print_exception(e1)


async def upsert_guilds(cur: cursors.Cursor, *guilds: discord.Guild | discord.Object | tuple) -> None:
    """Upsert a Discord guild in the appropriate database table.

    Parameters
    ----------
    cur : Cursor
        aiomysql connection pool cursor
    guilds : tuple[:class:`discord.Guild` | :class:`discord.Object` | tuple]
        One or more guilds, discord objects, or tuples of guild ids, names, and blocked statuses, to use for upsertion.
    """
    print("guilds")

    # Format the guilds as minimal tuples.
    values = [(guild.id, False) if isinstance(guild, discord.Guild | discord.Object) else guild for guild in guilds]
    print("guild values",values)
    # upsert_query =
    # print("query con")
    try:
        for value in values:
            await cur.execute(f"""
            INSERT INTO guilds (guild_id, is_blocked) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE is_blocked = {value[1]}
        """, value)
        print("guild executed")
    except Exception as e:
        traceback.print_exception(e)
