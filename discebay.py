"""
    Projet : DiscEbay
    Date Creation : 12/05/2024
    Date Revision : 14/05/2024
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Bot discord de type leboncoin ou ebay
"""

import io
import discord
from discord.ext import commands

channelID = int("Channel ID for the bot")
botID = 'YOUR APP TOKEN'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def toSell(ctx, arg):
    """
        Function bot discord to add sell announcement

        Input:
            - ctx: context discord
            - arg: [string] with all information for announcement

    """
    if ctx.channel.id == channelID:
        # Separation of all element for the announcement
        separation = [arg.find("title="), arg.find("price="), arg.find("description=")]

        title = arg[6:separation[1]]
        price = arg[separation[1] + 6:separation[2]]
        description = arg[separation[2] + 12:]

        # Prepare the message in embed
        embed = discord.Embed(title="SELLING", description=f"Created by {ctx.author.mention}", color=0x00ff00)
        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Price", value=price, inline=False)
        embed.add_field(name="Description", value=description, inline=False)

        # Check if photo are send with the message
        if ctx.message.attachments:
            # Send message
            message = await ctx.send(embed=embed)

            imageNumber = len(ctx.message.attachments)

            # Send all photo
            for img in range(imageNumber):
                image_content = await ctx.message.attachments[img].read()

                file = discord.File(io.BytesIO(image_content), filename="image.png")
                await ctx.send(file=file)
        else:
            # Send message without photo
            await ctx.send(embed=embed)

        # Delete initial message
        await ctx.message.delete()


@bot.command()
async def search(ctx, arg):
    """
        Function bot discord to add research announcement

        Input:
            - ctx: context discord
            - arg: [string] with all information for announcement

    """
    if ctx.channel.id == channelID:
        # Separation of all element for the announcement
        separation = [arg.find("title="), arg.find("description=")]

        title = arg[6:separation[1]]
        description = arg[separation[1] + 12:]

        # Prepare the message in embed
        embed = discord.Embed(title="SEARCHING", description=f"Created by {ctx.author.mention}", color=0x00ff00)
        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Description", value=description, inline=False)

        # Send message
        await ctx.send(embed=embed)

        # Delete initial message
        await ctx.message.delete()


@bot.command()
async def finish(ctx):
    """
        Function bot discord to stop the research or the sell

        Input:
            - ctx: context discord
    """

    if ctx.channel.id == channelID:
        # If message is a response
        if ctx.message.reference is not None:
            # Take id
            idMessage = ctx.message.reference.message_id
            # Take initial message
            message = await ctx.channel.fetch_message(idMessage)

            # Save author
            embeds = message.embeds[0]
            description = embeds.description
            initId = description.find("@")

            if initId > 0:
                initialAuthor = int(description[initId + 1:-1])
                messageAuthor = ctx.message.author.id

                # If the author is the same as the creation message
                if messageAuthor == initialAuthor:
                    embeds.title = "ANNOUNCEMENT COMPLETED"
                    embeds.description = "***** Completed *******"
                await message.edit(embed=embeds)

    # Delete initial message
    await ctx.message.delete()

bot.run(botID)
