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

# Dictionary of symptoms and predefined responses
symptoms_responses = {
    "knee pain": "It sounds like you're experiencing knee pain. Here are a few things you might consider: rest, ice, compression, and elevation. However, please consult a healthcare professional for a proper diagnosis and treatment.",
    "headache": "For a headache, ensure you're staying hydrated, resting in a dark, quiet room, and taking over-the-counter pain relievers if needed. However, please consult a healthcare professional for a proper diagnosis and treatment.",
    "stomach ache": "For a stomach ache, you might try drinking clear fluids, avoiding solid foods, and resting. However, please consult a healthcare professional for a proper diagnosis and treatment."
}

questions = {
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

def get_next_question(state):
    for key in questions:
        if key not in state:
            return key, questions[key]
    return None, "Thank you for providing all the information. Based on what you've told me, here's some advice:"

def getResponse(state, user_input):
    user_input_lower = user_input.lower()  # Convert user input to lowercase for matching

    # Check if the user input matches any predefined symptom
    for symptom in symptoms_responses:
        if symptom in user_input_lower:
            return symptoms_responses[symptom], state

    if not state or state.get("step") == "start":
        state = {"step": "Background"}
        ai_response = questions["Background"]
    else:
        state[state["step"]] = user_input
        next_step, question = get_next_question(state)
        if next_step:
            state["step"] = next_step
            ai_response = question
        else:
            # Generate medical advice based on the collected information
            advice_prompt = (
                "Based on the following information, provide general medical advice:\n"
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
                state["step"] = "end"
            except Exception as e:
                logging.error(f"Error calling OpenAI API: {e}")
                ai_response = "Error: Unable to get response from server. Please try again later."

    return ai_response, state

