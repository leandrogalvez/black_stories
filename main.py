from dotenv import load_dotenv
from openai import OpenAI
import os
import json
load_dotenv()

print("Sus vacaciones no fueron tan buenas para su salud")

client = OpenAI(api_key=os.environ.get("OPENAI_KEY",""))
#preguntas = 'the player has guessed the location of the story?': 'True or False'
#        'the player has guessed that the guy had a scar?: 'True or False'
#        'the player has guessed why did the guy have a scar?: 'True or False'
#        'the player has guessed that the guy was in a taxi?: 'True or False'
#        'the player has guessed that the guy was unconscious?: 'True or False'
#        'the player has guessed who knocked the guy unconscious?: 'True or False']

prompt = """
    You are the narrator of a table game where the players have to guess what happened
    only with yes or no questions and you need to answer them.
    This is the story: 
    <story>
    Un hombre de vacaciones en un país tropical paró un taxi
    y el conductor lo dejó inconsciente. Cuando el hombre despertó en mitad de la noche,
    se encontró fuera de la ciudad con un cicatriz fresca en la espalda. De vuelta a casa,
    sus perores terrores se confirmaron: su riñón izquierdo había sido robado.
    </story>
    Your answer has to be a json with this characteristics:
    <responses_template>
    {
        'reasoning of the question': 'a string that justifies why the question can be answered with a yes or a no'
        'can be answered the question with a yes or a no?': 'True or False'
        'reasoning of the answer': 'a string that justifies why the answer is yes or no'
        'answer to the question': 'true or false'
    }
    </response_template>
    <question_example>
    the guy was in a tropical country?
    </question_example>
    <response_example>
    {
        'reasoning of the question': 'can be answered with yes or no because it does not ask for a specific detail, only whether I was in that place and does not require details.'
        'can be answered the question with a yes or a no?': 'true'
        'reasoning of the answer': 'the answer is yes because in the story says that the man was in a tropical country'
        'answer to the question': 'true'
    }
    </response_example>
    <question2_example>
    what happened to him?
    </question2_example>
    <response2_example>
    {
        'reasoning of the question': 'the question can't be answered with a yes or a no because it is asking what happened to him'
        'can be answered the question with a yes or a no?': 'false'
        'reasoning of the answer': 'the answer is no because it can't be answered with a yes or a no'
        'answer to the question': 'can't be answered with yes or no, make another question'
    }
    </response2_example>

"""
questions = []
prompt_2 = """
    el usuario pregunta: {pregunta}
"""
hitos = {
    'hito_1': 'the player has guessed the location of the story?',
    'hito_2': 'the player has guessed that the guy had a scar?',
    'hito_3': 'the player has guessed why did the guy have a scar?',
    'hito_4': 'the player has guessed that the guy was in a taxi?',
    'hito_5': 'the player has guessed that the guy was unconscious?',
    'hito_6': 'the player has guessed who knocked the guy unconscious?',
}

prompt_3 = """
    you are the narrator of a game table and you have to say whether a part of the story
    has been discovered or not with these landmarks:
    landmarks = {
    'hito_1': 'the player has guessed the location of the story?',
    'hito_2': 'the player has guessed that the guy had a scar?',
    'hito_3': 'the player has guessed why did the guy have a scar?',
    'hito_4': 'the player has guessed that the guy was in a taxi?',
    'hito_5': 'the player has guessed that the guy was unconscious?',
    'hito_6': 'the player has guessed who knocked the guy unconscious?',
    }
    This is the story:
    <story>
    Un hombre de vacaciones en un país tropical paró un taxi
    y el conductor lo dejó inconsciente. Cuando el hombre despertó en mitad de la noche,
    se encontró fuera de la ciudad con un cicatriz fresca en la espalda. De vuelta a casa,
    sus perores terrores se confirmaron: su riñón izquierdo había sido robado.
    </story>
    your answer has to be a json like this:
    <response_template>
    {
        'landmark_reasoning': 'a string that justifies why that landmark has been discovered'
        'hito_(number)': 'true or false'
    }
    </response_template>

    <question_example>
    the guy was in a tropical country?
    </question_example>
    <response_example>
    {
        'landmark_reasoning': 'as the player have asked if he was in a tropical country,
        he already knows where the story takes place'
        'hito_1': true
    }
    </response_example>

    if most of the landmarks have been discovered, tell the story to the user

"""

pregunta = input('Pregunta algo: ')
questions.append(pregunta)
mensajes = [{"role": "system", "content": prompt},
        {"role": "user", "content": prompt_2}]

mensajes2 = [{"role": "system", "content": prompt_3},
        {"role": "user", "content": prompt_2}]


while True:
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo-1106",
        response_format = {"type": "json_object"},
        messages=mensajes,
        )
    response = json.loads(completion.choices[0].message.content)

    print(response)
    mensajes.append({"role": "system", "content": prompt_2})
    mensajes.append({"role": "user", "content": input("Pregunta algo: ")})


