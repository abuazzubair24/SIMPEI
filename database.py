from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_CHAT_ID
from database import simpan_pembayaran


async def bukti_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("menunggu_bukti"):
        return

    user = update.effective_user
    caption = update.message.caption or ""
    nama = caption.replace("Nama :", "").replace("Nama:", "").strip() or user.full_name
    username = user.username if user.username else "-"

    photo = update.message.photo[-1]
    file_id = photo.file_id

    pembayaran_id = simpan_pembayaran(
        chat_id=user.id,
        nama=nama,
        username=username,
        photo_file_id=file_id,
    )

    context.user_data["menunggu_bukti"] = False

    await update.message.reply_text(
        f"✅ Bukti transfer diterima!\n\n"
        f"Nama: *{nama}*\n"
        f"ID: `{pembayaran_id}`\n\n"
        f"Admin akan memverifikasi segera. Terima kasih!",
        parse_mode="Markdown"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{pembayaran_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{pembayaran_id}"),
        ]
    ])

    await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=file_id,
        caption=(
            f"📥 *BUKTI PEMBAYARAN*\n\n"
            f"🆔 ID: {pembayaran_id}\n"
            f"👤 Nama: {nama}\n"
            f"💬 Chat ID: {user.id}"
        ),
        parse_mode="Markdown",
        reply_markup=keyboard
    )