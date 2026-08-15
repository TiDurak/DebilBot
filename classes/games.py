import random

class RockPaperScissors:
    def __init__(self):
        super().__init__()
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
    def __init__(self):
        super().__init__()
        self.__SYMBOLS = ['🍒', '🔔', '7️⃣', '👑', '☠️']
        self.__SLOTS = [0, 1, 2]
        self.slots = None

    async def __spin_slots(self) -> list:
        slots = self.__SLOTS
        for i in range(3):
            slots[i] = self.__SYMBOLS[random.randint(0, 4)]

        return slots

    async def get_result(self) -> str:
        slots = await self.__spin_slots()
        self.slots = slots
        is_same = True if slots[0] == slots[1] == slots[2] else False
        if is_same and self.__SYMBOLS[4] in slots:
            result = 'ЛОШАРА! Ваш баланс обнулён'
        elif is_same and self.__SYMBOLS[3] in slots:
            result = '+ 5 000 баксов на ваш счёт'
        elif is_same and self.__SYMBOLS[2] in slots:
            result = '+ 10 000 баксов на ваш счёт'
        elif is_same and self.__SYMBOLS[1] in slots:
            result = '+ 15 000 баксов на ваш счёт'
        elif is_same and self.__SYMBOLS[0] in slots:
            result = 'ДЖЕКПОТ!!! + 1 000 000 баксов на ваш счёт'
        elif self.__SYMBOLS[0] == slots[0] == slots[1] or slots[0] == slots[2] == self.__SYMBOLS[0] or slots[1] == slots[2] == self.__SYMBOLS[0]:
            result = '+ 3 500 баксов на ваш счёт'
        elif self.__SYMBOLS[0] in slots:
            result = '+ 1 500 баксов на ваш счёт'
        else:
            result = 'Ничего('
        return result

    async def slots_parsed(self) -> str:
        slots = str(self.slots[0]) + str(self.slots[1]) + str(self.slots[2])
        return slots