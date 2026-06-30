from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_CHAT_ID
from database import (
    approve_pembayaran,
    reject_pembayaran,
    get_pembayaran_by_id,
)


async def approve_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin approve pembayaran"""
    
    query = update.callback_query
    await query.answer()
    
    # Ambil pembayaran_id dari callback data
    pembayaran_id = int(query.data.split("_")[1])
    
    # Get data pembayaran
    pembayaran = get_pembayaran_by_id(pembayaran_id)
    
    if not pembayaran:
        await query.edit_message_caption("❌ Data tidak ditemukan")
        return
    
    chat_id_user = pembayaran[1]
    nama = pembayaran[2]
    
    # Update status di DB
    approve_pembayaran(pembayaran_id)
    
    # Edit pesan admin (hapus button)
    await query.edit_message_caption(
        caption=(
            f"📥 BUKTI PEMBAYARAN\n\n"
            f"🆔 ID Pembayaran : {pembayaran_id}\n"
            f"👤 Nama : {nama}\n"
            f"✅ Status : APPROVED\n\n"
            f"_Verified oleh admin_"
        ),
        parse_mode="Markdown",
    )
    
    # Notify user
    await context.bot.send_message(
        chat_id=chat_id_user,
        text=(
            f"✅ *Pembayaran Anda Telah Dikonfirmasi*\n\n"
            f"Terima kasih *{nama}* atas partisipasi Anda.\n\n"
            f"Semoga Allah ﷻ menerima dari kita semua. "
            f"Barakallahu fiikum! 🤲"
        ),
        parse_mode="Markdown",
    )


async def reject_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin reject pembayaran"""
    
    query = update.callback_query
    await query.answer()
    
    # Ambil pembayaran_id dari callback data
    pembayaran_id = int(query.data.split("_")[1])
    
    # Get data pembayaran
    pembayaran = get_pembayaran_by_id(pembayaran_id)
    
    if not pembayaran:
        await query.edit_message_caption("❌ Data tidak ditemukan")
        return
    
    chat_id_user = pembayaran[1]
    nama = pembayaran[2]
    
    # Update status di DB
    reject_pembayaran(pembayaran_id)
    
    # Edit pesan admin (hapus button)
    await query.edit_message_caption(
        caption=(
            f"📥 BUKTI PEMBAYARAN\n\n"
            f"🆔 ID Pembayaran : {pembayaran_id}\n"
            f"👤 Nama : {nama}\n"
            f"❌ Status : REJECTED\n\n"
            f"_Verified oleh admin_"
        ),
        parse_mode="Markdown",
    )
    
    # Notify user
    await context.bot.send_message(
        chat_id=chat_id_user,
        text=(
            f"⚠️ *Pembayaran Anda Ditolak*\n\n"
            f"Halo *{nama}*, bukti transfer Anda tidak sesuai.\n\n"
            f"Silakan hubungi admin untuk penjelasan lebih lanjut."
        ),
        parse_mode="Markdown",
    )