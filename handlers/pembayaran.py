from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from config import ADMIN_CHAT_ID
from database import simpan_pembayaran


async def bukti_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle foto bukti transfer"""
    
    if not update.message.photo:
        return

    user = update.effective_user
    photo = update.message.photo[-1].file_id
    
    # Ambil nama dari context atau username
    nama = context.user_data.get("nama_pembayar", user.full_name)

    # Simpan ke database
    pembayaran_id = simpan_pembayaran(
        chat_id=user.id,
        nama=nama,
        username=user.username or "-",
        photo_file_id=photo
    )

    # Tombol untuk admin approve/reject
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Terima", callback_data=f"approve_{pembayaran_id}"),
            InlineKeyboardButton("❌ Tolak", callback_data=f"reject_{pembayaran_id}"),
        ]
    ])

    # Kirim ke admin dengan tombol
    await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=photo,
        caption=(
            f"📥 BUKTI PEMBAYARAN\n\n"
            f"🆔 ID Pembayaran : {pembayaran_id}\n"
            f"👤 Nama : {nama}\n"
            f"📱 Username : @{user.username if user.username else '-'}\n"
            f"🆔 Chat ID : {user.id}\n"
            f"📅 Tanggal : {update.message.date}"
        ),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

    # Reply ke user
    await update.message.reply_text(
        "✅ *Bukti transfer berhasil dikirim.*\n\n"
        "Jazakumullahu khairan atas kepercayaan Ayah/Bunda yang telah berpartisipasi dalam mendukung *Indah Siar Kids*.\n\n"
        "Semoga Allah ﷻ membalas setiap kebaikan Ayah/Bunda dengan pahala yang berlipat ganda, melapangkan rezeki, serta menjadikannya sebagai amal jariyah.\n\n"
        "InsyaAllah dana yang terkumpul akan digunakan untuk mendukung keberlangsungan Channel *Indah Siar Kids* agar terus memberikan manfaat bagi umat.\n\n"
        "_Barakallahu fiikum._ 🤲",
        parse_mode="Markdown",
    )

    # Clear context
    context.user_data.pop("nama_pembayar", None)