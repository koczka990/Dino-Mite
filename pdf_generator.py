import json
import pdfkit

class Exercise:
    def __init__(self, exercise_number, ex_title, text):
        self.exercise_number = exercise_number
        self.ex_title = ex_title
        self.text = text

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notebook Template</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .exercise {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .exercise-title {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .exercise-number {
            font-weight: bold;
        }
        .exercise-text {
            margin-top: 10px;
        }
        .exercise img {
            margin-right: 20px;
            max-width: 100px;
            max-height: 100px;
        }
    </style>
</head>
<body>
    <h1>Notebook Template</h1>
    
    //exercisesgohere
    
    <!-- Add more exercises as needed -->
    
</body>
</html>"""

html_exercise = """<div class="exercise">
        <img src="path/to/image1.jpg" alt="Exercise 1 Image">
        <div>
            <div class="exercise-title">{{ex_title}}</div>
            <div class="exercise-number">{{number}}</div>
            <div class="exercise-text">{{text}}</div>
        </div>
    </div>"""

path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def extract_exercises_from_json(raw_json):
    json_list = json.loads(raw_json)
    exercises = []
    for item in json_list:
        exercise = Exercise(
            exercise_number=item.get('exercise_number'),
            ex_title=item.get('ex_title'),
            text=item.get('text')
        )
        exercises.append(exercise)
    return exercises

def generate_notebook(raw_json):
    exercises = extract_exercises_from_json(raw_json)
    all_exercises = ""
    for exercise in exercises:
        print("TESTING")
        print(exercise.exercise_number, "--", exercise.ex_title, "--", exercise.text)
        print("------------------")
        ex_html = html_exercise
        ex_html = ex_html.replace('{{ex_title}}', exercise.ex_title)
        ex_html = ex_html.replace('{{number}}', str(exercise.exercise_number))
        ex_html = ex_html.replace('{{text}}', exercise.text)
        all_exercises += ex_html
    output_html = html_template.replace('//exercisesgohere', all_exercises)
    print("------------------")
    print(output_html)
    print("------------------")
    pdfkit.from_string(output_html, 'notebook.pdf', configuration=config, options={"enable-local-file-access": ""})
    return output_html
    