import requests
import random
from bs4 import BeautifulSoup as bs

class JokeParser:
    def __init__(self):
        self.__JOKE_WEBSITE = "https://baneks.ru/"

    async def __get_url(self, joke_number)-> str:
        if joke_number > 1142:
            raise ValueError("param joke_number must be not bigger as 1142")
        joke_url = self.__JOKE_WEBSITE + str(joke_number)
        return joke_url

    async def __parse(self, joke_number) -> str:
        joke_url = await self.__get_url(joke_number)
        request = requests.get(joke_url)
        soup = bs(request.text, "html.parser")
        parsed = soup.find_all("article")
        joke = ""
        for jokes in parsed:
            joke += jokes.p.text
        return joke

    async def get_joke(self, joke_number) -> str:
        if joke_number is None:
            joke_number = str(random.randint(1, 1142))
        joke = await self.__parse(joke_number)
        return joke