import random

class RockPaperScissors:
    def __init__(self):
        self.__answers = ['Камень', 'Ножницы', 'Бумага']
        self.__answer = None

    async def __is_win(self, user_choice) -> bool | None:
        answer = random.choice(self.__answers)
        self.__answer = answer
        if user_choice == 'Камень' and answer == 'Ножницы':
            victory = True
        elif user_choice == 'Ножницы' and answer == 'Бумага':
            victory = True
        elif user_choice == 'Бумага' and answer == 'Камень':
            victory = True
        elif user_choice == answer:
            victory = None
        else:
            victory = False
        return victory

    async def get_embed_description(self, user_choice) -> str:
        victory = await self.__is_win(user_choice)
        if victory:
            description=f"Ты выбрал `{user_choice}`, а я выбрал `{self.__answer}` \n"\
                        "Впервые в своей жизни ты победил... УРАААА!!!!11!1! 🎉🥳🥳"\
                        "ты блядь гомодрил обоссаный, сын говна триебливого, пшёл нахуй быстро"
        elif victory is False:
            description=f"Ты выбрал `{user_choice}`, а я выбрал `{self.__answer}` \n"\
                        "Ну да. Ты просрал, как всегда, АХАААХАХХААЗЗАЗА 🤪🤣"
        else:
            description=f"Ты выбрал `{user_choice}`, а я выбрал `{self.__answer}` \n"\
                        "Ничья, блядун ты вонючий. Го ещё раз, придурок малолетний! 😐"
        return description

class Slots:
    """
    Multipliers:

    👑👑👑 = x10
    👑👑 = x6.66
    7️⃣7️⃣7️⃣ = x50
    7️⃣7️⃣ = x7.5
    7️⃣ = x1.85
    🔔🔔🔔 = x4
    🔔🔔 = x2.5
    🍒🍒🍒 = x2.5
    🍒🍒 = x0.45
    ☠️☠️☠️ = x1.5
    ☠️☠️ = x0.65
    """
    def __init__(self):
        self.__SYMBOLS = ['🍒', '☠️', '🔔', '👑', '7️⃣']
        self.__WEIGHTS = [30, 25, 20, 15, 10]
        self.slots = None

    async def __spin_slots(self) -> list:
        return random.choices(
            self.__SYMBOLS,
            weights=self.__WEIGHTS,
            k=3
        )

    async def get_result(self) -> float:
        self.slots = await self.__spin_slots()
        counts = {
            symbol: self.slots.count(symbol)
            for symbol in self.__SYMBOLS
        }

        if counts['👑'] == 3:
            return 10

        if counts['👑'] == 2:
            return 6.66

        if counts['7️⃣'] == 3:
            return 50

        if counts['7️⃣'] == 2:
            return 7.5

        if counts['7️⃣'] == 1:
            return 1.85

        if counts['🔔'] == 3:
            return 4

        if counts['🔔'] == 2:
            return 2.5

        if counts['🍒'] == 3:
            return 2.5

        if counts['🍒'] == 2:
            return 0.45

        if counts['☠️'] == 3:
            return 1.5

        if counts['☠️'] == 2:
            return 0.65

        return 0

    async def slots_parsed(self) -> str:
        slots = str(self.slots[0]) + str(self.slots[1]) + str(self.slots[2])
        return slots