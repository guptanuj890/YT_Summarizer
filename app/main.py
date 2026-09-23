from chat import answer_doubt

question = "Why is this concept important?"

answer = answer_doubt(
    question,
    lesson,
    lesson_settings["difficulty"]
)

print(answer)