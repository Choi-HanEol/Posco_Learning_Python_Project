import sys
def convertToLowercase(command): # 대소문자 모두 소문자로 치환
    return command.lower()
def convertToUppercase(command): # 대소문자 모두 대문자로 치환
    return command.upper()
def showHeader():
    print("{:<10s}{:<15s}{:<10s}{:<10s}{:<10s}{:<10s}".format("Student", "Name", "Midterm", "Final", "Average", "Grade"))
    print("-" * 60)  # 총 60칸의 '-' 출력
def showStuList(data):
    for row in data:
        print("{:<10s}{:<15s}{:<10s}{:<10s}{:<10.2f}{:<10s}".format(row[0], row[1] ,row[2] ,row[3] ,row[4] ,row[5]))
def getGrade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 80 and avg < 90:
        return 'B'
    elif avg >= 70 and avg < 80:
        return 'C'
    elif avg >= 60 and avg < 70:
        return 'D'
    else:
        return 'F'
def getData(file_name):
    with open(file_name, "r") as f:
        text = f.read()
        split_data = [line.split('\t') for line in text.split('\n')]
        split_data.pop() # 마지막 개행문자 제거
    for idx in range(len(split_data)):
        avg, grade = getAvgGrade(split_data[idx][2], split_data[idx][3])
        split_data[idx].append(avg)
        split_data[idx].append(grade)
    return split_data
def setData(file_name, data):
    with open(file_name, 'w') as f:
        for row in data:
            f.write("{:<10s}{:<15s}{:<10s}{:<10s}{:<10.2f}{:<10s}".format(row[0], row[1] ,row[2] ,row[3] ,row[4] ,row[5]))
            f.write('\n')
            # f.write('\t'.join(map(str, row)) + '\n')
def getAvgGrade(mid_data, final_data):
    avg = (int(mid_data) + int(final_data))/2
    grade = getGrade(avg)
    return avg, grade
def updateAvgGrade(split_data):
    avg = (int(split_data[2]) + int(split_data[3]))/2
    split_data[4] = avg
    split_data[5] = getGrade(avg)
    return split_data[4], split_data[5]
class GradeManager:
    def __init__(self, data):
        self.data = data
    def show(self):
        self.data.sort(key=lambda x : x[4], reverse=True)
        showHeader()
        showStuList(self.data)
        # print()
    def search(self):
        input_sid = input("Student ID:")
        # print()
        for row in self.data:
            if row[0] == input_sid:
                showHeader()
                showStuList([row])
                return None
        print("NO SUCH PERSON.")
    def changescore(self):
        input_sid = input("Student ID:")
        # print()
        idx = 0
        for row in self.data:
            if row[0] == input_sid: #해당 학생을 찾았을 때
                input_mid_or_final = input("Mid/Final? ")
                input_mid_or_final = convertToLowercase(input_mid_or_final)
                if input_mid_or_final == 'mid':
                    input_new_score = input("Input new score:")
                    if (int(input_new_score) > 100) or (int(input_new_score) < 0):
                        print("잘못된 입력: 유효한 score 범위 (0~100)")
                        return None
                    showHeader()
                    showStuList([row])
                    print("Score changed.")
                    self.data[idx][2] = input_new_score
                    self.data[idx][4], self.data[idx][5] = updateAvgGrade(self.data[idx])
                    showStuList([self.data[idx]])
                    print()
                    return None
                elif input_mid_or_final == 'final':
                    input_new_score = input("Input new score:")
                    if (int(input_new_score) > 100) or (int(input_new_score) < 0):
                        print("잘못된 입력: 유효한 score 범위 (0~100)")
                        return None
                    showHeader()
                    showStuList([row])
                    print("Score changed.")
                    self.data[idx][3] = input_new_score
                    self.data[idx][4], self.data[idx][5] = updateAvgGrade(self.data[idx])
                    showStuList([self.data[idx]])
                    return None
                else:
                    print("잘못된 입력: (Mid or Final?)")
                    return None
            idx += 1
        print("NO SUCH PERSON.")
    def add(self):
        new_std_list = []
        input_sid = input("Student ID:")
        # print()
        for row in self.data:
            if row[0] == input_sid:
                print("ALREADY EXISTS")
                return None
        new_std_list.append(input_sid)
        input_name = input("Name: ")
        new_std_list.append(input_name)
        input_mid = input("Midterm Score: ")
        if int(input_mid) < 0 or int(input_mid) > 100:
            print("잘못된 범위 (0~100)")
            print()
            return None
        new_std_list.append(input_mid)
        input_final = input("Final Score: ")
        if int(input_final) < 0 or int(input_final) > 100:
            print("잘못된 범위 (0~100)")
            print()
            return None
        new_std_list.append(input_final)
        avg, grade = getAvgGrade(input_mid, input_final)
        new_std_list.append(avg)
        new_std_list.append(grade)
        self.data.append(new_std_list)
        print("Student added.")
    def searchgrade(self):
        input_grade = input("Grade to search: ")
        # print()
        input_grade = convertToUppercase(input_grade)
        finded_list = []
        is_find = False
        if (ord(input_grade) < 65 or ord(input_grade) > 70 or ord(input_grade) == 69):    # 입력된 학점이 A~D or F 가 아닐 때
            print("잘못된 학점 입력: A~D or F")
            return None
        for row in self.data:
            if row[5] == input_grade:
                is_find = True
                finded_list.append(row)
        showHeader()
        showStuList(finded_list)
        if not is_find:
            print("NO RESULTS.")
            return None
    def remove(self):
        if not self.data:
            print("List is empty.")
            print()
            return None
        input_sid = input("Student ID: (If you want to remove all info, please input \"all\" ): ")
        # print()
        for row in self.data:
            if row[0] == input_sid:
                self.data.remove(row)
                print("Student removed.")
                return None
        if input_sid == 'all':
            self.data.clear()
            return None
        print("NO SUCH PERSON.")
    def quit(self):
        input_save_signal = input("Save data? [yes/no] : ")
        self.data.sort(key=lambda x : x[4], reverse=True)   # 평균값을 기준으로 정렬
        if input_save_signal == 'yes':
            input_file_name = input("File name: ")
            if not'.txt' in input_file_name:
                input_file_name = input_file_name + '.txt'
            setData(input_file_name, self.data)
        elif input_save_signal == 'no':
            pass
        else:
            print("잘못된 명령어: (yes or no)\n")
            return False
        return True
def main():
    # read file name
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = 'students.txt'
    data = getData(file_name)
    grade_manager = GradeManager(data)
    grade_manager.show()
    print()
    while(True):
        # read command
        command = input("#")
        # print()
        command = convertToLowercase(command)
        # command 수행
        if command == 'show':
            grade_manager.show()
            print()
        elif command == 'search':
            grade_manager.search()
            print()
        elif command == 'changescore':
            grade_manager.changescore()
            print()
        elif command == 'add':
            grade_manager.add()
            print()
        elif command == 'searchgrade':
            grade_manager.searchgrade()
            print()
        elif command == 'remove':
            grade_manager.remove()
            print()
        elif command == 'quit':
            isQuit = grade_manager.quit()
            if not isQuit:
                continue
            break
        else:
            print("잘못된 command,\n 다시 입력\n")
            print()
            continue
if __name__ == "__main__":
    main()