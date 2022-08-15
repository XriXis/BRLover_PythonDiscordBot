import asyncio

from discord import message


async def reaction(ctx, state: bool):
    if state:
        await ctx.message.add_reaction('👌')
    else:
        await ctx.message.add_reaction('⛔')


async def delete_garbage(msgs: list[message]) -> None:
    await asyncio.sleep(200.0)
    for msg in msgs:
        try:
            await msg.delete
        except PermissionError:
            pass

# TO DO: a creator of embeds universality for all commands
