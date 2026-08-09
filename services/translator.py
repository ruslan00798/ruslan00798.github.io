import asyncio
from deep_translator import GoogleTranslator



MAX_LENGTH = 4500



def split_text(
    text: str,
    size: int = MAX_LENGTH
):

    parts = []

    while len(text) > size:

        index = text.rfind(
            " ",
            0,
            size
        )

        if index == -1:
            index = size


        parts.append(
            text[:index]
        )


        text = text[index:]


    parts.append(
        text
    )


    return parts



async def translate(
    text: str,
    language: str
):

    if not text.strip():

        return ""


    try:

        translator = GoogleTranslator(
            source="auto",
            target=language
        )


        parts = split_text(
            text
        )


        translated_parts = []


        for part in parts:

            result = await asyncio.to_thread(
                translator.translate,
                part
            )


            translated_parts.append(
                result
            )


        return "\n".join(
            translated_parts
        )



    except Exception as error:

        print(
            "Ошибка Google Translator:",
            error
        )


        return (
            "❌ Не удалось выполнить перевод.\n"
            "Попробуйте позже."
        )



# Добавление харакатов арабскому тексту
def add_harakat_simple(
    text: str
):

    return text


