from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import TOKEN
from handlers.start import start
from handlers.menu import menu
from handlers.pembayaran import bukti_transfer
from handlers.approval import approve_callback, reject_callback


app = Application.builder().token(TOKEN).build()

# Command
app.add_handler(CommandHandler("start", start))

# Menu
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu
    )
)

# Foto bukti transfer
app.add_handler(
    MessageHandler(
        filters.PHOTO,
        bukti_transfer
    )
)

# Approval callbacks (BARU)
app.add_handler(CallbackQueryHandler(approve_callback, pattern="^approve_"))
app.add_handler(CallbackQueryHandler(reject_callback, pattern="^reject_"))

print("=" * 40)
print("SIMPEI v2.0")
print("Bot sedang berjalan...")
print("=" * 40)

app.run_polling()