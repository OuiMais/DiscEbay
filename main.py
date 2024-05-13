"""
    Projet : DiscEbay
    Date Creation : 12/05/2024
    Date Revision : 13/05/2024
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Bot discord de type leboncoin ou ebay
"""

import io
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def toSell(ctx, arg):
    """
        Function bot discord to add sell announcement

        Input:
            - ctx: context discord
            - arg: [string] with all information for announcement

    """
    if ctx.channel.id == 1239158146602106941:
        # Separation of all element for the announcement
        separation = [arg.find("title="), arg.find("price="), arg.find("description=")]

        title = arg[6:separation[1]]
        price = arg[separation[1] + 6:separation[2]]
        description = arg[separation[2] + 12:]

        # Prepare the message in embed
        embed = discord.Embed(title="ANNONCE DE VENTE", description=f"Créée par {ctx.author.mention}", color=0x00ff00)
        embed.add_field(name="Titre", value=title, inline=False)
        embed.add_field(name="Prix", value=price, inline=False)
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
    if ctx.channel.id == 1239158146602106941:
        # Separation of all element for the announcement
        separation = [arg.find("title="), arg.find("description=")]

        title = arg[6:separation[1]]
        description = arg[separation[1] + 12:]

        # Prepare the message in embed
        embed = discord.Embed(title="RECHERCHE", description=f"Créée par {ctx.author.mention}", color=0x00ff00)
        embed.add_field(name="Titre", value=title, inline=False)
        embed.add_field(name="Description", value=description, inline=False)

        # Send message
        await ctx.send(embed=embed)

        # Delete initial message
        await ctx.message.delete()

@bot.command()
async def finish(ctx, message_id):
    # Marquer l'annonce comme terminée
    message = await ctx.channel.fetch_message(message_id)
    await message.edit(content="Vente terminée / Recherche terminée")

bot.run('MTIzOTE2MjgwNDU0NDYwNjIzOQ.G4MJV4.jBojU7Wq00Bh_4WzM_HwFKv5i31L0iHMWNReJ8')

