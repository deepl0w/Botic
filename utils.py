async def send_message(client, channel, msg, code_block=False, language=""):
    lines = msg.split('\n')

    new_msg = ""
    for l in lines:
        if len(new_msg) + len(l) + len(language) + 1 > 1990:
            final_msg = "```" + language +"\n" if code_block else ""
            final_msg += new_msg
            final_msg += "```" if code_block else ""

            await client.send_message(channel, final_msg)

            new_msg = ""

        new_msg += l + "\n"

    final_msg = "```" + language + "\n" if code_block else ""
    final_msg += new_msg
    final_msg += "```" if code_block else ""

    await client.send_message(channel, final_msg)

