import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import os

TOKEN = os.getenv("BOT_TOKEN", "your_token_here")

bot = Bot(token=TOKEN)
dp = Dispatcher()

MODULE_PATH = "app"
MODULE_COUNT = 7

@dp.message()
async def show_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Модуль {i}", callback_data=f"module_{i}")]
        for i in range(1, MODULE_COUNT + 1)
    ])
    await message.answer("📚 Выберите модуль обучения:", reply_markup=keyboard)

@dp.callback_query()
async def send_module(callback: CallbackQuery):
    module_number = callback.data.replace("module_", "")
    file_path = os.path.join(MODULE_PATH, f"module_{module_number}.txt")
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        await callback.message.edit_text(f"Модуль {module_number}

{content}")
    except FileNotFoundError:
        await callback.message.edit_text("Модуль не найден.")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
