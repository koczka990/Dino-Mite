import gradio as gr
import typing_extensions
import typing
import typing_extensions
import gradio as gr
import random
import google.generativeai as genai
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()
# api_key = os.getenv("API_KEY")

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are a professional math teacher who is an expert at basic level math such as addition and subtraction, who is an expert in creating exercises for students, in different topics, and tailoring them to their interests so they can immerse themselfs more in the learning process.",
)
chat = model.start_chat()

# Define class for child
class Child:
    def __init__(self, name, age, grade, interests):
        self.name = name
        self.age = age
        self.grade = grade
        self.interests = interests


# Define the schema for the mushroom response
class ChildSchema(typing_extensions.TypedDict):
    name: str
    age: int
    grade: int
    interests: str # TODO make this list[str]

class NotebookSchema(typing_extensions.TypedDict):
    exercise_number: int
    topic: str
    exercises: list[str]


# global child object to save attributes
child = Child("John", 10, 5, "Dinosaur")
base_prompt = f"The child you are teaching is named {child.name}, they are {child.age} years old, in grade {child.grade}, and they are interested in {child.interests}. Please keep this information in mind when creating tailored exercises."

# update global child object with new attributes
def update_user_data(name, age, grade, interests):
    child = Child(name, age, grade, interests)
    base_prompt = f"The child you are teaching is named {child.name}, they are {child.age} years old, in grade {child.grade}, and they are interested in {child.interests}. Please keep this information in mind when creating tailored exercises."
    chat.send_message(base_prompt)
    # return Child(name, age, grade, interests)

# Code for Task 2
def message_submitted(text, history):
    response = chat.send_message(text)
    for i in range(len(response.text)):
        time.sleep(random.uniform(0.01, 0.05))
        yield response.text[: i+1]

# interface one
iface1 = gr.Interface(
    fn=update_user_data,
    inputs=["text", "number", "number", "text"],
    outputs=None,
    title="Multi-Page Interface"
)
# interface two

with gr.Blocks(fill_height=True) as iface2:
    chatbot = gr.Chatbot(
            scale = 2,
            height=500
        )
    chat = gr.ChatInterface(fn=message_submitted, title="Your personal teaching assistant", chatbot=chatbot)

# TODO write prompt for notebook generation
notebook_base_prompt = "Please create 5 exercises for the child you are teaching, based on the topic of trigonometry."

prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

def generate_notebook(ex_num, topic):
    raw_notebook = model.generate_content(notebook_base_prompt,
        generation_config=genai.GenerationConfig(response_mime_type="application/json",
        response_schema = NotebookSchema))
    print(raw_notebook.text)

with gr.Blocks(fill_height=True) as iface3:
    button = gr.Button("Generate Exercise")
    button.click(fn=generate_notebook)

demo = gr.TabbedInterface([iface1, iface2, iface3], ["user", "chat", "notebook"], title="Teaching Assistant")

# Run the interface
if __name__ == "__main__":
    chat = model.start_chat()
    demo.launch(share=True)