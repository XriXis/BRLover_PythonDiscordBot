import asyncio

from discord import message, Embed, Colour

from Utils.JsonHandler import message_texts


async def reaction(ctx, flag: bool) -> None:
    if flag:
        await ctx.message.add_reaction('👌')
    else:
        await ctx.message.add_reaction('⛔')


async def delete_garbage(msgs: list[message]) -> None:
    await asyncio.sleep(200.0)
    for msg in msgs:
        try:
            await msg.delete
        except PermissionError:
            print("Bot haven't permission to manage message")


def custom_embed(flag: bool, key: str, *args: str) -> Embed:
    """
    :param flag: colour of embed
    :param key: str, key in json land-data
    :param args: Any, params to create format-string, were it used
    :return: Embed
    """
    if flag:
        col = Colour.dark_blue()
    else:
        col = Colour.red()
    embed = Embed(
        title="BRLover",
        description=message_texts[key] % args,
        colour=col
    )

    return embed
