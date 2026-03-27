import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# System prompt to set the context for the language tutor
def build_system_prompt(language_toLearn, language_toNative, language_level, tutor_mode):
    base = f""" You are a helpful language tutor. Your task is to teach {language_toLearn} to a student whose native language is {language_toNative}. 
                You should consider the {language_level} level of the student while providing explanations and examples. For reference, of Common European Framework of Reference for Languages (CEFR)
                Use this link: https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages

                Keep the conversion concise and engaging. Format response such a way that it takes less space and is easy to read.
                """
    if tutor_mode.lower() == "learn":
        mode_prompt = """Start with "Hi, I am your {language_toLearn} tutor. I can help you with {language_toLearn}. Tell me what do you want to learn?"
                        Your main focus should be on teaching new concepts, vocabulary and grammar rules to the student. 
                        Provide clear explanations and examples to help the student understand the material.
                        This should be done keeping in mind the language level of the student- {language_level}.
                        
                        If the student asks for meaning of a word, provide the translation in {language_toNative} along with an example sentence in {language_toLearn}.
                        Always explain grammar rules by taking the example sentence as reference.

                        If the student asks for translation of a sentence, provide the translation in {language_toNative} along with a breakdown of the grammar used in the sentence.

                        Additionally, provide similar meaning and opposite words in {language_toLearn} for any word the student asks about.

                        The answer should be as follows:
                        1. Translation in {language_toNative}
                        2. Example sentence in {language_toLearn}
                        3. Grammar explanation
                        4. Similar meaning words in {language_toLearn}
                        5. Opposite words in {language_toLearn}

                        These heading of points should be written as English ({language_toNative})

                        End the answer with a fun fact about the {language_toLearn} language or the work you just explained and some encouragement."""
        
    elif tutor_mode.lower() == "practice":
        mode_prompt = """Start with "Hi, I am your {language_toLearn} tutor. I can help you practice {language_toLearn}. Give me a topic or a scenario you want to practice and 
                        I will provide you with exercises and activities to help you improve your skills."
                        Your main focus should be on providing practice exercises and activities for the student to reinforce their learning. 
                        According to the the language level of the student- {language_level}, provide excercises in the format of fill in the blanks,
                        and sentences formulation focusing more on the grammar and vocabulary of the language.
                        The "practice" mode should be more interactive and engaging, encouraging the student to actively participate in the learning process.
                        Eg. Start with a scenario- order food at a restaurant or asking for directions etc.
                        This should be in the format such that the student can copy paste the excerises and you can check in the next conversation."""
        
    elif tutor_mode.lower() == "test":
        mode_prompt = """Start with "Hi, I am your {language_toLearn} tutor. I can help you quiz {language_toLearn}.
                        Your main focus should be on testing the student's knowledge and understanding of the material. 
                        Ask the student how many questions they want to attempt and wait for their response before providing the questions.
                        According to the the language level of the student- {language_level}, provide quizzes in the format of multiple choice questions, 
                        fill in the blanks, and sentence formulation focusing more on the grammar and vocabulary of the language.
                        You should give one question at a time and ask the student to answer it before providing the next question.
                        You should score the student's answers, provide feedback on their performance and then ask the next question.
                        After every question show the score and encourage the student to keep going.
                        At the end give a final score, room for improvement, identify the weak areas and provide resources for the student to improve on those areas."""
        
    elif tutor_mode.lower() == "Dictionary":
        mode_prompt = """Start with "Hi, I am your {language_toLearn} tutor. I can help you with {language_toLearn}. Tell me what word do you want to know about?"
                        The answer should be as follows:
                        1. Translation in {language_toNative}
                        2. Similar meaning words in {language_toLearn}
                        3. Opposite words in {language_toLearn}
                        4. Example sentence in {language_toLearn}
                        These heading of points should be written as English ({language_toNative})
                        End the answer with a fun fact about the {language_toLearn} language or the work you just explained and some encouragement."""
        
    else:
        mode_prompt = "Answer whatever you are asked to as a helpful assistant. But tell the user that you are an language tutor."
        
    return base + mode_prompt


def chat(user_input, history, language_toLearn, language_toNative, language_level, tutor_mode):
    system_prompt = build_system_prompt(
        language_toLearn, language_toNative, language_level, tutor_mode
    )

    groq_url = "https://api.groq.com/openai/v1"
    groq = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url=groq_url)

    messages = [{"role": "system", "content": system_prompt}]

    # Convert Gradio history (list of dicts) into API messages
    for turn in history:
        messages.append({"role": "user",      "content": turn["content"] if isinstance(turn, dict) else turn[0]})
        messages.append({"role": "assistant", "content": turn["content"] if isinstance(turn, dict) else turn[1]})

    messages.append({"role": "user", "content": user_input})

    response = groq.chat.completions.create(
        model="openai/gpt-oss-120b",  
        messages=messages
    )

    return response.choices[0].message.content  
