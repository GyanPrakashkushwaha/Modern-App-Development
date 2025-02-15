with open('data.csv', 'r') as f:
    header = f.readline()
    content = [i.strip().split(',') for i in f]
    

id_value = 1001
student_data = []
for i in content:
    std_data = i[0].strip()
    # print(std_data)
    if int(std_data) == id_value:
        student_data.append(i)
        
id_value = 2001      
marks_lst = []
for row in content:
    course_id = int(row[1].strip())
    # print(course_id)
    if course_id == id_value:
        print(course_id)
        marks_lst.append(int(row[2].strip()))
    

print(marks_lst)
print(max(marks_lst))
# print(header)
# print(content)
# print(content[0].split(','))
# print([i.strip() for i in content[0].split(',')]) # stripped.
# print([i.split(',') for i in student_data])
# print(student_data)