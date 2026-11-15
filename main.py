import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATA_FILE = Path(os.getenv("POINTS_FILE", "points.json"))

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set. Add it to your .env file.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def load_scores() -> dict[str, int]:
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            raw_scores = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not read {DATA_FILE}: {error}") from error

    if not isinstance(raw_scores, dict):
        raise RuntimeError(f"The contents of {DATA_FILE} must be a JSON object.")

    scores: dict[str, int] = {}
    for user_id, score in raw_scores.items():
        if isinstance(user_id, str) and isinstance(score, int) and not isinstance(score, bool):
            scores[user_id] = score
    return scores


def save_scores(scores: dict[str, int]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    directory = DATA_FILE.parent
    with NamedTemporaryFile("w", encoding="utf-8", dir=directory, delete=False) as temporary:
        json.dump(scores, temporary, indent=2, sort_keys=True)
        temporary.write("\n")
        temporary_path = Path(temporary.name)
    temporary_path.replace(DATA_FILE)


scores = load_scores()


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.command(name="points")
async def points_command(ctx: commands.Context[commands.Bot]) -> None:
    score = scores.get(str(ctx.author.id), 0)
    await ctx.send(f"{ctx.author.mention} has {score} point(s).")


@bot.command(name="give-points")
async def give_points_command(ctx: commands.Context[commands.Bot], amount: int) -> None:
    if amount <= 0:
        await ctx.send("The amount must be a positive whole number.")
        return

    user_id = str(ctx.author.id)
    scores[user_id] = scores.get(user_id, 0) + amount
    save_scores(scores)
    await ctx.send(f"Added {amount} point(s). {ctx.author.mention} now has {scores[user_id]} point(s).")


@bot.command(name="remove-points")
async def remove_points_command(ctx: commands.Context[commands.Bot], amount: int) -> None:
    if amount <= 0:
        await ctx.send("The amount must be a positive whole number.")
        return

    user_id = str(ctx.author.id)
    scores[user_id] = max(0, scores.get(user_id, 0) - amount)
    save_scores(scores)
    await ctx.send(f"Removed {amount} point(s). {ctx.author.mention} now has {scores[user_id]} point(s).")


@bot.event
async def on_command_error(ctx: commands.Context[commands.Bot], error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `!give-points <amount>` or `!remove-points <amount>`.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("The amount must be a whole number. Example: `!give-points 10`.")
        return
    raise error


bot.run(TOKEN)
