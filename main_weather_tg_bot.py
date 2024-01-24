import asyncio
from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher, types
import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        "Этот бот предоставляет информацию о погоде. Для получения погоды введите название города.\n"
        "Доступные команды:\n"
        "/help - Получить справку\n"
        "/about - О боте\n"
        "/author - Информация об авторе\n"
        "/source - Исходный код на GitHub\n"
        "/start - Начать"
    )
    await message.answer(help_text)


@dp.message(Command("about"))
async def about_command(message: types.Message):
    about_text = (
        "Этот бот создан для предоставления текущей информации о погоде.\n"
        "Он использует данные от OpenWeatherMap API.[https://openweathermap.org/]"
    )
    await message.answer(about_text)


@dp.message(Command("author"))
async def author_command(message: types.Message):
     await message.answer("Автор этого бота - Ерасыл [https://aespi808.github.io/aespi/]")


@dp.message(Command("source"))
async def source_command(message: types.Message):
    source_text = "Исходный код этого бота доступен на GitHub: [https://github.com/pythontoday/weather_telegram_bot/blob/master/main_weather_tg_bot.py]"
    await message.answer(source_text)


@dp.message()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]


        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"***Хорошего дня!***"
                            f"https://www.windy.com/?0.088,94.131,3,m:eXWahZk"
                            )
        




    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())