import discord
from discord import app_commands
from discord.ext import commands

id_do_servidor = # ID do Server

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # Usado para evitar sincronizar comandos mais de uma vez
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados 
            await self.tree.sync(guild=discord.Object(id=id_do_servidor))  # Sincronizar comandos com o servidor
            self.synced = True
        print(f"Entramos como {self.user}.")

client = MyClient()

@client.tree.command(guild=discord.Object(id=id_do_servidor), name='website', description='Visit our website and stay up to date with all the news and events!')
async def website(interaction: discord.Interaction):
  embed = discord.Embed(
    title="Legend of Edda: Pegasus Website",
    description="Stay up to date with all the news and events!",
    url="https://www.legend-of-edda.com",
    color=16721741
  )
  embed.set_thumbnail(url="https://www.legend-of-edda.com/wp-content/uploads/2024/05/Logo_Pegasus_Branco.png")  # logo
  await interaction.response.send_message(embed=embed, ephemeral=False)  # False para que todos possam ver

@client.tree.command(guild=discord.Object(id=id_do_servidor), name='shop', description='Visit our shop and purchase various items, pets, mounts, costumes and of course, drachmas!')
async def shop(interaction: discord.Interaction):
  embed = discord.Embed(
    title="Legend of Edda: Pegasus Shop",
    description="Shall we go shopping?",
    url="https://www.legend-of-edda.com/shop/",
    color=16721741
  )
  embed.set_thumbnail(url="https://www.legend-of-edda.com/wp-content/uploads/2024/05/Logo_Pegasus_Branco.png")  # logo
  await interaction.response.send_message(embed=embed, ephemeral=False)  # False para que todos possam ver

@client.tree.command(guild=discord.Object(id=id_do_servidor), name='about', description='Learn more about the bot.')
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="About EddaBot",
        description="This bot helps you navigate through the world of Legend of Edda: Pegasus!",
        color=16721741
    )
    embed.set_thumbnail(url="https://www.legend-of-edda.com/bot-logo.png")  # logo
    embed.add_field(name="Commands", value="Use `/website` to visit our website.\nUse `/shop` to visit our shop.\nUse `/questions` for frequently asked questions.", inline=False)
    embed.add_field(name="Developer", value="Bot developed by <@1211781614196105288>.", inline=True)
    embed.add_field(name="Support", value="For support, visit our [Support Server](https://discord.com/channels/1072287585721925686/1130230460358860921).", inline=True)
    embed.set_footer(text="Legend of Edda: Pegasus Bot © 2024")

    await interaction.response.send_message(embed=embed, ephemeral=False)  # False para que todos possam ver


class QuestionsSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Gameplay", description="Questions about gameplay."),
            discord.SelectOption(label="Account & Technical Support", description="Questions about your account or if you need support."),
            discord.SelectOption(label="Other", description="Other questions.")
        ]
        super().__init__(placeholder="Choose a question category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        support = 1130230460358860921
        channel_questions = 1073356257999716412
        category_responses = {
            "Gameplay": "For gameplay questions if you're newbie, [visit here](https://www.legend-of-edda.com/beginners-guide/).",
            "Account & Technical Support": f"For account-related questions, open a ticket at <#{support}>",
            "Other": f"For other questions, you can visit the <#{channel_questions}> on Discord!",
        }
        selected_category = self.values[0]
        response = category_responses.get(selected_category, "For more information, visit: https://www.legend-of-edda.com/questions")
        await interaction.response.send_message(response, ephemeral=False)

class QuestionsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(QuestionsSelect())

@client.tree.command(guild=discord.Object(id=id_do_servidor), name='questions', description='Get answers to various questions about the game.')
async def questions(interaction: discord.Interaction):
    await interaction.response.send_message("Select a category to get answers to your questions:", view=QuestionsView(), ephemeral=False)

client.run('TOKEN')
