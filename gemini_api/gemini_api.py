from google import generativeai as genai
from retrieve_reccomendations.retrieve_major_minor_rec import choose_degree_of_interests
import json
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into the environment

# Access them
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)

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

        match chat_branch_state:
            case "Initial State":
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

            case "Initial Clarification":
                text = "Sorry, I had trouble processing that. Try again!"
                new_chat_branch_state = "Initial State"
            
            case "Individual Class":
                system_instruction = """
                    You are a classifier.
                    You will return two parts strictly formatted with a comma in between.
                    
                    Part 1:
                    You will return a strictly formatted list like in Python of the following categories, nothing else.
                    They will describe themselves, and you will return at least 3 (more if possible) categories that align with their interests. MAKE SURE IT IS ONLY THESE CATEGORIES YOU RETURN AND STRICTLY FORMATTED:

                    'Nutrition', 'South America', 'Pop Culture', 'Legal Issues', 'Teaching',
                    'Journalism', 'Sustainability', 'Finance', 'Nature', 'Conflict Resolution',
                    'Video Games', 'Math', 'Human Behavior', 'Literature', 'Crafts', 'Technology',
                    'Movies', 'Fitness', 'Forensics', 'Central America', 'Language', 'Science',
                    'Marketing', 'Asia', 'Fashion', 'Business', 'Music', 'Philosophy', 'History',
                    'Internet', 'Children', 'Travel', 'Media', 'Photography', 'Design',
                    'Environment', 'Food', 'Security', 'Religion', 'Sports', 'Healthcare',
                    'Data Analysis', 'Helping People', 'Performance', 'North America', 'Animals',
                    'Management', 'Programming', 'Art', 'Writing', 'Leadership'

                    Part 2:
                    They should also mention a gened they need to fulfill or multiple. Return them strictly formatted like a Python list is declared.
                    The codes are AH, SH, WC, NS, WL, EC, NM, MM, and only these.
                    Only pick from here: AH (this is for arts and humanities), SH (this is for social and historical sciences), WC (this is for world cultures), NS (this is for natural sciences), WL (this is for world languages), EC (this is for English composition), NM (this is for natural and mathematical sciences), MM (this is for mathematical modeling), and only these.
                    Keep in mind if they say natural and mathematical, that does not also mean natural science and vice versa.

                    If either part is not present, return -1.
                """

                response_text = await get_model_response(system_instruction, input_text)
                text = response_text
                new_chat_branch_state = "Final State"

            case "Class Scheduling":
                system_instruction = """
                    You are a classifier.
                    you strictly will only return a number with no other text. No whitespace, no text.
                    You will return 1 if they state or imply they take accounting
                    If not, even if it is business and not accounting return -1.
                """

                response_text = await get_model_response(system_instruction, input_text)
                text = response_text
                if response_text == "1":
                    new_chat_branch_state = "Final State"
                else:
                    text = "Sorry, I had trouble processing that. As of now only the data for accounting is fully available. Try again!"

            case "Majors":
                system_instruction = """
                    You are a classifier.
                    You will return two parts strictly formatted with a comma in between.
                    You will return a strictly formatted list like in Python of the following categories, nothing else, no commas or whitespace before or after. The response should start and end with brackets. CLOSE THE STRINGS IN DOUBLE QUOTES ONLY.
                    They will describe themselves, and you will return at least 3 (more if possible) categories that align with their interests. MAKE SURE IT IS ONLY THESE CATEGORIES YOU RETURN AND STRICTLY FORMATTED:

                    "Nutrition", "South America", "Pop Culture", "Legal Issues", "Teaching",
                    "Journalism", "Sustainability", "Finance", "Nature", "Conflict Resolution",
                    "Video Games", "Math", "Human Behavior", "Literature", "Crafts", "Technology",
                    "Movies", "Fitness", "Forensics", "Central America", "Language", "Science",
                    "Marketing", "Asia", "Fashion", "Business", "Music", "Philosophy", "History",
                    "Internet", "Children", "Travel", "Media", "Photography", "Design",
                    "Environment", "Food", "Security", "Religion", "Sports", "Healthcare",
                    "Data Analysis", "Helping People", "Performance", "North America", "Animals",
                    "Management", "Programming", "Art", "Writing", "Leadership"

                    If nothing is related to them, return -1.
                """

                response_text = await get_model_response(system_instruction, input_text)
                print("Gemini response:", response_text)

                try:
                    suggested_majors = choose_degree_of_interests("majors", json.loads(response_text),)
                    print("Suggested Majors:", suggested_majors)

                    system_instruction_summary = """
                        You will sum up why a major is good for them based on their interests and the majors they are interested in. Here is the data:
                    """

                    summary_response = await get_model_response(system_instruction_summary, json.dumps(suggested_majors))
                    text = summary_response.strip()

                except Exception as e:
                    print("Error processing majors:", e)
                    text = "Sorry, something went wrong while processing your interests."

                new_chat_branch_state = "Final State"
            case "Minors":
                system_instruction = """
                    You are a classifier.
                    You will return two parts strictly formatted with a comma in between.
                    You will return a strictly formatted list like in Python of the following categories, nothing else, no commas or whitespace before or after. The response should start and end with brackets. CLOSE THE STRINGS IN DOUBLE QUOTES ONLY.
                    They will describe themselves, and you will return at least 3 (more if possible) categories that align with their interests. MAKE SURE IT IS ONLY THESE CATEGORIES YOU RETURN AND STRICTLY FORMATTED:

                    "Nutrition", "South America", "Pop Culture", "Legal Issues", "Teaching",
                    "Journalism", "Sustainability", "Finance", "Nature", "Conflict Resolution",
                    "Video Games", "Math", "Human Behavior", "Literature", "Crafts", "Technology",
                    "Movies", "Fitness", "Forensics", "Central America", "Language", "Science",
                    "Marketing", "Asia", "Fashion", "Business", "Music", "Philosophy", "History",
                    "Internet", "Children", "Travel", "Media", "Photography", "Design",
                    "Environment", "Food", "Security", "Religion", "Sports", "Healthcare",
                    "Data Analysis", "Helping People", "Performance", "North America", "Animals",
                    "Management", "Programming", "Art", "Writing", "Leadership"

                    If nothing is related to them, return -1.
                """

                response_text = await get_model_response(system_instruction, input_text)
                print("Gemini response:", response_text)

                try:
                    suggested_majors = choose_degree_of_interests("minors", json.loads(response_text),)
                    print("Suggested Minors:", suggested_majors)

                    system_instruction_summary = """
                        You will sum up why a minor is good for them based on their interests and the majors they are interested in. Here is the data:
                    """

                    summary_response = await get_model_response(system_instruction_summary, json.dumps(suggested_majors))
                    text = summary_response.strip()

                except Exception as e:
                    print("Error processing majors:", e)
                    text = "Sorry, something went wrong while processing your interests."

                new_chat_branch_state = "Final State"

            case _:
                text = ""
                new_chat_branch_state = "Initial State"

        return text, new_chat_branch_state

    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong.", "Initial State"

# ✅ Run the async function and print output
response = asyncio.run(get_bot_response("Hi i want to schedule all my classes?", "Initial State"))
print("Bot:", response[0])
print("New State:", response[1])
response = asyncio.run(get_bot_response("my major is accounting!!!", response[1]))
print("Bot:", response[0])
print("New State:", response[1])
