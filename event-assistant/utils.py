#===============================================================================
# Helper functions/utilities
#===============================================================================

# 
# Helper function for informing of invalid type
#
# ctx: discord context object
# type: type as a string
#
async def sendInvalidType(ctx, type):
    await ctx.send(f"{ctx.author.mention} invalid type '{type}'. try 'food' or 'hangout'")