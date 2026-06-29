from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_CHAT_ID
from database import approve_pembayaran, reject_pembayaran, get_pembayaran_by_id


async def approve_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    pembayaran_id = int(query.data.split("_")[1])
    pembayaran = get_pembayaran_by_id(pembayaran_id)

    if not pembayaran:
        await query.edit_message_caption("❌ Data tidak ditemukan")
        return

    chat_id_user = pembayaran[1]
    nama = pembayaran[2]

    approve_pembayaran(pembayaran_id)

    await query.edit_message_caption(
        caption=(
            f"📥 *BUKTI PEMBAYARAN*\n\n"
            f"🆔 ID: {pembayaran_id}\n"
            f"👤 Nama: {nama}\n"
            f"✅ Status: APPROVED\n\n"
            f"_Verified oleh admin_"
        ),
        parse_mode="Markdown",
    )

    await context.bot.send_message(
        chat_id=chat_id_user,
        text=(
            f"✅ *Pembayaran Anda Telah Dikonfirmasi*\n\n"
            f"Terima kasih {nama} atas partisipasi Anda.\n\n"
            f"Semoga Allah ﷻ menerima dari kita semua. Barakallahu fiikum! 🤲"
        ),
        parse_mode="Markdown",
    )


async def reject_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    pembayaran_id = int(query.data.split("_")[1])
    pembayaran = get_pembayaran_by_id(pembayaran_id)

    if not pembayaran:
        await query.edit_message_caption("❌ Data tidak ditemukan")
        return

    chat_id_user = pembayaran[1]
    nama = pembayaran[2]

    reject_pembayaran(pembayaran_id)

    await query.edit_message_caption(
        caption=(
            f"📥 *BUKTI PEMBAYARAN*\n\n"
            f"🆔 ID: {pembayaran_id}\n"
            f"👤 Nama: {nama}\n"
            f"❌ Status: REJECTED\n\n"
            f"_Verified oleh admin_"
        ),
        parse_mode="Markdown",
    )

    await context.bot.send_message(
        chat_id=chat_id_user,
        text=(
            f"⚠️ *Pembayaran Anda Ditolak*\n\n"
            f"Halo {nama}, bukti transfer Anda tidak sesuai.\n\n"
            f"Silakan hubungi admin untuk penjelasan lebih lanjut."
        ),
        parse_mode="Markdown",
    )