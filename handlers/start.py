from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

from database import simpan_anggota


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    simpan_anggota(
        chat_id=user.id,
        nama=user.full_name,
        username=user.username if user.username else "-",
        tanggal=datetime.now().strftime("%d-%m-%Y %H:%M")
    )

    keyboard = [
    ["📚 Edisi Terbaru"],
    ["💳 Bayar Iuran", "📄 Cara Pembayaran"],
    ["📤 Kirim Bukti Transfer"],
    ["☎️ Hubungi Admin"]
]

    await update.message.reply_text(
        "Assalamu'alaikum warahmatullahi wabarakatuh.\n\n"
        "*Selamat datang di Bot Pengingat Iuran Indah Siar Kids.*\n\n"
        "Silakan pilih menu di bawah ini.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        ),
        parse_mode="Markdown"
    )