import discord
import asyncio
from datetime import datetime, timedelta
import pytz
from book_config import books  

def run_discord_bot():
    TOKEN = 'add your token here'
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True

    client = discord.Client(intents=intents)

    async def schedule_messages():
        sweden_tz = pytz.timezone('Europe/Stockholm')
        now = datetime.now(sweden_tz)

        for book in books:
            book_time = datetime.strptime(book["date"], '%Y-%m-%d %H:%M')
            book_time = sweden_tz.localize(book_time)

            if now > book_time:
                continue

            delay = (book_time - now).total_seconds()
            await asyncio.sleep(delay)

            title_link = f"{book['title']} - [Read Here]({book['link']})"
            
            for guild in client.guilds:
                christmas_channel = discord.utils.get(guild.text_channels, name="🎄")
                if christmas_channel:
                    await christmas_channel.send(title_link)
                    await christmas_channel.send(file=discord.File(book["image"]))
                    await christmas_channel.send(book["description"])

            now = datetime.now(sweden_tz)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
        for guild in client.guilds:
            christmas_channel = discord.utils.get(guild.text_channels, name="🎄")
            if christmas_channel:
                await christmas_channel.send("Ho, ho, ho, Reading Nook! 🎅 I'm your Festive Librarian for the season. Every frosty Sunday, a heartwarming short story awaits you. Immerse yourself in the festive spirit with each tale! 🎄📖")
        
        client.loop.create_task(schedule_messages())

    client.run(TOKEN)

run_discord_bot()
