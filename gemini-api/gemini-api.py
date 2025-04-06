from google import generativeai as genai
import asyncio

# ✅ Configure your Gemini API key
genai.configure(api_key="Lol")

# ✅ Create the Gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")


async def get_model_response(system_instruction, user_prompt):
    try:
        # ✅ Combine instruction and user prompt into one "user" message
        full_prompt = f"{system_instruction}\n\nUser request: {user_prompt}"

        # ✅ Generate content using the model
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": full_prompt}]}
            ]
        )

        # ✅ Extract and return the response text
        return response.text.strip()
    
    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong."
# ✅ Async function to get the bot response
async def get_bot_response(input_text, chat_branch_state):
    try:
        text = ""
        new_chat_branch_state = chat_branch_state

        if chat_branch_state == "Initial State":
            system_instruction = """
                You are a classifier. Return only a single number (and nothing else) based on the user's request:
                Return 1 if they want help finding a single class.
                Return 2 if they want help finding majors.
                Return 3 if they want help finding minors.
                Return 4 if they want to see information about a class, such as average GPA.
                Return 5 if they want help scheduling a full semester of classes for their major.
                Do not return 5 if they are only asking about scheduling an individual class.
                If they imply multiple things, do 5.
                Return -1 if they are asking about nothing related to the above, but only if absolutely not related.
                Do not explain your answer. Do not include any text. Just return the number.
            """

            response_text = await get_model_response(system_instruction, input_text)
            print("Gemini response:", response_text)

            match response_text:
                case "1":
                    text = "Great! I can help you find a single class. What are you looking for?"
                    new_chat_branch_state = "Class Scheduling"
                case "2":
                    text = "Awesome! I can help you find majors. What are you interested in?"
                    new_chat_branch_state = "Majors"
                case "3":
                    text = "Sure! I can help you find minors. What are you interested in?"
                    new_chat_branch_state = "Minors"
                case "4":
                    text = "Sure! I can provide information about a class, such as average GPA. Which class are you interested in?"
                    new_chat_branch_state = "Class Information"
                case "5":
                    text = "Sure! I can help you schedule a full semester of classes for your major. Which major are you interested in?"
                    new_chat_branch_state = "Class Scheduling"
                case "-1":
                    text = "Sorry, I had trouble processing that. Try again!"
                    new_chat_branch_state = "Initial State"
                case _:
                    text = "Sorry, I had trouble processing that. Try again!"
                    new_chat_branch_state = "Initial State"

        elif chat_branch_state == "Initial Clarification":
            text = "Sorry, I had trouble processing that. Try again!"
            new_chat_branch_state = "Initial State"

        elif chat_branch_state == "Class Scheduling":
            text = ""  # placeholder or future logic
            new_chat_branch_state = "Final State"

        else:
            text = ""
            new_chat_branch_state = "Initial State"

        return text, new_chat_branch_state

    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong.", "Initial State"

# ✅ Run the async function and print output
response = asyncio.run(get_bot_response("I want to take a class?", "Initial State"))
print("Bot:", response[0])
print("New State:", response[1])
