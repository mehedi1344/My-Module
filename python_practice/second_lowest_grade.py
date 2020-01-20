student_with_grade = {}
for _ in range(int(input())):
  name = input()
  score = float(input())
  student_with_grade[name] = score
student_grade_list = [[i, j] for i, j in student_with_grade.items()]
sorted_list = sorted(student_grade_list, key = lambda x:x[1])
only_grade = [i[1] for i in sorted_list]
mylist = list(dict.fromkeys(only_grade))
min_grade = mylist[0]
mylist.remove(min_grade)
second_min_grade = mylist[0]
low_grd_std = []
for i in sorted_list:
  if i[1]==second_min_grade:
    low_grd_std.append(i)
final_sorted_list = sorted(low_grd_std, key = lambda x:x[0])
for name in final_sorted_list:
  print(name[0])
