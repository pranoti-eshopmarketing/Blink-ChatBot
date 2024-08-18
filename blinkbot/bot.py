import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blinkbot.settings')
django.setup()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, CallbackQueryHandler
from dotenv import load_dotenv
import logging
from phantomConnect import create_solana_wallet
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from colorama import Fore, Style

async def start(update: Update, context : CallbackContext) -> None : 
    keyboard = [[InlineKeyboardButton("Create Wallet", callback_data='create_wallet')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message ="""   
    🎉 Welcome to Mon3y, the future of
    crypto trading \n\n🌟 *Trade to Earn passive income!*
    increase your trading volume & 
    referrals to boost your points,raising 
    your share of up to 10% of all our fees--
    paid out of SOL.\n\n👌 *User-Friendly Design:* Whether you're
    a beginner or a pro, our bot is tailored
    to fit all your trading needs.\n\n ⚙️ *Advanced Trading Features:*
    Harness the power of Limit, Take-Profit,
    and Stop-Loss orders \n\n 🔒 *Unmatched Speed, Fees & Security:* We
    optimise trading routes, while keeping
    your capital safety our top priority.
          """
    await update.message.reply_text(
        welcome_message,
          parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
    )
    
async def create_wallet(update : Update, context : CallbackContext):
    
    creds = create_solana_wallet()
    wallet_address = creds[0]
    private_key = creds[1]
    query = update.callback_query
    await query.answer()
    
    message = f"Your wallet details:\n\n💰Balance: *0 SOL*\n\nTo start trading, send some SOL to your Mon3y address.\n\n wallet address: *{wallet_address}* (Tap to copy) \n private key: *{private_key}* \n\n Once done, tap to refresh and your balance will appear here.\n\n *How to buy a token?* \n\n Simply enter the token symbol or contract address."
    
    buy = InlineKeyboardButton("buy", callback_data='buy')
    sell_and_manage = InlineKeyboardButton("Sell & Manage", callback_data='sellndmanage')
    orders = InlineKeyboardButton("Orders", callback_data='orders')
    my_points = InlineKeyboardButton("My points", callback_data='mypoints')
    wallet = InlineKeyboardButton("Wallet", callback_data='wallet')
    settings = InlineKeyboardButton("Settings", callback_data='settings')
    help = InlineKeyboardButton("Help", callback_data='help')
    refer = InlineKeyboardButton("Refer Friends", callback_data='refer')
    refresh = InlineKeyboardButton("refresh", callback_data='refresh')
    keyboard = [
        [buy,sell_and_manage],
        [orders, my_points],
        [wallet,settings],
        [help,refer],
        [refresh],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

async def help(update : Update, context : CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    message = """
    *Help:*
    
    *---General---*
    *How to buy?* Simply reply with a
    token symbol or address. You will
    then get an overview of the token,
    along with buy options.
    
    *How to sell?*
    All tokens that you own will be 
    displayed under "Positions Overview"
    from the Home screen. You can either
    click on the token to sell from here,
    or go to "Sell & Manage", where you'll
    be presented with options.
    
    *Is my crypto safe?"* The safety of your
    crypto is our main priority, and we 
    have multiple security measures in 
    place to protect it. When depositing
    crypto to your wallet, please make sure
    that you are using the official Mon3y 
    Bot from URL: www.mon3ybot.com or
    alternatively, only deposit a small
    amount of SOL to test trade with.
    
    Please also ensure that you have 2FA
    enabled for sends.
    
    *Why is my net profit lower than
    expected?* Your Net Profit represents
    your actual profit after all fees have 
    been deducted.
    
    *---FEES---
    Is Mon3y free? How much do i pay for
    transactions?* Mon3y is free to use.
    We only charge you 1% per trade.
    
    *---Trade to Earn---
    What are points?*
    Points represent your share of the
    revenue distributed from our trading 
    fees. For example, if we allocate 
    10,000 points across all traders
    and you have earned 1,000 of these
    points, you are entitled to 10%
    of all trading fees collected,
    paid out in SOL.
    
    *How do i earn points?*
    Points are awarded based on your 
    trading volume and the activity
    of those you refer:
    *⚫Trading volume:* You earn 10 
        points for every SOL you 
        trade. For instance, if
        you trade 100 SOL, you
        will receive 1,000 points.
    *⚫Referrals:* Increase your 
        points by referring friends.
        The points your referrals earn
        from their trading will also
        be added to your total, effectively
        boosting your share of distirbuted 
        fees, up to a maximum of 50,000
        points per month from referrals.
        PLUS, your referral gets a 1,000
        point bonus for joining.
    
    *Is there a maximum limit to the points 
    I can earn?*
    No. The only cap is on referral points,
    up to, maximum of 50,000 per month
    as mentioned above. This cap ensures
    fairness and promotes a more equitable
    distribution of fees among all participants.
         
    """
    
    keyboard = [[InlineKeyboardButton("Close", callback_data='close')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.message.edit_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"Error in 'help' function: {e}")
        await query.message.reply_text("An error occurred while processing your request.")
 
async def wallet(update : Update, context : CallbackContext) :
    query = update.callback_query
    await query.answer()
    
    balance_details = '''
    *Your Wallet:*
    
    *Address*
    ----Addres will come here (Tap to copy)----
    
    💰Balance: *0 SOL*
    
    _Tap to copy address and send SOL to deposit_
    '''
    
    solscan = InlineKeyboardButton("Solscan", callback_data='solscan')
    close = InlineKeyboardButton("Close", callback_data='close')
    deposit_sol = InlineKeyboardButton("Deposit SOL", callback_data='deposit_sol')
    withdraw = InlineKeyboardButton("Withdraw All SOL", callback_data='withdrawall')
    withdraw_x = InlineKeyboardButton("Withdraw X SOL", callback_data='withdrawx')
    reset = InlineKeyboardButton("Reset Wallet", callback_data='reset')
    export_private_key = InlineKeyboardButton("Export Private Key", callback_data='export_private_key')
    refresh = InlineKeyboardButton("refresh", callback_data='refresh')
    
    keyboard = [
        [solscan, close],
        [deposit_sol],
        [withdraw, withdraw_x],
        [reset, export_private_key],
        [refresh]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.message.edit_text(balance_details, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"Error in 'help' function: {e}")
        await query.message.reply_text("An error occurred while processing your request.")

async def settings(update : Update, context : CallbackContext):
    query = update.callback_query
    await query.answer()
    
    message = '''
    *Settings:*
    
    *Announcements:* Occasional 
    annoucements. Tap to toggle.
    
    
    *AUTO BUY* Immediately buy
    when pasting token address.
    Tap to toggle.
    
    *BUTTONS CONFIG* Customize
    your buy and sell buttons for
    buy token and manage position.
    Tap to edit.
    
    *SLIPPAGE CONFIG* Customize 
    your slippage settings for buys
    and sells. Tap to edit. Max Price
    impact is to protect against
    trades in extremely illiquid pools
    
    *TRANSACTION PRIORITY*
    Increase your Transaction Priority
    to improve transaction speed. Select
    preset or tap to edit.
    
    *MEV PROTECT* MEV Protect
    accelerates your transactions
    and protect against frontruns to
    make sure you get the best price
    possible. *Turbo:* BONKbot will 
    use MEV Protect, but if unprotected
    sending is faster it will use that
    instead. *Secure:* Transactions are
    guaranteed to be protected. This is 
    the ultra secure option, but may
    be slower.
    
    '''
    
    keyboard = [
        [InlineKeyboardButton("🟢 Announcements", callback_data='announcements')],
        [InlineKeyboardButton("---Auto Buy---", callback_data='auto_buy')],
        [InlineKeyboardButton("🔴 Disabled", callback_data='auto_buy'),InlineKeyboardButton("✏️ 0.1 SOL", callback_data='auto_buy')],
        [InlineKeyboardButton("---Buy Config---", callback_data='buy_config'), InlineKeyboardButton("---Sell Config---", callback_data='sell_config')],
        [InlineKeyboardButton("✏️ B1: 0.25 SOL", callback_data='auto_buy'), InlineKeyboardButton("✏️ S1:25%", callback_data='auto_buy')],
        [InlineKeyboardButton("✏️ B2: 1 SOL", callback_data='auto_buy'), InlineKeyboardButton("✏️ S2:50%", callback_data='auto_buy')],
        [InlineKeyboardButton("---Slippage Config---", callback_data='auto_buy')],
        [InlineKeyboardButton("✏️ Buy: 10%", callback_data='auto_buy'),InlineKeyboardButton("✏️ Sell: 10%", callback_data='auto_buy')],
        [InlineKeyboardButton("✏️  Max Price Import: 25%", callback_data='auto_buy')],
        [InlineKeyboardButton("↔️ MEV Protecy: Turbo 🚀", callback_data='auto_buy')],
        [InlineKeyboardButton("---Transaction Priority---", callback_data='auto_buy')],
        [InlineKeyboardButton("↔️ High", callback_data='auto_buy'),InlineKeyboardButton("✏️ 0.005 SOL", callback_data='auto_buy') ],
        [InlineKeyboardButton("Close", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.message.edit_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"Error in 'help' function: {e}")
        await query.message.reply_text("An error occurred while processing your request.")
        
def main() -> None:
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
    logger = logging.getLogger(__name__)
    load_dotenv()
    token = os.getenv("TOKEN")
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(create_wallet, pattern='create_wallet'))
    application.add_handler(CallbackQueryHandler(help, pattern='help'))
    application.add_handler(CallbackQueryHandler(wallet, pattern='wallet'))
    application.add_handler(CallbackQueryHandler(settings, pattern='settings'))
    application.run_polling()
    
if __name__ == '__main__':
    main()