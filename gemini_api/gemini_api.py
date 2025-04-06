from google import generativeai as genai
from retrieve_reccomendations.retrieve_major_minor_rec import choose_degree_off_interests
from retrieve_reccomendations.schedulebuilder import schedule_build
import asyncio
from dotenv import load_dotenv
import os
import traceback
import json

load_dotenv()  # Loads variables from .env into the environment

# Access them
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key="")

# create the Gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")


async def get_model_response(system_instruction, user_prompt):
    try:
        # combine instruction and user prompt into one "user" message
        full_prompt = f"{system_instruction}\n\nUser request: {user_prompt}"

        # generate content using the model
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": full_prompt}]}
            ]
        )

        # Extract and return the response text
        return response.text.strip()

    except Exception as e:
        print("🔥 Error occurred:")
        traceback.print_exc()  # Prints full stack trace
        return "Sorry, something went wrong." + traceback.format_exc() + "Hello"
# async function to get the bot response
async def get_bot_response(input_text, chat_branch_state):
    try:
        text = ""
        new_chat_branch_state = chat_branch_state
        # Branches for chat conversation. Branch is determined via gemini
        match chat_branch_state:
            case "Initial State":
                system_instruction = """
                    You are a classifier. Return only a single number (and nothing else) based on the user's request:
                    Return 1 if they want help finding majors.
                    Return 2 if they want help finding minors.
                    Return 3 if they want help scheduling, choosing a semester, something related to that.
                    Return -1 if they are asking about nothing related to the above, but only if absolutely not related.
                    Do not explain your answer. Do not include any text. Just return the number.
                """

                response_text = await get_model_response(system_instruction, input_text)
                print("Gemini response:", response_text)

                match response_text:
                    case "1":
                        text = "Awesome! I can help you find majors. What are you interested in?"
                        new_chat_branch_state = "Majors"
                    case "2":
                        text = "Sure! I can help you find minors. What are you interested in?"
                        new_chat_branch_state = "Minors"
                    case "3":
                        print("We are scheduling")
                        text = "Sure! I can help you schedule a full semester of classes for your major. Which major are you interested in?"
                        new_chat_branch_state = "Class Scheduling"
                    case _:
                        text="Sorry, I had trouble understanding that. Could you be more clear"

            case "Initial Clarification":
                text = "Sorry, I had trouble understanding that. Could you be more clear"
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
                text = response_text + "<br><br>Now what would you like to do? As a reminder, you can ask me about majors, minors, or scheduling."
                new_chat_branch_state = "Initial State"

            case "Class Scheduling":
                system_instruction = """
                    You are a classifier.
                    you strictly will only return a number with no other text. No whitespace, no text.
                    You will return 1 if they state or imply they take accounting
                    If not, even if it is business and not accounting return -1.
                """

                response_text = await get_model_response(system_instruction, input_text)
                if response_text == "1":
                    new_chat_branch_state = "Class Scheduling Interests"
                    text = "Awesome! I can help you schedule a full semester of classes for your major. What are some of your interests and what is your current semester as a number? For instance Freshman Spring would be 2."
                else:
                    text = "Sorry, I had trouble processing that. As of now only the data for accounting is fully available. Try again!"

            case "Class Scheduling Interests":
                print("in class schedduling interests")
                system_instruction = """
                    You are a classifier.
                    you will return two parts as a python array strictly formatted strictly
                    the first part is the semester they are currently in -1. So if they say they are in their second semester, return 1.
                    Strictly just put this as a number

                    in the second part, you will return a strictly formatted list like in Python of the following categories, nothing else, no commas or whitespace before or after. The response should start and end with brackets. CLOSE THE STRINGS IN DOUBLE QUOTES ONLY.
                    They will describe themselves, and you will return at least 1 (more if possible) categories that align with their interests. MAKE SURE IT IS ONLY THESE CATEGORIES YOU RETURN AND STRICTLY FORMATTED:
                    "Nutrition", "South America", "Pop Culture", "Legal Issues", "Teaching",
                    "Journalism", "Sustainability", "Finance", "Nature", "Conflict Resolution",
                    "Video Games", "Math", "Human Behavior", "Literature", "Crafts", "Technology",
                    "Movies", "Fitness", "Forensics", "Central America", "Language", "Science",
                    "Marketing", "Asia", "Fashion", "Business", "Music", "Philosophy", "History",
                    "Internet", "Children", "Travel", "Media", "Photography", "Design",
                    "Environment", "Food", "Security", "Religion", "Sports", "Healthcare",
                    "Data Analysis", "Helping People", "Performance", "North America", "Animals",
                    "Management", "Programming", "Art", "Writing", "Leadership"

                    REMEMBER YOUR OUTPUT WILL START AND END WITH BRACKETS. NOTHING BEFORE OR AFTER strings will be in double quotes

                """
                response_text = await get_model_response(system_instruction, input_text)
                try:

                    # Parse the JSON string into a Python object
                    print(response_text)
                    parsed_response = json.loads(response_text)
                    print(parsed_response)


                    # Extract the semester and interests
                    cur_semester = parsed_response[0]  # First element is the semester
                    interests = parsed_response[1]     # Second element is the list of interests

                    print("Current Semester:", cur_semester)
                    print("Interests:", interests)
                    schedule_builder = schedule_build(interests, cur_semester)
                    print(schedule_builder)
                    system_instruction = """
                    You will return these classes in the schedule as a formatted list with the information associated with each.you can use <br> in there to make new line. if time is not listed just say it is asynchronous online
                        """
                    text = await get_model_response(system_instruction, str(schedule_builder))
                    text = text + "<br><br>Now what would you like to do? As a reminder, you can ask me about majors, minors, or scheduling."
                    new_chat_branch_state = "Initial State"



                except json.JSONDecodeError as e:
                    print("Error parsing response:", e)



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
                    suggested_majors = choose_degree_off_interests("majors", json.loads(response_text),)
                    print("Suggested Majors:", suggested_majors)

                    system_instruction_summary = """
                        You will sum up why each of these majors is good for a student (Same student for all) based off of these interests of their's which is listed with teach associated major
                        Put these as a list with <br> in between and return nothing before or after this list make sure each major is bolded
                    """

                    summary_response = await get_model_response(system_instruction_summary, json.dumps(suggested_majors))
                    text = summary_response.strip()

                except Exception as e:
                    print("Error processing majors:", e)
                    text = "Sorry, something went wrong while processing your interests."

                text = text + "<br><br>Now what would you like to do? As a reminder, you can ask me about majors, minors, or scheduling."
                new_chat_branch_state = "Initial State"
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
                    suggested_majors = choose_degree_off_interests("minors", json.loads(response_text),)
                    print("Suggested Minors:", suggested_majors)

                    system_instruction_summary = """
You will sum up why each of these minors is good for a student (Same student for all) based off of these interests of their's which is listed with teach associated minor
                        Put these as a list with <br> in between and return nothing before or after this list make sure each minor is bolded                  """

                    summary_response = await get_model_response(system_instruction_summary, json.dumps(suggested_majors))
                    text = summary_response.strip()

                except Exception as e:
                    print("Error processing majors:", e)
                    text = "Sorry, something went wrong while processing your interests."

                text = text + "<br><br>Now what would you like to do? As a reminder, you can ask me about majors, minors, or scheduling."
                new_chat_branch_state = "Initial State"

            case _:
                text = ""
                new_chat_branch_state = "Initial State"

        return text, new_chat_branch_state

    except Exception as e:
        print("🔥 Error occurred:")
        traceback.print_exc()  # Prints full stack trace
        return "Sorry, something went wrong." + traceback.format_exc() + "Hello"

