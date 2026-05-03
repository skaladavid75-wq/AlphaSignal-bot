import os
import json
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN ID", "0"))
URL = os.environ.get("RENDER_EXTERNAL_URL")

VIP_FILE = "vip.json"

app = Flask(__name__)
application = ApplicationBuilder().token(7696654212:AAFOHIeFVEx-izK7En5EJloXqbVRGLf1qPA).build()

# ---------------- VIP SYSTEM ----------------

def load_vip():
    try:
        with open(VIP_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_vip(data):
    with open(VIP_FILE, "w") as f:
        json.dump(data, f)

def is_vip(user_id):
    return user_id in load_vip()

# ---------------- BOT ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ahoj!\n"
        "💎 Tento bot má VIP systém.\n"
        "Použij /vip pro kontrolu."
    )

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_vip(user_id):
        await update.message.reply_text("💎 Máš VIP přístup!")
    else:
        await update.message.reply_text("❌ Nemáš VIP přístup.")

# ---------------- ADMIN ----------------

async def addvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Nemáš oprávnění.")
        return

    try:
        target = int(context.args[0])
        vip_list = load_vip()

        if target not in vip_list:
            vip_list.append(target)
            save_vip(vip_list)

        await update.message.reply_text("💎 VIP přidán.")
    except:
        await update.message.reply_text("Použití: /addvip ID")

# ---------------- MESSAGE ----------------

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_vip(user_id):
        await update.message.reply_text("💎 VIP odpověď: máš přístup k premium obsahu.")
    else:
        await update.message.reply_text("❌ Free verze. Upgraduj na VIP.")

# ---------------- WEBHOOK ----------------

@app.route(f"/7696654212:AAFOHIeFVEx-izK7En5EJloXqbVRGLf1qPA", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot běží 👍"

# ---------------- START ----------------

async def main():
    await application.initialize()
    await application.bot.set_webhook(f7696654212:AAFOHIeFVEx-izK7En5EJloXqbVRGLf1qPA)
    await application.start()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vip", vip))
    application.add_handler(CommandHandler("addvip", addvip))
    application.add_handler(MessageHandler(filters.TEXT, echo))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

    app.run(host="0.0.0.0", port=10000)
