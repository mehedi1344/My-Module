if __name__ == '__main__':
    n = int(input())
    student_marks = {}
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()
    numbers = []
    for key in student_marks:
      try:
        if key==query_name:
          numbers = student_marks[key]
          break
      except NameError:
        pass
    total_num = 0
    for i in range(len(numbers)):
      total_num += numbers[i]
    average_num = float(total_num/int(len(numbers)))
    print("{:.2f}".format(average_num))
