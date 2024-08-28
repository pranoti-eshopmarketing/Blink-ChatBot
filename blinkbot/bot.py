import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blinkbot.settings')
django.setup()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, filters, CallbackContext, ApplicationBuilder, CallbackQueryHandler, ContextTypes, MessageHandler
from dotenv import load_dotenv
import logging
from phantomConnect import create_solana_wallet, buy_solana, price
from blinkbot.models import UserProfile
from asgiref.sync import sync_to_async

async def start(update: Update, context : CallbackContext) -> None :
    chat_id = update.effective_chat.id
    username = update.effective_chat.username
    # Example of checking if a user profile exists
    user_profile = await sync_to_async(UserProfile.objects.get)(chat_id=chat_id)
    if user_profile : 
        pass
        
    #if wallet is not created then create wallet
    else :
        creds = create_solana_wallet()
        wallet_address = creds[0]
        private_key = creds[1]
        
        # else take public key from db
        # ---- logic here------
        chat_id = update.effective_chat.id
        username = update.effective_chat.username
        
        #adding data to db
        await sync_to_async(UserProfile.objects.update_or_create)(
            chat_id=chat_id,
            defaults={
                'username': username,
                'public_key': wallet_address,
                'private_key': private_key,
            }
        )
    
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
    chat_id = update.effective_chat.id
    user_profile = await sync_to_async(UserProfile.objects.get)(chat_id=chat_id)
    #get wallet address and private key 
    wallet_address = user_profile.public_key
    private_key =  user_profile.private_key
    # creds = create_solana_wallet()
    # wallet_address = creds[0]
    # private_key = creds[1]
    query = update.callback_query
    await query.answer()
    
    message = f"Your wallet details:\n\n💰Balance: *0 SOL*\n\nTo start trading, send some SOL to your Mon3y address.\n\n wallet address: *{wallet_address}* (Tap to copy) \n private key: *{private_key}* \n\n Once done, tap to refresh and your balance will appear here.\n\n *How to buy a token?* \n\n Simply enter the token symbol or contract address."
    
    buy = InlineKeyboardButton("Buy", callback_data='buy')
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

# user_states = {}

async def Buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Close", callback_data='close')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Buy Token:\n\nTo buy a token enter a ticker, token address, or a URL from pump.fun, Birdeye, Dexscreener or Meteora.",
        reply_markup=reply_markup
    )
    # user_states[update.message.chat_id] = 'awaiting_token'

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        if query.data == 'close':
            await query.message.delete()  # Delete the message with the "Close" button
        await query.answer()  # Acknowledge the button press
    else:
        print("Received callback query without query data.")
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # user_id = update.message.chat_id
    print(update.message.text)
    if update.message.text:
        token_address = update.message.text  # User-provided token address or ticker
        print("token_address", token_address)
        data = price(token_address)
        name = data['pairs'][0]['baseToken']['name']
        symbol = data['pairs'][0]['baseToken']['symbol']
        priceUsd = data['pairs'][0]['priceUsd']
        m5 = data['pairs'][0]['priceChange']['m5']
        h1 = data['pairs'][0]['priceChange']['h1']
        h6 = data['pairs'][0]['priceChange']['h6']
        h24 = data['pairs'][0]['priceChange']['h24']
        # Generate dummy token details for demonstration
        token_details = (
            f"{name} | {symbol} | {token_address}\n\n"
            f"Price: ${priceUsd}\n"
            f"5m: {m5}%, 1h: {h1}%, 6h: {h6}%, 24h: {h24}%\n"
            f"-------static data------\n"
            f"Market Cap: $8.85B\n\n"
            f"Price Impact (5.0000 SOL): 0.99%\n\n"
            f"Wallet Balance: 0.0048 SOL\n"
            f"To buy press one of the buttons below."
        )
        
        # Example buttons for buying
        keyboard = [
            [InlineKeyboardButton("Buy Now", url="http://example.com/buy")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(token_details, reply_markup=reply_markup)
        buy_solana(update.message.text)
        # Reset user state
        # user_states.pop(user_id, None)
    else:
        await update.message.reply_text("Please use the /buy command to start the process.")
      
         
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
    application.add_handler(CallbackQueryHandler(Buy, pattern='buy'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))
    
    #application starts
    application.run_polling()
    
if __name__ == '__main__':
    main()