students = []
scores = []

while True:
    name = input("Enter student name (or type 'done' to finish): ")

    if name.lower() == "done":
        break

    score = float(input("Enter score: "))

    if score < 0 or score > 100:
        print("Score must be between 0 and 100. Please try again.")
        continue

    students.append(name)
    scores.append(score)

if len(scores) == 0:
    print("No valid student data entered.")
else:
    average = sum(scores) / len(scores)
    highest = max(scores)
    lowest = min(scores)
    total_students = len(scores)

    print(" Results:")
    print("Average Score:", average)
    print("Highest Score:", highest)
    print("Lowest Score:", lowest)
    print("Total Students:", total_students)