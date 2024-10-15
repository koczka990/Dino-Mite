import json
json_string = """```json
[
  {
    "exercise_number": 1,
    "topic": "Trigonometry: Sine",
    "exercise": "Imagine you're flying a kite! The string is 10 meters long, and it makes a 30-degree angle with the ground. How high is the kite in the air?"
  },
  {
    "exercise_number": 2,
    "topic": "Trigonometry: Cosine",
    "exercise": "You're walking your dog on a leash that's 2 meters long. You're walking in a straight line, and your dog is pulling at a 45-degree angle. How far away is your dog from you?"
  },
  {
    "exercise_number": 3,
    "topic": "Trigonometry: Tangent",
    "exercise": "You're building a ramp for your skateboard. The ramp is 3 meters long, and the base of the ramp is 2 meters wide. What is the angle of the ramp?"
  },
  {
    "exercise_number": 4,
    "topic": "Trigonometry: Finding Angles",
    "exercise": "You're playing a game of pool. You hit the white ball, and it travels 5 meters before hitting a red ball. The red ball moves 3 meters away from the white ball. What angle did the white ball hit the red ball at?"
  },
  {
    "exercise_number": 5,
    "topic": "Trigonometry: Applications",
    "exercise": "You want to find the height of a tree. You stand 10 meters away from the tree and measure the angle of elevation to the top of the tree to be 60 degrees. How tall is the tree?"
  }
]
```"""
# print("--------------------")
# print(json_string[950:960])
# print("--------------------")
listss = json.loads(json_string[8:-4])
print(listss[0])