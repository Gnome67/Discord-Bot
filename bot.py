# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all() 

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.command(name='ping')
async def on_message(ctx):
    response = 'pong'
    await ctx.send(response)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command()
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been given a role called: {role.name}")

@bot.command()
async def newrole(ctx, *, rolename=None):
    if not rolename:
        await ctx.send("You forgot to provide a name!")
    else:
        role = await ctx.guild.create_role(name=rolename, mentionable=True)
        await ctx.author.add_roles(role)
        await ctx.send(f"Successfully created and assigned {role.name}!")

# @bot.event
# async def on_raw_reaction_add(payload):
#     guild = bot.get_guild(payload.guild_id) # Get guild
#     member = get(guild.members, id=payload.user_id) # Get the member out of the guild
#     # The channel ID should be an integer:
#     if payload.channel_id == 1056649462245756998: # Only channel where it will work
#         if str(payload.emoji) == "💀": # Your emoji
#             role = get(payload.member.guild.roles, id=1111783365293658193) # Role ID
#         else:
#             role = get(guild.roles, name=payload.emoji)
#         if role is not None: # If role exists
#             await payload.member.add_roles(role)
#             print(f"Added {role}")

@bot.command()
async def roles(ctx):
    reaction   = await ctx.reply("Select your Anime" + '\n' + '\n' + "- Demon Slayer :japanese_ogre: " '\n' + "- One Piece :pirate_flag: " + '\n' + "- Naruto :skull: " + '\n' + "- Dragon Ball :fire: ")
    await reaction.add_reaction('👹')
    await reaction.add_reaction('🏴‍☠️')
    await reaction.add_reaction('💀')
    await reaction.add_reaction('🔥')

# @bot.event
# async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
#   ChID = 1056649462245756998
#   if payload.channel_id != ChID:
#     return
#   if str(payload.emoji) == "👹":
#     demonslayer = discord.utils.get(payload.member.guild.roles, name="test 1")
#     await payload.member.add_roles(demonslayer)
#   if str(payload.emoji) == "🏴‍☠️":
#     onepiece = discord.utils.get(payload.member.guild.roles, name="test 2")
#     await payload.member.add_roles(onepiece)
#   if str(payload.emoji) == "💀":
#     naruto = discord.utils.get(payload.member.guild.roles, name="test 3")
#     await payload.member.add_roles(naruto)
#   if str(payload.emoji) == "🔥":
#     dragonball = discord.utils.get(payload.member.guild.roles, name="test 4")
#     await payload.member.add_roles(dragonball)

# async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
#     ChID = 1056649462245756998
#     if payload.channel_id != ChID:
#        return
#     if str(payload.emoji) == "👹":
#         demonslayer = discord.utils.get(payload.member.guild.roles, name="test 1")
#         await payload.member.remove_roles(demonslayer)
#         print("test 1 removed")
#     if str(payload.emoji) == "🏴‍☠️":
#         onepiece = discord.utils.get(payload.member.guild.roles, name="test 2")
#         await payload.member.remove_roles(onepiece)
#         print("test 2 removed")
#     if str(payload.emoji) == "💀":
#         naruto = discord.utils.get(payload.member.guild.roles, name="test 3")
#         await payload.member.remove_roles(naruto)
#         print("test 3 removed")
#     if str(payload.emoji) == "🔥":
#         dragonball = discord.utils.get(payload.member.guild.roles, name="test 4")
#         await payload.member.remove_roles(dragonball)
#         print("test 4 removed")

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role_message_id = 0  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 0,  # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='🟡'): 0,  # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='green', id=0): 0,  # ID of the role associated with a partial emoji's ID.
        }

async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    """Gives a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != self.role_message_id:
        return

    guild = self.get_guild(payload.guild_id)
    if guild is None:
        # Check if we're still in the guild and it's cached.
         return
    try:
        role_id = self.emoji_to_role[payload.emoji]
    except KeyError:
        # If the emoji isn't the one we care about then exit as well.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    try:
        # Finally, add the role.
        await payload.member.add_roles(role)
    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        pass

async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
    """Removes a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != self.role_message_id:
        return

    guild = self.get_guild(payload.guild_id)
    if guild is None:
        # Check if we're still in the guild and it's cached.
        return

    try:
            role_id = self.emoji_to_role[payload.emoji]
    except KeyError:
         # If the emoji isn't the one we care about then exit as well.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    # The payload for `on_raw_reaction_remove` does not provide `.member`
    # so we must get the member ourselves from the payload's `.user_id`.
    member = guild.get_member(payload.user_id)
    if member is None:
        # Make sure the member still exists and is valid.
        return

    try:
        # Finally, remove the role.
        await member.remove_roles(role)
    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        pass

@bot.command()
async def removerole(ctx, user: discord.Member, role:discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'{role.name} has been removed from {user.name} ')

bot.run(TOKEN)