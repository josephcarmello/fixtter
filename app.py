import discord
import re

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

## regex for twitter/x links
twitter_pattern = re.compile(r"https?://(?:www\.)?twitter\.com/([a-zA-Z0-9_]+)(/status/\d+)?")
x_pattern = re.compile(r"https?://(?:www\.)?x\.com/([a-zA-Z0-9_]+)(/status/\d+)?")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    modified_content = twitter_pattern.sub(r"https://vxtwitter.com/\1\2", message.content)
    modified_content = x_pattern.sub(r"https://vxtwitter.com/\1\2", modified_content)

    if modified_content != message.content:
        if message.reference:
            ## If the message is a reply, get OG message that was replied to
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            ## Send a reply to the OG message
            await replied_message.reply(f'{message.author.mention} posted: {modified_content}')
        else:
            ## If the message is not a reply, just send as usual
            await message.channel.send(f'{message.author.mention} posted: {modified_content}')

        await message.delete()

client.run('YOUR_DISCORD_TOKEN_HERE')
