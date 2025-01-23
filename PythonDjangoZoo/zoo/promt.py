from decouple import config

async def create_promt(system_text: str = "", user_text: str = ""):
    return {
        "modelUri": f"gpt://{config('ya_catalog_key')}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": system_text
            },
            {
                "role": "user",
                "text": user_text
            }
        ]
    }