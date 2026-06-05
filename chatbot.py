from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load API key
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Create Gemini model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# Load NGO data
with open(
    "ngo_data.txt",
    "r",
    encoding="utf-8"
) as f:
    ngo_data = f.read()

# Store conversation history
chat_history = []

SYSTEM_PROMPT = """
You are the official AI Assistant for InAmigos Foundation.

Rules:
1. Answer ONLY using the NGO information provided.
2. Be professional and concise.
3. Do not invent information.
4. Use conversation history to understand follow-up questions.
5. If the answer is not found in the NGO information, reply exactly:
   'I could not find that information on the InAmigos Foundation website.'
"""

print("=" * 50)
print("      InAmigos Foundation AI Assistant")
print("=" * 50)
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    # Save user message
    chat_history.append(f"User: {user_input}")

    # Keep only recent history
    history_text = "\n".join(chat_history[-10:])

    prompt = f"""
{SYSTEM_PROMPT}

NGO Information:
{ngo_data}

Conversation History:
{history_text}

Current User Question:
{user_input}
"""

    try:
        response = model.generate_content(prompt)

        answer = response.text.strip()

        # Save bot response in memory
        chat_history.append(f"Bot: {answer}")

        print("\nBot:", answer)
        print()

        # Save conversation log
        with open(
            "chat_log.txt",
            "a",
            encoding="utf-8"
        ) as log:
            log.write(f"User: {user_input}\n")
            log.write(f"Bot: {answer}\n")
            log.write("-" * 50 + "\n")

    except Exception as e:

        error_message = str(e)

        if "429" in error_message:
            print(
                "\nBot: API quota exceeded. "
                "Please wait a while and try again."
            )

        else:
            print("\nError:", error_message)