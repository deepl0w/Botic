from enum import Enum
from random import randint
import subprocess


class Cmd(Enum):
    HELLO    = 'hello'
    HELP     = 'help'
    FLIP     = 'flip'
    BOT_SRC  = 'botsrc'
    SHELL    = 'shell'

class Bot:


    MAX_COMMAND_SIZE = 20

    COMMANDS = [Cmd.HELLO, Cmd.HELP, Cmd.FLIP, Cmd.BOT_SRC, Cmd.SHELL]

    COMMANDS_DESCRIPTION = {
            Cmd.HELLO: 'Responds by saying hello to you.',
            Cmd.FLIP:  'Flips a coin.',
            Cmd.HELP:  'Prints this info message.',
            Cmd.BOT_SRC: 'Prints the source code of the Bot class',
            Cmd.SHELL:   'Run a shell command'
    }

    def __init__(self, client, prefix):
        self.prefix = prefix
        self.client = client

    async def run(self, message):
        content = message.content
        channel = message.channel
        author = message.author

        if author == self.client.user:
            return

        if content[0:1] != self.prefix:
            return

        command = content[1:self.MAX_COMMAND_SIZE].partition(' ')[0]

        if command == Cmd.HELP.value:
            await self.help(channel)
        elif command == Cmd.HELLO.value:
            await self.hello(channel, author)
        elif command == Cmd.FLIP.value:
            await self.flip(channel, author)
        elif command == Cmd.BOT_SRC.value:
            await self.bot_src(channel)
        elif command == Cmd.SHELL.value:
            arg = content[len(command)+1:]
            await self.shell(channel, arg)
        else:
            await self.invalid_command(channel)

    async def hello(self, channel, author):
        msg = 'Hello {0.mention}'.format(author)

        await self.client.send_message(channel, msg)

    async def flip(self, channel, author):
        if author.nick == 'La Araña Discoteca':
            msg = "Muie Miță! :))))))))))))))))))))"
        else:
            if randint(0, 1) == 0:
                msg = "Heads!"
            else:
                msg = "Tails!"

        await self.client.send_message(channel, msg)

    async def shell(self, channel, arg):
        msg = subprocess.check_output(arg, shell=True).decode("utf-8").strip()
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
