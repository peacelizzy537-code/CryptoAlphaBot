import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Your links
CHANNEL_LINK = 'https://t.me/blaqmarqetnotify'
CONTACT_LINK = 'https://t.me/annopow'

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with crypto options."""
    user = update.effective_user
    
    welcome_message = (
        f"🚀 Welcome to CryptoGuruBot, {user.first_name}!\n\n"
        "💎 **Your Gateway to Crypto Advertising & Bot Solutions**\n\n"
        "We help crypto projects succeed on Telegram with:\n\n"
        "🔹 **Ad Fix Services** - Get rejected ads approved\n"
        "🔹 **Approved Bots** - Ready-to-use, already approved\n"
        "🔹 **Custom Bots** - Trading, arbitrage, automation\n"
        "🔹 **Growth Management** - CPM optimization & scaling\n\n"
        "📊 **Choose an option below to get started:**"
    )
    
    keyboard = [
        [InlineKeyboardButton("🤖 Crypto Bot Development", callback_data="bot_services")],
        [InlineKeyboardButton("📢 Ad Fix & Approval", callback_data="ad_services")],
        [InlineKeyboardButton("📈 Market Insights", callback_data="market_insights")],
        [InlineKeyboardButton("📩 Contact Support", url=CONTACT_LINK)],
        [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "bot_services":
        text = (
            "🤖 **Crypto Bot Development Services**\n\n"
            "We build high-performance Telegram bots for:\n\n"
            "🔹 **Trading Bots** - Automated crypto trading\n"
            "🔹 **Arbitrage Bots** - Price difference detection\n"
            "🔹 **Volume Bots** - Generate trading volume\n"
            "🔹 **Moderator Bots** - Community management\n"
            "🔹 **Alert Bots** - Price notifications\n"
            "🔹 **Arbitrage Bots** - Price difference detection\n\n"
            "💰 **Pricing:**\n"
            "• Basic Bot: $150\n"
            "• Approved Bot: $250\n"
            "• Custom Automation: $500\n\n"
            "📩 Contact us to get started!"
        )
        keyboard = [
            [InlineKeyboardButton("📩 Contact for Bot", url=CONTACT_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif query.data == "ad_services":
        text = (
            "📢 **Telegram Ad Fix & Approval Services**\n\n"
            "Get your crypto ads approved fast:\n\n"
            "🔹 **Ad Destination Issues** - Fix landing page problems\n"
            "🔹 **Prohibited Content** - Crypto, gambling, adult\n"
            "🔹 **Destination Quality** - Improve user experience\n"
            "🔹 **Irrelevant Destination** - Match ad to content\n\n"
            "💰 **Pricing:**\n"
            "• Basic Fix: $200\n"
            "• Approved Channel/Bot: $350\n"
            "• Growth Management: $500/month\n\n"
            "📩 Contact us for a free consultation!"
        )
        keyboard = [
            [InlineKeyboardButton("📩 Contact for Ads", url=CONTACT_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif query.data == "market_insights":
        text = (
            "📊 **Crypto Market Insights**\n\n"
            "Stay updated with the latest crypto trends:\n\n"
            "🔹 **Bitcoin Dominance**: 52.3%\n"
            "🔹 **Ethereum Gas**: 12 GWEI\n"
            "🔹 **DeFi TVL**: $45.2B\n"
            "🔹 **Daily Trading Volume**: $68.7B\n"
            "🔹 **BTC Price**: $62,450\n"
            "🔹 **ETH Price**: $3,420\n\n"
            "📢 Join our channel for daily updates!"
        )
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif query.data == "menu":
        text = (
            "🚀 Welcome back to CryptoGuruBot!\n\n"
            "Choose an option below:"
        )
        keyboard = [
            [InlineKeyboardButton("🤖 Crypto Bot Development", callback_data="bot_services")],
            [InlineKeyboardButton("📢 Ad Fix & Approval", callback_data="ad_services")],
            [InlineKeyboardButton("📈 Market Insights", callback_data="market_insights")],
            [InlineKeyboardButton("📩 Contact Support", url=CONTACT_LINK)],
            [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a help message."""
    help_text = (
        "🤖 **CryptoGuruBot Help**\n\n"
        "Available commands:\n"
        "/start - Show main menu\n"
        "/help - Show this help\n"
        "/services - List all services\n"
        "/contact - Contact support\n"
        "/channel - Join our channel\n\n"
        "🔹 We help crypto projects succeed on Telegram!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all services."""
    services_text = (
        "💎 **Our Crypto Services**\n\n"
        "1️⃣ **Ad Fix Service** - $200+\n"
        "   Fix prohibited content & get approved\n\n"
        "2️⃣ **Approved Bots** - $250\n"
        "   Ready-to-use, already approved\n\n"
        "3️⃣ **Custom Bots** - $500\n"
        "   Full automation & custom features\n\n"
        "4️⃣ **Growth Management** - $500/month\n"
        "   CPM optimization & ad spend management\n\n"
        "📩 Contact us for a free consultation!"
    )
    keyboard = [
        [InlineKeyboardButton("📩 Contact Us", url=CONTACT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(services_text, reply_markup=reply_markup, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends contact information."""
    contact_text = (
        "📩 **Contact CryptoGuruBot**\n\n"
        "🔹 **Telegram**: https://t.me/annopow\n"
        "🔹 **Channel**: https://t.me/blaqmarqetnotify\n\n"
        "We respond within 1-2 hours!\n"
        "⏰ **24/7 Support Available**\n\n"
        "💬 Send us a message and we'll help you!"
    )
    keyboard = [
        [InlineKeyboardButton("📩 Message Us", url=CONTACT_LINK)],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(contact_text, reply_markup=reply_markup, parse_mode='Markdown')

async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends channel link."""
    channel_text = (
        "📢 **Join Our Channel**\n\n"
        "Get daily crypto insights, trading tips, and advertising strategies!\n\n"
        "🔹 **BLAQSTRATEGY Channel**: https://t.me/blaqmarqetnotify"
    )
    keyboard = [
        [InlineKeyboardButton("📢 Join Now", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(channel_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- Main Function ---

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ BOT_TOKEN not set! Please set it in Railway environment variables.")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("services", services_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("channel", channel_command))
    
    # Register button handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the Bot
    logger.info("🤖 CryptoGuruBot is starting...")
    logger.info("📢 Channel link: https://t.me/blaqmarqetnotify")
    logger.info("✅ CryptoGuruBot is running!")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
