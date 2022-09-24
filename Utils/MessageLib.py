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


def custom_embed(is_blue: bool, key: str, *args: str) -> Embed:
    """
    :param is_blue: colour of embed, True - blue; False - red
    :param key: str, key in json lang-data
    :param args: Any, params to create format-string, where it used
    :return: Embed
    """
    if is_blue:
        col = Colour.dark_blue()
    else:
        col = Colour.red()
    embed = Embed(
        title="BRLover",
        description=message_texts[key] % args,
        colour=col
    )

    return embed
