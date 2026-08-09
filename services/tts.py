import edge_tts
import tempfile
import os



VOICES = {

    "en": "en-US-JennyNeural",

    "ru": "ru-RU-SvetlanaNeural",

    "de": "de-DE-ConradNeural",

    "fr": "fr-FR-DeniseNeural",

    "es": "es-ES-ElviraNeural",

    "it": "it-IT-ElsaNeural",

    "ar": "ar-SA-HamedNeural",

    "ja": "ja-JP-NanamiNeural",

    "ko": "ko-KR-SunHiNeural",

    "uk": "uk-UA-PolinaNeural"
}



def get_voice(
    language: str
):

    return VOICES.get(
        language,
        VOICES["en"]
    )



async def text_to_speech(
    text: str,
    voice: str
):

    if not text.strip():

        raise ValueError( "Пустой текст для озвучки")


    # Ограничение Edge TTS
    if len(text) > 3000:

        text = text[:3000]



    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )


    file_path = file.name

    file.close()



    try:

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice
        )


        await communicate.save(
            file_path
        )


        return file_path



    except Exception:

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )


        raise

async def generate_audio(text: str, language: str,) -> str:
    """
    Создаёт аудиофайл для текста
    на указанном языке.
    """ 

    voice = get_voice(language)

    return await text_to_speech(text=text, voice=voice,)  