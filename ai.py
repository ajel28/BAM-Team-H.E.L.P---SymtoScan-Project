# from openai import AzureOpenAI
# from secret import *
# import logging

# ENDPOINT = AZURE_OPENAI_ENDPOINT
# KEY = AZURE_OPENAI_API_KEY
# MODEL = "gpt-35-turbo"

# openai_client = AzureOpenAI(
#     api_key=KEY,
#     azure_endpoint=ENDPOINT,
#     api_version="2024-05-01-preview"
# )

# # Initial questions based on BOLDCART framework
# initial_questions = {
#     "Background": "Can you tell me a bit about your medical history?",
#     "Onset": "When did the symptoms start?",
#     "Location": "Where exactly is the pain located?",
#     "Duration": "How long have you been experiencing these symptoms?",
#     "Character": "Can you describe the nature of the pain?",
#     "Aggravating": "Is there anything that makes it worse?",
#     "Relieving": "Is there anything that makes it better?",
#     "Timing": "Is there a specific time of day or activity when the symptoms are worse?",
#     "Severity": "On a scale of 1 to 10, how severe is the pain?"
# }

# def generate_question(state, user_input):
#     primary_symptom = state.get("primary_symptom", "your condition")
    
#     prompt = (
#         "You are a highly knowledgeable medical assistant. Based on the following information and the user's previous response, generate a concise question that fits within the BOLDCART framework "
#         "to gather more detailed information about the primary symptom ({primary_symptom}).\n"
#         "Do not include introductory phrases, just ask the question.\n"
#         f"Primary symptom: {primary_symptom}\n"
#         f"User's previous response: {user_input}\n"
#         f"State: {state}\n"
#         "Ask a question that fits into the next BOLDCART category and is relevant to the user's previous response."
#     )
    
#     try:
#         response = openai_client.chat.completions.create(
#             model=MODEL,
#             messages=[
#                 {"role": "system", "content": "You are a highly knowledgeable medical assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         logging.error(f"Error calling OpenAI API: {e}")
#         return "Error: Unable to generate a question at this time. Please try again later."

# def getResponse(state, user_input):
#     user_input_lower = user_input.lower()  # Convert user input to lowercase for matching

#     if not state or state.get("step") == "start":
#         state = {"step": "Background", "primary_symptom": user_input}
#         ai_response = initial_questions["Background"]
#     else:
#         state[state["step"]] = user_input
#         next_step, question = get_next_question(state)
#         if next_step:
#             state["step"] = next_step
#             ai_response = generate_question(state, user_input)
#         else:
#             # Generate medical advice based on the collected information
#             advice_prompt = (
#                 "Based on the following information, provide general medical advice for the primary symptom ({primary_symptom}):\n"
#                 f"Background: {state.get('Background', '')}\n"
#                 f"Onset: {state.get('Onset', '')}\n"
#                 f"Location: {state.get('Location', '')}\n"
#                 f"Duration: {state.get('Duration', '')}\n"
#                 f"Character: {state.get('Character', '')}\n"
#                 f"Aggravating: {state.get('Aggravating', '')}\n"
#                 f"Relieving: {state.get('Relieving', '')}\n"
#                 f"Timing: {state.get('Timing', '')}\n"
#                 f"Severity: {state.get('Severity', '')}\n"
#                 "Provide advice but always remind the user to consult with a healthcare professional for proper diagnosis and treatment."
#             )
#             advice_prompt = advice_prompt.format(primary_symptom=state.get("primary_symptom", "your condition"))
#             try:
#                 response = openai_client.chat.completions.create(
#                     model=MODEL,
#                     messages=[
#                         {"role": "system", "content": "You are a highly knowledgeable medical assistant."},
#                         {"role": "user", "content": advice_prompt}
#                     ],
#                     max_tokens=1000
#                 )
#                 ai_response = response.choices[0].message.content
#                 state["step"] = "end"
#             except Exception as e:
#                 logging.error(f"Error calling OpenAI API: {e}")
#                 ai_response = "Error: Unable to get response from server. Please try again later."

#     return ai_response, state

# def get_next_question(state):
#     for key in initial_questions:
#         if key not in state:
#             return key, initial_questions[key]
#     return None, "Thank you for providing all the information. Based on what you've told me, here's some advice:"

from openai import AzureOpenAI
from secret import *
import logging

ENDPOINT = AZURE_OPENAI_ENDPOINT
KEY = AZURE_OPENAI_API_KEY
MODEL = "gpt-35-turbo"

openai_client = AzureOpenAI(
    api_key=KEY,
    azure_endpoint=ENDPOINT,
    api_version="2024-05-01-preview"
)

# Initial questions based on BOLDCART framework
initial_questions = {
    "Background": "Can you tell me a bit about your medical history?",
    "Onset": "When did the symptoms start?",
    "Location": "Where exactly is the pain located?",
    "Duration": "How long have you been experiencing these symptoms?",
    "Character": "Can you describe the nature of the pain?",
    "Aggravating": "Is there anything that makes it worse?",
    "Relieving": "Is there anything that makes it better?",
    "Timing": "Is there a specific time of day or activity when the symptoms are worse?",
    "Severity": "On a scale of 1 to 10, how severe is the pain?"
}

def translate_text(text, target_language):
    translation_prompt = f"Translate the following text to {target_language}:\n{text}"
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a highly skilled translator."},
                {"role": "user", "content": translation_prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error calling OpenAI API for translation: {e}")
        return "Error: Unable to translate text at this time."

def generate_question(state, user_input, language):
    primary_symptom = state.get("primary_symptom", "your condition")
    
    prompt = (
        "You are a highly knowledgeable medical assistant. Based on the following information and the user's previous response, generate a concise question that fits within the BOLDCART framework "
        "to gather more detailed information about the primary symptom ({primary_symptom}).\n"
        "Do not include introductory phrases, just ask the question.\n"
        f"Primary symptom: {primary_symptom}\n"
        f"User's previous response: {user_input}\n"
        f"State: {state}\n"
        "Ask a question that fits into the next BOLDCART category and is relevant to the user's previous response."
    )
    
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a highly knowledgeable medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        question = response.choices[0].message.content
        if language != "en":
            question = translate_text(question, language)
        return question
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Error: Unable to generate a question at this time. Please try again later."

def getResponse(state, user_input, language):
    user_input_lower = user_input.lower()  # Convert user input to lowercase for matching

    if not state or state.get("step") == "start":
        state = {"step": "Background", "primary_symptom": user_input}
        ai_response = initial_questions["Background"]
    else:
        state[state["step"]] = user_input
        next_step, question = get_next_question(state)
        if next_step:
            state["step"] = next_step
            ai_response = generate_question(state, user_input, language)
        else:
            # Generate medical advice based on the collected information
            advice_prompt = (
                "Based on the following information, provide general medical advice for the primary symptom ({primary_symptom}):\n"
                f"Background: {state.get('Background', '')}\n"
                f"Onset: {state.get('Onset', '')}\n"
                f"Location: {state.get('Location', '')}\n"
                f"Duration: {state.get('Duration', '')}\n"
                f"Character: {state.get('Character', '')}\n"
                f"Aggravating: {state.get('Aggravating', '')}\n"
                f"Relieving: {state.get('Relieving', '')}\n"
                f"Timing: {state.get('Timing', '')}\n"
                f"Severity: {state.get('Severity', '')}\n"
                "Provide advice but always remind the user to consult with a healthcare professional for proper diagnosis and treatment."
            )
            advice_prompt = advice_prompt.format(primary_symptom=state.get("primary_symptom", "your condition"))
            try:
                response = openai_client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are a highly knowledgeable medical assistant."},
                        {"role": "user", "content": advice_prompt}
                    ],
                    max_tokens=300
                )
                ai_response = response.choices[0].message.content
                if language != "en":
                    ai_response = translate_text(ai_response, language)
                state["step"] = "end"
            except Exception as e:
                logging.error(f"Error calling OpenAI API: {e}")
                ai_response = "Error: Unable to get response from server. Please try again later."

    if language != "en":
        ai_response = translate_text(ai_response, language)

    return ai_response, state

def get_next_question(state):
    for key in initial_questions:
        if key not in state:
            return key, initial_questions[key]
    return None, "Thank you for providing all the information. Based on what you've told me, here's some advice:"
