#----------------------------------------------------
# Assignment 3: assignment3.py
# 
# Author: Peishu Huang 
# Collaborators/References: N/A
#----------------------------------------------------
# the code below is the main programm
#----------------------------------------------------

from enrollStudent import PriorityQueue,EnrollTable,StudentNode

def read_file():
    '''
    it will return a nested list
    '''
    # this try-catch code will determine whether the  filename is valid
    # if it is unvalid, then it will keep asking to input a valid filename
    openfile = False
    while not openfile:
        filename = input("Please enter a filename for student records: ")
        try:
            file = open(filename, "r")
            openfile = True
        except Exception:
            print("Invalid input") 
    content = file.readlines()
    file.close()
    data_list = []
    for student in content:
        data_list.append(data_split(student))
    return data_list
    
def data_split(student_string):
    '''
    return a list like this [ID, Faculty, first name, last name]
    '''
    string = student_string.rstrip("\n")
    data_list = string.split()  # this string.split() method will separate the string by space 
    if len(data_list) != 4:
        raise Exception("The", student_string ,"is not a valid data")
    isPass = (data_list[0].isnumeric() and (data_list[1] in ["EDU","ART","BUS","ENG","SCI"]))  # this will check whether the data is valid
    if isPass:
        return data_list
    else:
        raise Exception("The", student_string ,"is not a valid data")

def node_generate(student_data):
    '''
    it will generate a StudentNode from [ID, Faculty, first name, last name]
    it will return this node
    '''
    ID = student_data[0]
    faculty = student_data[1]
    first_name = student_data[2]
    last_name = student_data[3]
    return StudentNode(ID,faculty,first_name,last_name)

def table_waitlist():
    '''
    this will generate an enroll table (and priority queue if table is full)
    it will return the enroll table and priority queue
    '''
    data_list = read_file()  # get a nested list
    table = EnrollTable(51)  # create an enroll table
    waitlist = PriorityQueue()  # create a priority queue
    for student_data in data_list:  
        a_student = node_generate(student_data)
        if table.size() < 50:  # insert in table when the size is smaller than 50
            table.insert(a_student)
        else:  # else, it will insert into priority queue
            waitlist.enqueue(a_student)  
    return table, waitlist

def save_as_txt(string,txt_name, mode):
    '''
    the string argument is a string
    this method will save the string to a given txt
    mode can be "a", "w"
    '''
    file = open(txt_name, mode)
    if mode == "a":
        file.write("\n"+"-"*25+"\n")
    file.write(string)
    file.close()    

def drop_and_waitlist_reg(table, waitlist):
    '''
    the arguments are table and waitlist
    first it will drop student (from given file)
    and then it will dequeue the highest priority student from the priority queue and enroll this student in the course 
    by adding this student node to the enrollment table. 
    it will return table and waitlist
    '''
    data_list = read_file()      
    for student_data in data_list:
        a_student = node_generate(student_data)
        if table.isEnrolled(a_student.getID()):
            table.remove(a_student.getID())
            a_student = waitlist.dequeue()  # dequeue
            table.insert(a_student)  # enroll            
        else:
            message = "WARNING: %s %s (ID: %s) is not currently enrolled and cannot be dropped." % (a_student.getFirstName(),a_student.getLastName(),str(a_student.getID()))
            print(message)
    return table, waitlist

def message_print_and_save(table, waitlist):
    '''
    nothing but just a meassage printer
    it will also save the content
    return nothing
    '''
    print("\nThis is the Enroll Table:")
    print(table)
    save_as_txt(str(table), "enrolled.txt", "w")
    print("\nThis is the Waitlist:")
    print(waitlist)
    print('')
    save_as_txt(str(waitlist), "waitlist.txt", "a")    

def main():
    user_input = ""
    quit = False
    while not quit:
        while not user_input in ["R","D","Q"]:
            user_input = input("R for Register, D for Drop, Q for quit: ")
        if user_input == "Q":
            print("Goodbye...")
            quit = True
        elif user_input == "R":
            table, waitlist = table_waitlist()
            message_print_and_save(table,waitlist)
            user_input = ""
        elif user_input == "D":
            table, waitlist = drop_and_waitlist_reg(table, waitlist)
            message_print_and_save(table,waitlist)
            user_input = ""         

main()
            

      
