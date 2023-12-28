import discord
from discord.ext import commands
import os
import traceback
from dotenv import load_dotenv
from gpt4_summary import generate_summary

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="f!", intents=intents)


def check_perms(ctx):
    return ctx.message.author.id == 363690578950488074 or "mod" in [r.name for r in ctx.message.author.roles]


# CheckFailure
@bot.event
async def on_command_error(ctx, error):
    print("".join(traceback.format_exception(type(error), error, error.__traceback__)))
    await ctx.channel.send(error.args[0])


@bot.command(brief="Use the GPT-4 api to summarize the last 150 messages in a channel",
             help="Use the GPT-4 api to summarize the last 150 messages in a channel, ping .saph."
                  "or something if you need to summarize more.",
             aliases=['s', 'sum'])
@commands.check(check_perms)
async def summarize(ctx, channel_id):
    channel = await ctx.guild.fetch_channel(channel_id)
    messages = []

    async for message in channel.history(limit=150):
        if message.reference is not None:
            replied_message = await channel.fetch_message(message.reference.message_id)
            messages.append(f"{message.author.display_name}: {message.content} (replying to: {replied_message.content})")
        else:
            messages.append(f"{message.author.display_name}: {message.content}")

    messages = "Thread Name - " + channel.name + "\n" + "\n".join(messages[1:][::-1])
    summary = generate_summary(messages)
    with open("summary.txt", "w") as file:
        file.write(summary)

    with open("summary.txt", "rb") as file:
        await ctx.send("DISCLAIMER: The following summary is generated using AI "
                       "and may not be completely accurate.", file=discord.File(file, filename="summary.txt"))


bot.run(TOKEN)
