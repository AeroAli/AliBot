# This example requires the 'message_content' privileged intent to function.

import asyncio

import discord
import youtube_dl
from discord import FFmpegPCMAudio, PCMVolumeTransformer

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    url_queue = []

    @commands.hybrid_command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.hybrid_command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem - Case sensitive, relative path"""

        source = PCMVolumeTransformer(FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    # @commands.hybrid_command()
    # async def yt(self, ctx, *, url):
    #     """Plays from a url (almost anything youtube_dl supports)"""
    #
    #     async with ctx.typing():
    #         player = await YTDLSource.from_url(url, loop=self.client.loop)
    #         ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
    #
    #     await ctx.send(f'Now playing: {player.title}')

    @commands.hybrid_command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    # @commands.hybrid_command()
    # async def stream_queue(self, ctx):
    #     """Streams from queue"""
    #
    #     queues = self.url_queue
    #     while len(queues) > 0:
    #         for url in queues:
    #             async with ctx.typing():
    #                 player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
    #                 ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
    #                 await ctx.send(f'Now playing: {player.title}')
    #
    # @commands.hybrid_command()
    # async def queue(self, ctx, *, option: str, url: str | None = None):
    #     """a/add = add url, r/remove = remove url, s/show = show queue"""
    #     queues = self.url_queue
    #     if url and (option == "a" or option == "add"):
    #         queues.append(url)
    #         await ctx.send(f"Added song to queue in position {len(queues)}")
    #     elif option == "s" or option == "show":
    #         await ctx.send(f"{[y for y in queues]}")
    #     elif url in queues and (option == "r" or option == "remove"):
    #         queues.remove(url)
    #         await ctx.send("Song Removed")
    #     else:
    #         await ctx.send("Not an option, please try again")


    @commands.hybrid_command()
    async def change_volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.hybrid_command()
    async def get_volume(self, ctx):
        """Gets the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        volume = ctx.voice_client.source.volume
        await ctx.send(f"Changed volume to {volume}%")

    @commands.hybrid_command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel")

    @play.before_invoke
    # @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(client):
    await client.add_cog(Music(client))
