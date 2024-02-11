from dotenv import load_dotenv
from openai import OpenAI
import os
import json
load_dotenv()
from chat import Chat

print("Sus vacaciones no fueron tan buenas para su salud")

client = OpenAI(api_key=os.environ.get("OPENAI_KEY",""))

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
        'can be answered the question with a yes or a no?': True or False
        'reasoning of the answer': 'a string that justifies why the answer is yes or no'
        'answer to the question': True or False
    }
    </response_template>
    <question_example>
    the guy was in a tropical country?
    </question_example>
    <response_example>
    {
        'reasoning of the question': 'can be answered with yes or no because it does not ask for a specific detail, only whether I was in that place and does not require details.'
        'can be answered the question with a yes or a no?': True
        'reasoning of the answer': 'the answer is yes because in the story says that the man was in a tropical country'
        'answer to the question': True
    }
    </response_example>
    <question2_example>
    what happened to him?
    </question2_example>
    <response2_example>
    {
        'reasoning of the question': 'the question can't be answered with a yes or a no because it is asking what happened to him'
        'can be answered the question with a yes or a no?': False
        'reasoning of the answer': 'the answer is no because it can't be answered with a yes or a no'
        'answer to the question': 'can't be answered with yes or no, make another question'
    }
    </response2_example>

"""

hitos = {
    'hito_1': False,
    'hito_2': False,
    'hito_3': False,
    'hito_4': False,
    'hito_5': False,
}

prompt_2 = """
    you are the narrator of a game table and you have to say whether a part of the story
    has been discovered or not following these landmarks:
    landmarks = {
    'hito_1': 'the player knows that the story takes place in a tropical country',
    'hito_2': 'the player knows that the guy had a scar',
    'hito_3': 'the player knows that the guy had a scar because he had a kidney stolen',
    'hito_4': 'the player knows that the guy was in a taxi',
    'hito_5': 'the player knows that the guy was unconscious',
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
        'landmarks': {
            'hito_1': 'true or false'
            'hito_2': 'true or false'
            'hito_3': 'true or false'
            'hito_4': 'true or false'
            'hito_5': 'true or false'
            }
    }
    </response_template>

    <question_example>
    the guy was in a tropical country?
    </question_example>

    <response_example>
    {
        'landmark_reasoning': 'as the player have asked if he was in a tropical country,
        he already knows where the story takes place'
        'landmarks':{
            'hito_1': true
            'hito_2': false
            'hito_3': false
            'hito_4': false
            'hito_5': false
            }
    }
    </response_example>

    <question2_example>
    was riding a bicycle?
    </question2_example>

    <response2_example>
    {
        'landmark_reasoning': 'he doesnt discover anything important acording to the landmarks'
        'landmarks': {
            'hito_1': false
            'hito_2': false
            'hito_3': false
            'hito_4': false
            'hito_5': false
            }
    }
    </response2_example>

    <question3_example>
    got into a taxi and was knocked unconscious?
    </question3_example>

    <response3_example>
    {
        'landmark_reasoning': 'as the player has asked if he got into a taxi, he has discovered
        hito_4 and he has asked too if he was knocked unconscious so he has discovered hito_5'
        'landmarks': {
            'hito_1': false
            'hito_2': false
            'hito_3': false
            'hito_4': true
            'hito_5': true
            }
    }
    </response3_example>

"""

chat = Chat(prompt)
chat2 = Chat(prompt_2)
while True:
    pregunta = input("introduce una pregunta: ")
    res1 = chat.send_message_json(pregunta)
    if res1["answer to the question"] == True:
        print("yes")
    else:
        print(res1["answer to the question"])
    if res1["can be answered the question with a yes or a no?"] == True:
        res2 = chat2.send_message_json(pregunta)
        landmarks = res2['landmarks']
        for key, ans in landmarks.items():
            if ans:
                hitos[key] = True
    valores_true = sum(hitos.values())
    if valores_true >= 4:
        print("Enhorabuena has adivinado lo que ocurrió. Esta es la historia: Un hombre de vacaciones en un país tropical paró un taxi y el conductor lo dejó inconsciente. Cuando el hombre despertó en mitad de la noche, se encontró fuera de la ciudad con un cicatriz fresca en la espalda. De vuelta a casa, sus perores terrores se confirmaron: su riñón izquierdo había sido robado.")


