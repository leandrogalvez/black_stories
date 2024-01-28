from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_KEY",""))


prompt_2 = """
    eres un narrador de un juego de mesa de adivinar una historia y 
    te van a hacer preguntas para intentar adivinarla.
    Esta es la historia: Un hombre de vacaciones en uun país tropical paró un taxi
    y el conductor lo dejó inconsciente. Cuando el hombre despertó en mitad de la noche,
    se encontró fuera de la ciudad con un cicatriz fresca en la espalda. De vuelta a casa,
    sus perores terrores se confirmaron: su riñón izquierdo había sido robado.

    First of all you have to tell the player only this: 
    Sus vacaciones no fueron tan buenas para su salud

    The question can only be a yes or no question:
    {
        'pregunta': {pregunta}
    }
    Your answer has to be a yes or no question.
    if the question has a diferent answer than yes or no, you have to tell the player
    to ask again. Your answer has to be a json with this characteristics:
    {
        '{pregunta} can be answered with a yes or a no?': 'True or False'
        '{answer}': 'si or no'
    }


"""
mensajes = [{"role": "system", "content": prompt_2},
        {"role": "user", "content": input('Pregunta algo: ')}]

while True:
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=mensajes
        )
    print(completion.choices[0].message.content)
    mensajes.append({"role": "system", "content": prompt_2})
    mensajes.append({"role": "user", "content": input("Pregunta algo: ")}) 


