import discord
import logging
import os
import random
import utils
from discord.ext import commands
from dotenv import load_dotenv
from collections import defaultdict
from enum import Enum
from datetime import datetime

#
# The different categories of items being stored. Used to differentiate
# what is stored in different data structures
#
class Category(Enum):
    FOOD = 1
    HANGOUT = 2

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
DEFAULT_HISTORY_LENGTH = 5     # Default Length of history to display
FOOD = "food"                  # the food string

# Suggestions for each category
all_suggestions = defaultdict(set)

# Reverse chronological history of completed suggestions for given category
all_completed = defaultdict(list)

# # Map suggestion to user. This will be a dictionary of dictionary:
# # {user : {food: [], hangout: {}}}
# self_wants = defaultdict(lambda: defaultdict(list))

#
# Return true and the set of suggestion for for everyone for the given category
# if the category exists in a list: [True, set()]. Return false
# and an empty set if the category does not exist: [False, set()]
#
# cat: the category to get the set for
#
def getSuggestion(cat:str):
    if cat == "food":
        return [True, all_suggestions[Category.FOOD]]
    elif cat == "hangout":
        return [True, all_suggestions[Category.HANGOUT]]
    return [False, set()]

#
# Return true and the list of completed of suggestion if the category exists 
# in a list: [True, []]. Return false and an empty list if the category does 
# not exist: [False, []]
#
# cat: the category to get the set for
#
def getCompleted(cat:str):
    if cat == "food":
        return [True, all_completed[Category.FOOD]]
    elif cat == "hangout":
        return [True, all_completed[Category.HANGOUT]]
    return [False, []]

#
# Add a suggestion for everyone
#
# name: name of the item
# cat: the category
#
@bot.command()
async def suggest(ctx, name:str, cat:str = FOOD):
    success, suggestion = getSuggestion(cat)
    
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    suggestion.add(name)
    await ctx.send(f"{ctx.author.mention} suggested {name} for {cat}!")

#
# Remove a suggestion if it exists
#
# name: name of the suggestion
# cat: the category
#
@bot.command()
async def remove(ctx, name:str, cat:str = FOOD):
    success, suggestion = getSuggestion(cat)
    
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    if name in suggestion:
        suggestion.remove(name)
        
    await ctx.send(f"{ctx.author.mention} removed {name}!")

#
# Remove all suggestions for a category
#
# cat: the category
#
@bot.command()
async def clear(ctx, cat:str = FOOD):
    success, suggestion = getSuggestion(cat)
        
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    suggestion.clear()
    await ctx.send(f"{ctx.author.mention} cleared {cat} category!")

#
# Pick a random suggestion for a category
#
# cat: the category
#
@bot.command()
async def pickForMe(ctx, cat:str = FOOD):
    success, suggestion = getSuggestion(cat)
        
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    pick_from = list(suggestion)
    rand_pick = pick_from[random.randint(0, len(pick_from) - 1)]
    await ctx.send(f"{ctx.author.mention} and squad shall hit up {rand_pick}")

#
# Mark a suggestion as completed
#
# name: name of suggestion
# cat: the category
#
@bot.command()
async def completed(ctx, name:str, cat:str = FOOD):
    success, completed = getCompleted(cat)
    success, suggestion = getSuggestion(cat)
        
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    if name not in suggestion:
        await ctx.send(f"{ctx.author.mention} '{name}' has not yet been suggested. suggest it first before doing it :^)")
        return
    
    today = datetime.now().strftime("%B %d, %Y")
    name_today = name + " - " + today
    completed.insert(0, name_today)
    suggestion.remove(name)
    await ctx.send(f"{ctx.author.mention} and the squad accomplished {name} on {today}!")

#
# Print a history of completed suggestions for the given category
#
# hist_length: the length of history
# cat: the category
#
@bot.command()
async def history(ctx, hist_length:int = DEFAULT_HISTORY_LENGTH, cat:str = FOOD):
    success, completed = getCompleted(cat)
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    completed_str = ""
    for i in range(hist_length):
        if i >= len(completed):
            break
        completed_str += completed[i] + "\n"
    
    await ctx.send(f"So far, {ctx.author.mention} and the squad has completed:\n{completed_str}")

#
# Print current list of suggestions for the given category
#
# cat: the category
#
@bot.command()
async def currentSuggestions(ctx, cat:str = FOOD):
    success, suggestion = getSuggestion(cat)
    if not success:
        await utils.sendInvalidType(ctx, cat)
        return
        
    suggested_str = ""
    for s in suggestion:
        suggested_str += s + "\n"
    
    await ctx.send(f"{ctx.author.mention} the suggested {cat} so far is:\n{suggested_str}")

# TODO: implement in future
# Give x random suggestions to create as a poll
@bot.command()
async def randomPoll(ctx):
    return

# Create a poll with the following options
@bot.command()
async def poll(ctx):
    return

# Add an event
@bot.command()
async def suggestForSelf(ctx, type:str, name:str):
    return

# Remove my suggestion
@bot.command()
async def removeSuggestionForSelf(ctx):
    return

# Remove my clear my suggestion
@bot.command()
async def clearSuggestionForSelf(ctx):
    return

bot.run(token=DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)