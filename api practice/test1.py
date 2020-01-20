import json
import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)

todo_user_dict = {}
for todo in todos:
    if todo['completed']:
        try:
            todo_user_dict[todo['userId']] += 1
        except KeyError:
            todo_user_dict[todo['userId']] = 1
top_users = sorted(todo_user_dict.items(), key=lambda x: x[1], reverse=True)
max_completed = top_users[0][1]
users = []
for score in top_users:
    if score[1] == max_completed:
        users.append(str(score[0]))
max_users = " and ".join((users))
filtered_todos = []
for todo in todos:
    if str(todo['userId']) in users:
        filtered_todos.append(todo)
with open("filtered_data_file.json", 'w') as write_file:
    json.dump(filtered_todos, write_file, indent=2)
