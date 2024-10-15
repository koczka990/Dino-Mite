import gradio as gr
import typing_extensions
import typing_extensions
import gradio as gr
import random
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
import pdf_generator as pdf_gen

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are an experienced and engaging math teacher specializing in foundational math topics such as addition, subtraction, multiplication, and division. You create interactive and personalized exercises that adapt to each student’s interests and learning pace. Your goal is to make math fun, educational, and tailored to the child's unique interests or themes they enjoy (such as animals, sports, or space). Ensure exercises vary in difficulty and provide hints or encouragement if a student struggles, fostering a positive and confidence-building learning environment",
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
    interests: str 

# global child object to save attributes
child = Child("John", 10, 5, "Dinosaur")
base_prompt = f"The child you are teaching is named {child.name}, they are {child.age} years old, in grade {child.grade}, and they are interested in {child.interests}. Please keep this information in mind when creating tailored exercises."

# update global child object with new attributes
def update_user_data(name, age, grade, interests):
    child = Child(name, age, grade, interests)
    base_prompt = f"The child you are teaching is named {child.name}, they are {child.age} years old, in grade {child.grade}, and they are interested in {child.interests}. Please keep this information in mind when creating tailored exercises."
    chat.send_message(base_prompt)

# Code for Task 2
def message_submitted(text, history):
    response = chat.send_message(text)
    for i in range(len(response.text)):
        time.sleep(random.uniform(0.01, 0.05))
        yield response.text[: i+1]


with gr.Blocks(fill_height=True, fill_width=False) as iface_merged:
    name_box = gr.Textbox(label="Name")
    age_box = gr.Number(label="Age", minimum=0, maximum=100)
    grade_box = gr.Number(label="Grade", minimum=0, maximum=12)
    interests_box = gr.Textbox(label="Interests")
    submit_btn = gr.Button("Submit")

    with gr.Column(visible=False) as output_col:
        chatbot = gr.Chatbot(
                placeholder="Your data was successfully submitted! Please ask me anything.",
                scale = 2,
                height=500
            )
        chat = gr.ChatInterface(fn=message_submitted, title="Your personal teaching assistant", chatbot=chatbot)

    def submit(name, age, grade, interests):
        update_user_data(name, age, grade, interests)
        return {
            name_box: gr.Textbox(label="Name", visible=False),
            age_box: gr.Number(label="Age", minimum=0, maximum=100, visible=False),
            grade_box: gr.Number(label="Grade", minimum=0, maximum=12, visible=False),
            interests_box: gr.Textbox(label="Interests", visible=False),
            submit_btn: gr.Button("Submit", visible=False),
            output_col: gr.Column(visible=True),
        }

    submit_btn.click(
        submit,
        [name_box, age_box, grade_box, interests_box],
        [name_box, age_box, grade_box, interests_box, submit_btn, output_col],
    )

notebook_base_prompt = """Please create 5 exercises for the child you are teaching, based on the topic of trigonometry in this JSON format. Only output the expected json list.

Use this JSON schema:

Exercise = {'exercise_number': int, 'topic': str, 'text': str}
Return: list[Exercise]"""

def get_notebook_prompt(num_of_ex, topic):
    prompt = f"Please create {num_of_ex} exercises for the child you are teaching, based on the topic of {topic} in this JSON format. ex_title should be a creative title for each exercise. Only output the expected json list. Use this JSON schema: Exercise = " + "{'exercise_number': int, 'ex_title': str, 'text': str} Return: list[Exercise]"
    return prompt

class NotebookSchema(typing_extensions.TypedDict):
    exercise_number: int
    topic: str
    exercises: list[str]


def generate_notebook(topic, num_of_ex, progress=gr.Progress()):
    progress(0, desc="Starting")
    time.sleep(1)
    progress(0.05)
    prompt = get_notebook_prompt(num_of_ex, topic)
    response = chat.send_message(prompt)
    from_index = response.text.find("[")
    to_index = response.text.rfind("]") + 1
    pdf_gen.generate_notebook(response.text[from_index:to_index])
    for i in range(num_of_ex):
        progress(i/num_of_ex, desc=f"Generating exercise {i+1}.")
        time.sleep(random.uniform(0.1, 0.7))
    return [gr.Text("Exercise sheet generated!"), gr.DownloadButton(label="Download Notebook", value="notebook.pdf", visible=True)]

iface3 = gr.Interface(generate_notebook, inputs=[gr.Text(label="Topic"), gr.Number(label="Number of Exercises")], outputs=[gr.Text(label=""), gr.DownloadButton(label="Download Notebookd", visible=False)])


demo = gr.TabbedInterface([iface_merged, iface3], ["Main", "notebook"], title="Teaching Assistant")

# Run the interface
if __name__ == "__main__":
    chat = model.start_chat()
    demo.launch(share=True)