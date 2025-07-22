import fitz  # PyMuPDF
import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()
gemini_api_key  = os.getenv("GEMINI_KEY")
if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY not found in environment variables. "
                     "Please check your .env file or system environment.")
genai.configure(api_key=gemini_api_key)

MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)


def extract_text_from_uploaded_file(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc]), None
    except Exception as e:
        return "", f"❌ Error reading uploaded PDF: {e}"

def extract_text_from_path(path):
    try:
        doc = fitz.open(path)
        return "".join([page.get_text() for page in doc]), None
    except Exception as e:
        return "", f"❌ Error reading local PDF: {e}"

def summarize_with_gemini(text_to_summarize, max_output_tokens: int = 500):
    print("summerizer called")
    prompt = f"Please summarize the following text concisely:\n\n{text_to_summarize}"
    print(prompt)

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=0.7,
                top_p=0.9,
                top_k=40
            )
        )
        print(response)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return "❌ Gemini summarization failed."


# inp = f"""Chess is a board game for two players. It is an abstract strategy game that involves no hidden information and no elements of chance. It is played on a square board consisting of 64 squares arranged in an 8×8 grid. The players, referred to as "White" and "Black", each control sixteen pieces: one king, one queen, two rooks, two bishops, two knights, and eight pawns, with each type of piece having a different pattern of movement. An enemy piece may be captured (removed from the board) by moving one's own piece onto the square it occupies. The object of the game is to "checkmate" (threaten with inescapable capture) the enemy king. There are also several ways a game can end in a draw."""
# print(summarize_with_gemini(inp))