"""
Telegram Bot for Raze Casino
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎰 Открыть Казино",
                web_app=WebAppInfo(url=config.WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Канал",
                url=f"https://t.me/{config.CHANNEL_ID}"
            )
        ]
    ])
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command"""
    user_name = message.from_user.first_name
    
    welcome_text = (
        f"🎰 <b>Добро пожаловать в Raze Casino, {user_name}!</b>\n\n"
        f"🎮 <b>Доступные игры:</b>\n"
        f"├ 💥 Краш - Поймай момент\n"
        f"├ 💎 Мины - Открывай клетки\n"
        f"├ 🏰 Башня - Поднимайся вверх\n"
        f"└ 🎡 Рулетка - x2, x3, x5, x30\n\n"
        f"💰 <b>Минимальная ставка:</b> $0.30\n"
        f"💵 <b>Минимальный вывод:</b> $2.00\n\n"
        f"🎁 <b>Бонусы:</b>\n"
        f"├ Ежедневный бонус\n"
        f"├ Реферальная программа\n"
        f"└ Промокоды\n\n"
        f"Нажмите кнопку ниже чтобы начать играть! 👇"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )
    
    # Log to channel
    await log_to_channel(
        f"👤 Новый пользователь\n"
        f"ID: {message.from_user.id}\n"
        f"Username: @{message.from_user.username or 'нет'}\n"
        f"Имя: {user_name}"
    )


@dp.message(Command("app"))
async def cmd_app(message: Message):
    """Open web app"""
    await message.answer(
        "🎰 Открыть Raze Casino:",
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Help command"""
    help_text = (
        "📖 <b>Помощь</b>\n\n"
        "<b>Команды:</b>\n"
        "/start - Главное меню\n"
        "/app - Открыть казино\n"
        "/help - Эта справка\n\n"
        "<b>Игры:</b>\n"
        "💥 <b>Краш</b> - Выводи до того как ракета улетит\n"
        "💎 <b>Мины</b> - Открывай безопасные клетки\n"
        "🏰 <b>Башня</b> - Поднимайся по уровням\n"
        "🎡 <b>Рулетка</b> - Ставь на множители\n\n"
        "По вопросам пишите @admin"
    )
    
    await message.answer(help_text)


async def log_to_channel(text: str, level: str = "INFO"):
    """Log message to logs channel"""
    try:
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "ADMIN": "👑"
        }
        
        emoji = emoji_map.get(level, "📝")
        
        await bot.send_message(
            config.LOGS_CHANNEL_ID,
            f"{emoji} {text}"
        )
    except Exception as e:
        logger.error(f"Failed to log to channel: {e}")


async def notify_user(user_id: int, text: str):
    """Send notification to user"""
    try:
        await bot.send_message(user_id, text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Failed to notify user {user_id}: {e}")


async def main():
    """Main function"""
    logger.info("🚀 Starting Raze Casino Bot...")
    
    try:
        # Start polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
