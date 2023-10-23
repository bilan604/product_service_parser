import os
import time
import openai
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_gpt_3_5_result(prompt, model_version="gpt-3.5-turbo-16k"):
    message=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
                model=model_version,
                messages=message,
                temperature=0.5,
                max_tokens=1000,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
        return response
    except Exception as e:
        if isinstance(e, openai.error.RateLimitError):
            print("Sleeping for 60 seconds due to OpenAI prompting rate limit")
            time.sleep(60)
            response = openai.ChatCompletion.create(
                model=model_version,
                messages=message,
                temperature=0.5,
                max_tokens=1000,
                frequency_penalty=0.0
            ).choices[0].message.content.strip()
            return response
        print("Error occured on OpenAI API call:", str(e))
        return None

