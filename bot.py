from enum import Enum
from random import randint
import os
import subprocess
from subprocess import STDOUT


class Cmd(Enum):
    HELLO    = 'hello'
    HELP     = 'help'
    FLIP     = 'flip'
    BOT_SRC  = 'botsrc'
    # SHELL    = 'shell'
    PLAY     = 'play'

class Bot:


    MAX_COMMAND_SIZE = 20

    COMMANDS = [Cmd.HELLO, Cmd.HELP, Cmd.FLIP, Cmd.BOT_SRC, Cmd.PLAY]

    COMMANDS_DESCRIPTION = {
            Cmd.HELLO: 'Responds by saying hello to you.',
            Cmd.FLIP:  'Flips a coin.',
            Cmd.HELP:  'Prints this info message.',
            Cmd.BOT_SRC: 'Prints the source code of the Bot class',
            Cmd.PLAY : 'Play music from youtube',
            # Cmd.SHELL:   'Run a shell command'
    }

    def __init__(self, client, prefix):
        self.prefix = prefix
        self.client = client

    def log(self, message):
        server  = message.server.name
        channel = message.channel.name
        content = message.content
        author = message.author.name

        path = server
        if not os.path.exists(path):
            os.makedirs(path)

        path += "/" + channel + "_log.txt"
        with open(path, 'a+', encoding = 'utf-8') as f:
            f.write(author + ": " + content + "\n")

    async def run(self, message):
        content = message.content
        channel = message.channel
        author = message.author

        if author == self.client.user:
            return

        self.log(message)

        if content[0:1] != self.prefix:
            return

        args = content[1:self.MAX_COMMAND_SIZE].partition(' ')
        command = args[0]

        if command == Cmd.HELP.value:
            await self.help(channel)
        elif command == Cmd.HELLO.value:
            await self.hello(channel, author)
        elif command == Cmd.FLIP.value:
            await self.flip(channel, author)
        elif command == Cmd.BOT_SRC.value:
            await self.bot_src(channel)
        elif command == Cmd.PLAY.value:
            voice_channel = author.voice.voice_channel
            if len(args) > 1:
                await self.play(channel, voice_channel, arg[1])
        elif command == Cmd.SHELL.value:
            if len(args) > 1:
                await self.shell(channel, " ".join(args[1:]))
        else:
            await self.invalid_command(channel)

    async def hello(self, channel, author):
        msg = 'Hello {0.mention}'.format(author)

        await self.client.send_message(channel, msg)

    async def flip(self, channel, author):
        if author.name == 'mihaid':
            msg = "Muie Miță! :))))))))))))))))))))"
        else:
            if randint(0, 1) == 0:
                msg = "Heads!"
            else:
                msg = "Tails!"

        await self.client.send_message(channel, voice_channel, arg)

    async def play(self, channel, voice_channel, arg):
        if not voice_channel:
            await self.client.send_message(channel, "`You must be in a voie channel!`")

        voice = await self.client.join_voice_channel(voice_channel)
        palyer = await voice.create_ytdl_player(arg)

        player.start()

    async def shell(self, channel, arg):
        try:
            msg = subprocess.check_output(arg + " &", stderr = STDOUT, shell=True, timeout = 2).decode("utf-8").strip()
        except subprocess.CalledProcessError as exc:
            msg = exc.output.decode("utf-8").strip()
        except subprocess.TimeoutExpired as exc:
            msg = "Timeout!"

        msg = "```\n" + msg + "```"
        await self.client.send_message(channel, msg)

    async def bot_src(self, channel):
        start_ticks = "```python\n"
        end_ticks = "```"

        msg = open('bot.py', encoding="utf-8").read().strip().replace('`', '`\u200b')

        if len(msg) > 1990:
            lines = msg.split('\n')
            msg1 = start_ticks + "\n".join(lines[:len(lines)//2]) + end_ticks
            msg2 = start_ticks + "\n".join(lines[len(lines)//2:]) + end_ticks

            await self.client.send_message(channel, msg1)
            await self.client.send_message(channel, msg2)
        else:
            await self.client.send_message(channel, msg)

    async def help(self, channel):
        msg = "```\n"
        for c in self.COMMANDS:
            msg += "{}{} - {}\n".format(self.prefix, c.value,
                                        self.COMMANDS_DESCRIPTION[c])
        msg += "```"

        await self.client.send_message(channel, msg)

    async def invalid_command(self, channel):
        msg = "Invalid command! Use `" + self.prefix + "help` for more info."
        await self.client.send_message(channel, msg)

    def ready(self):
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')
