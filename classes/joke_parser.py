class Joke:
    def __init__(self):

    joke_website = "https://baneks.ru/"

            joke_url = joke_website + str(joke_number)
            request = requests.get(joke_url)
            soup = bs(request.text, "html.parser")

            parsed = soup.find_all("article")
            for jokes in parsed:
                embed = discord.Embed(color=settings.get("main_embed_color"), title=f"📋 Анекдот #{str(joke_number)}",
                                      description=jokes.p.text)
                embed.set_footer(text="Этот даунский анек взят (*скомунизжен) из https://baneks.ru/")
                await interaction.response.send_message(embed=embed)
                message = await interaction.original_response()

                emojis = ['🤣', '😐', '💩', '🪗']

                for emoji in emojis:
                    await message.add_reaction(emoji)