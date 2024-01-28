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
        'reasoning of the question': 'puede ser respondida con un si o no porque no pregunta por un detalle en concreto, solo si estaba en ese lugar y no requiere detalles'
        'can be answered the question with a yes or a no?': 'true'
        'reasoning of the answer': 'the answer is yes because in the story says that the man was in a tropical country'
        'answer to the question': 'true'
    }
    </response_example>
    <question2_example>
    the guy was in a tropical country?
    </question2_example>
    <response2_example>
    {
        'reasoning of the question': 'puede ser respondida con un si o no porque no pregunta por un detalle en concreto, solo si estaba en ese lugar y no requiere detalles'
        'can be answered the question with a yes or a no?': 'true'
        'reasoning of the answer': 'the answer is yes because in the story says that the man was in a tropical country'
        'answer to the question': 'true'
    }
    </response_example>

"""
questions = []
prompt_2 = """
    el usuario pregunta: {pregunta}
"""
pregunta = input('Pregunta algo: ')
questions.append(pregunta)
mensajes = [{"role": "system", "content": prompt},
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

