import os
from telegram import Update
from telegram.ext import ContextTypes

from config import (
    BANK,
    NO_REKENING,
    ATAS_NAMA,
    LINK_EDISI,
    TELEGRAM_ADMIN,
    WHATSAPP_ADMIN,
    CHANNEL,
    QRIS,
)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # ==========================
    # EDISI TERBARU
    # ==========================

    if text == "📚 Edisi Terbaru":

        await update.message.reply_text(
            f"*📚 Edisi Terbaru*\n\n"
            f"Silakan akses melalui link berikut:\n\n"
            f"{LINK_EDISI}",
            parse_mode="Markdown"
        )

    # ==========================
    # BAYAR IURAN
    # ==========================

    elif text == "💳 Bayar Iuran":

        if os.path.exists(QRIS):

            with open(QRIS, "rb") as foto:

                await update.message.reply_photo(
                    photo=foto,
                    caption=(
                        f"*💳 Pembayaran Iuran*\n\n"
                        f"*{BANK}* : `{NO_REKENING}`\n"
                        f"*a.n.* {ATAS_NAMA}\n\n"
                        "Silakan transfer *sesuai kemampuan dan keikhlasan*.\n\n"
                        "Setelah melakukan transfer silakan pilih menu\n"
                        "*📤 Kirim Bukti Transfer*."
                    ),
                    parse_mode="Markdown"
                )

        else:

            await update.message.reply_text(
                "QRIS tidak ditemukan."
            )

    # ==========================
    # CARA PEMBAYARAN
    # ==========================

    elif text == "📄 Cara Pembayaran":

        await update.message.reply_text(
            "*📄 Cara Pembayaran*\n\n"
            "1. Scan QRIS atau transfer ke rekening.\n"
            "2. Simpan bukti transfer.\n"
            "3. Klik menu *📤 Kirim Bukti Transfer*.\n"
            "4. Kirim nama dan foto bukti transfer.\n"
            "5. Admin akan memverifikasi pembayaran.",
            parse_mode="Markdown"
        )

    # ==========================
    # KIRIM BUKTI
    # ==========================

    elif text == "📤 Kirim Bukti Transfer":

        context.user_data["menunggu_bukti"] = True

        await update.message.reply_text(
            "*📤 Kirim Bukti Transfer*\n\n"
            "Silakan kirim:\n\n"
            "• Nama\n"
            "• Foto bukti transfer\n\n"
            "Contoh:\n"
            "Nama : Ahmad Fauzi\n"
            "(Lampirkan foto bukti transfer)",
            parse_mode="Markdown"
        )

    # ==========================
    # HUBUNGI ADMIN
    # ==========================

    elif text == "☎️ Hubungi Admin":

        await update.message.reply_text(
            f"*☎ Hubungi Admin*\n\n"
            f"Telegram : {TELEGRAM_ADMIN}\n\n"
            f"WhatsApp : {WHATSAPP_ADMIN}\n\n"
            f"Channel :\n{CHANNEL}",
            parse_mode="Markdown"
        )