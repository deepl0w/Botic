import discord
from queue import Queue
from threading import Thread
from subprocess import STDOUT
import pafy
import os
import utils
import asyncio
import urllib.request
import urllib.parse
import re

class Player:
    CACHE_PATH = ".cache"
    CACHE_MAX_SIZE = 1024 * 1024 * 1024 * 2

    def __init__(self, client, server):
        self.server = server
        self.client = client
        self.player = None
        self.play_queue = Queue()
        self.download_queue = Queue()
        self.downloading = False
        self.current_video = None

    async def add(self, channel, voice_channel, query):
        if self.download_queue.qsize() == 0:
            Thread(target = self._dw_func, args = (channel,)).start()

        self.download_queue.put_nowait(query)

        if self.client.is_voice_connected(self.server):
            voice = self.client.voice_client_in(self.server)
        else:
            voice = await self.client.join_voice_channel(voice_channel)

            await self._next_song(channel, voice)

    async def skip(self):
        self.player.stop()

        await utils.send_message(self.client, channel,
                "Skipping `" + self.current_video.title + "`.")

    def _dw_func(self, channel):
        self.downloading = True

        if not os.path.exists(self.CACHE_PATH):
            os.makedirs(self.CACHE_PATH)

        while True:
            url = self.download_queue.get()
            if url == None:
                self.downloading = False
                break

            # convert to youtube search if it's not a link
            if not (url.startswith("http://") or url.startswith("https://")):
                query = urllib.parse.urlencode({"search_query" : url})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" +
                        query)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})',
                        html_content.read().decode())
                url = search_results[0]

                video = pafy.new(url)
                best = video.audiostreams[1]

                asyncio.run_coroutine_threadsafe(utils.send_message(self.client, channel,
                        "Added `" + video.title + "` to queue."), self.client.loop)

                path = self.CACHE_PATH + "/" + url + "." + best.extension

                if not os.path.exists(path):
                    best.download(filepath = path)
                self.play_queue.put_nowait((path, video))


    async def _next_song(self, channel, voice):
        while self.downloading and self.play_queue.qsize() == 0:
            pass

        if not self.play_queue.empty():
            filename, video = self.play_queue.get()

            try:
                self.player = voice.create_ffmpeg_player(filename,
                        after = lambda : asyncio.run_coroutine_threadsafe(
                            self._next_song(channel, voice), self.client.loop))
                self.player.start()

                self.current_video = video
                await utils.send_message(self.client, channel,
                        "Now playing `" + video.title + "`.")
            except discord.ClientException as ce:
                print(ce)
                await utils.send_message(self.client, channel, "Can't play the song.")
        else:
            await voice.disconnect()

            await utils.send_message(self.client, channel, "Queue completed.")


