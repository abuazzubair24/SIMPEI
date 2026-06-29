from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_CHAT_ID


async def bukti_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return

    user = update.effective_user
    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=photo,
        caption=(
            f"📥 BUKTI PEMBAYARAN\n\n"
            f"👤 Nama : {user.full_name}\n"
            f"📱 Username : @{user.username if user.username else '-'}\n"
            f"🆔 Chat ID : {user.id}"
        ),
    )

    await update.message.reply_text(
        "✅ *Bukti transfer berhasil dikirim.*\n\n"
        "Jazakumullahu khairan atas kepercayaan Ayah/Bunda yang telah berpartisipasi dalam mendukung *Indah Siar Kids*.\n\n"
        "Semoga Allah ﷻ membalas setiap kebaikan Ayah/Bunda dengan pahala yang berlipat ganda, melapangkan rezeki, serta menjadikannya sebagai amal jariyah.\n\n"
        "InsyaAllah dana yang terkumpul akan digunakan untuk mendukung keberlangsungan Channel *Indah Siar Kids* agar terus memberikan manfaat bagi umat.\n\n"
        "_Barakallahu fiikum._ 🤲",
        parse_mode="Markdown",
    )