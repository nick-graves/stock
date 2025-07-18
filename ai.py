import requests
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()



def summarize_with_ollama(text, model="llama3.1:8b"):
    prompt = (
        "You are an analyst tasked with summarizing information gathered from multiple web pages "
        "about a specific Exchange-Traded Fund (ETF). The text below contains scraped content from the top 5 websites "
        "related to this ETF, limited to the first 10,000 characters. Some content may be repetitive or noisy.\n\n"
        "Please provide:\n"
        "1. A brief but accurate **overview** of what the ETF is and what it invests in.\n"
        "2. A bullet-point list of **key information**, such as top holdings, sector focus, fees, performance highlights, "
        "associated risks, or any notable features mentioned.\n"
        "3. Ignore unrelated or low-quality content.\n\n"
        "4. Please respond only in plaintext. No markdown formatting\n\n"
        "Scraped Text:\n"
        f"{text}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        raise RuntimeError(f"Ollama API error: {response.status_code} - {response.text}")
    


def summarize_with_gemini(text):
    prompt = (
        "You are an analyst tasked with summarizing information gathered from multiple web pages "
        "about a specific Exchange-Traded Fund (ETF). The text below contains scraped content from the top 5 websites "
        "related to this ETF, limited to the first 10,000 characters. Some content may be repetitive or noisy.\n\n"
        "Please provide:\n"
        "1. A brief but accurate **overview** of what the ETF is and what it invests in.\n"
        "2. A bullet-point list of **key information**, such as top holdings, sector focus, fees, performance highlights, "
        "associated risks, or any notable features mentioned.\n"
        "3. Ignore unrelated or low-quality content.\n\n"
        "4. Please respond only in plaintext. No markdown formatting\n\n"
        "Scraped Text:\n"
        f"{text}"
    )

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
    
    return response.text
