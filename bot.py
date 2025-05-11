import os
import tempfile
import subprocess
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("7403455823:AAFY5KY4qYhJFe8265CXhZhzQs843smRZc0")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a voice or audio file and I'll enhance it like Adobe Voice Enhancer!")

# Audio file handler
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.voice or update.message.audio
    if not file:
        await update.message.reply_text("Please send a valid voice or audio file.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, 'input.wav')
        output_path = os.path.join(tmpdir, 'output.wav')

        file_id = file.file_id
        tg_file = await context.bot.get_file(file_id)
        await tg_file.download_to_drive(file_path)

        await update.message.reply_text("Enhancing your voice, please wait...")

        # Call VoiceFixer (assumed already installed and available)
        try:
            subprocess.run(["voicefixer", "--input", file_path, "--output", output_path], check=True)
        except subprocess.CalledProcessError:
            await update.message.reply_text("Voice enhancement failed. Please try again later.")
            return

        await update.message.reply_audio(audio=InputFile(output_path), caption="Here is your enhanced audio!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))

    print("Bot is running...")
    app.run_polling()
                                 
