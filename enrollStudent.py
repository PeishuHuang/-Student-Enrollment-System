#----------------------------------------------------
# Assignment 3: enrollStudent
# 
# Author: Peishu Huang 
# Collaborators/References: N/A
#----------------------------------------------------
# the code below is a module for assignment3
# it contains class StudentNode, EnrollTable
# and PriorityQueue
#----------------------------------------------------

class StudentNode:
    def __init__(self, student_id, faculty, first, last):
        '''
        takes four strings as input parameters: the student id, faculty, first name, and last name. 
        '''
        self.__id = student_id
        self.__faculty = faculty
        self.__firstname = first
        self.__lastname = last   
        self.__previous = None
        self.__next = None
    
    def setID(self, student_id):
        '''
        sets the student id to the given id. 
        '''
        self.__id = student_id
    
    def setFac(self,faculty): 
        '''
        sets the faculty abbreviation to the given faculty. 
        '''
        self.__faculty = faculty
    
    def setFirstName(self,first):
        '''
        sets the student's first name to the given first name. 
        '''
        self.__firstname = first
        
    def setLastName(self,last): 
        '''
        sets the student's last name to the given last name. 
        '''
        self.__lastname = last
    
    def setNext(self,next): 
        '''
        sets next as the next node. 
        '''
        self.__next = next
    
    def setPrev(self,previous): 
        '''
        sets previous as the previous node. 
        '''
        self.__previous = previous
    
    def getID(self):
        '''
        returns the student id as a string. 
        '''
        return self.__id
        
    def getFac(self):
        ''' 
        returns the faculty abbreviation as a string. 
        '''
        return self.__faculty
        
    def getFirstName(self): 
        '''
        returns a string representing the student's first name. 
        '''
        return self.__firstname
        
    def getLastName(self):
        '''
        returns a string representing the student's last name. 
        '''
        return self.__lastname
    
    def getNext(self):
        '''
        returns the next node.
        '''
        return self.__next
        
    def getPrev(self): 
        '''
        returns the previous node.     
        '''
        return self.__previous

class EnrollTable:
    def __init__(self,capacity):
        self.__table = []
        for i in range(capacity):
            self.__table.append([None])
        
        self.__capacity = capacity
        self.__size = 0
    
    def computIndex(self,studentID):
        '''
        this method takes a given student id string as a parameter and returns an 
        integer that will represent the index
        '''
        studentID = int(studentID)
        first = studentID//10000
        second = studentID//100 - first*100
        third = studentID - first*10000 - second*100
        summation = first + second + third**2
        return summation%self.__capacity
    
    def insert(self,item):
        '''
        this method inserts a given item, a StudentNode object, in the enrollment table
        '''
        # call the computIndex method
        item_id = item.getID()
        index = self.computIndex(item_id)
        slot = self.__table[index]
        if slot[0] == None:  # when there is no StudentNode in slot, appending it directly
            slot[0] = item
        else:
            # since the studentID is a unique 6 digits
            # so they have partial order relationship
            # so the below code will insert item exactly once
            # To see this, we should assume the single linked in slot is already in an (strictly) ascending order
            # so we have something like this, id_1 < id_2 < id_3 <... < id_n 
            # if id_j < item_id < id_j+1, then no wonder item_id < id_j+1 < id_j+2 < ......
            # so it is impossible to insert more than once
            finish = False
            student = slot[0]
            if int(item_id) < int(slot[0].getID()):  # when the item has smallest ID
                item.setNext(student)
                slot[0] = item  
                finish = True
            while not finish:
                current_id = int(student.getID())
                if student.getNext() != None:
                    next_student = student.getNext()
                    next_id = int(next_student.getID())
                else:
                    # when the item_id is greater than all studentID, then it should be insert at the end
                    # so we set a number which is always greater than the item_id, that is (item_id + 1)
                    # and we set a "pseudo-next_student", which is None actually
                    next_student = None
                    next_id = str(int(item_id) + 1)
                if int(current_id) < int(item_id) < int(next_id):  # this will insert exactly once
                    student.setNext(item)
                    item.setNext(next_student)
                    finish = True
                else:  
                    # this will not be executed when the item be inserted into the end
                    # so the student will not be None
                    student = next_student
        self.__size = self.__size + 1
    
    def remove(self,studentID):
        '''
        this method removes from the enrollment table the node for the relevant 
        student corresponding with the given student id. 
        This method returns True if the student has been successfully dropped from the course or False otherwise. 
        '''
        studentID = str(studentID)
        index = self.computIndex(studentID)
        slot = self.__table[index]
        if slot[0] == None:
            return False
        # else:
        student = slot[0]  
        if student.getID() == studentID:  # when it is at the first position
            next_student = student.getNext()  # next student could be None  
            student.setNext(None)
            slot[0] = next_student
        else:
            finish = False
            while not finish:
                current_id = student.getID()
                if student.getNext() != None:
                    next_student = student.getNext()
                    next_id = next_student.getID()  # None type has no getId attribute
                if next_id == studentID:
                    student.setNext(next_student.getNext())
                    next_student.setNext(None)
                    finish = True
                else:
                    student = next_student
                if student == None:
                    # if the next is None, and it is still in this loop
                    # then there is no such student
                    return False                      
        self.__size = self.__size - 1
        return True
        
    def isEnrolled(self,studentID):
        '''
        this method searches the enrollment table given a student id, and returns 
        True if the corresponding student is found in the table, and False otherwise
        '''
        studentID = str(studentID)
        index = self.computIndex(studentID)
        slot = self.__table[index]
        if slot[0] == None:  # if it is empty
            return False
        else:
            student = slot[0]
            while True:
                if student != None:  # when it is not the end
                    if student.getID() == studentID:  # this means the student enrolled
                        return True
                    else:
                        student = student.getNext()  # if not, keep traversing
                else:
                    # if it is None, then it is at the end, that means it traverses the whole link
                    # since "return True" hasn't been executed
                    # then this student doesn't enroll
                    return False 
                
    def size(self):
        '''
        just return the size(an integer) of the table
        '''
        return self.__size
    
    def isEmpty(self):
        '''
        determine whether the table is empty
        return a boolean value
        '''
        return self.__size == 0
    
    def __studentstr(self,student):  # a private method
        return " %s %s %s %s" % (student.getID(), student.getFac(), student.getFirstName(), student.getLastName())
    
    def __str__(self):
        '''
        return a string
        '''
        string = "["
        for index in range(self.__capacity):
            slot = self.__table[index]
            if  slot[0] != None:
                string = string + str(index) + ":"
                finish = False
                student = slot[0]
                while not finish:
                    if student.getNext() == None:
                        string = string + self.__studentstr(student) + "\n"
                        finish = True
                    else:
                        string = string + self.__studentstr(student) + ","
                        student = student.getNext()
        string = string.rstrip("\n") + "]"
        return string

class PriorityQueue:
    def __init__(self):
        # creates an empty doubly linked chain with both head and tail having references to None
        # and the size of the priority queue should be set to 0. 
        self.__head = None
        self.__tail = None
        self.__size = 0
    
    def __getPriority(self,item):  # private method
        '''
        get the priotiy value of a StudentNode
        return an integer that can represent the faculty
        '''
        priority_value = ["EDU","ART","BUS","ENG","SCI"]  # Faculty priority value is its index
        return priority_value.index(item.getFac())
    
    def __search(self,current_node, priority_value):
        '''
        this will traverse the queue from tail by taking the priotiyvalue as key
        it return a StudentNode 
        this will only apply to the queue when it has two different priority value in the queue
        it will use in the enqueue method
        so it would not has any exception by the premises
        '''
        # in the situation that where this will be applied 
        # there is StudentNode's priority value bigger than the given one and there also exists a smaller one
        # then in this situation, it will return the leftmost StudenNode which priority value is bigger and the most close to the given one
        # for example, if the queue is [front-> 4-4-4-4-3-3-1-1-1-1 <- rear], and the given priority value is 3, 
        # then it will return the rightmost "3"
        if self.__getPriority(current_node) == priority_value:
            return current_node
        elif self.__getPriority(current_node) < priority_value and self.__getPriority(current_node.getPrev()) > priority_value:
            return current_node.getPrev()
        else:
            return self.__search(current_node.getPrev(), priority_value)  # recursively         
    
    def enqueue(self,item):
        '''
        enqueues a new StudentNode to the rear of the queue or traverses the queue to 
        determine the position in which the new node will be inserted based on the faculty priority of the given item
        This method updates the priority queue size by incrementing it by 1
        This method does not return anything. 
        '''
        # there are several situations totally
        # if there are StudentNodes with the given priority value in the queue, self.__search will return the rightmost one of them 
        # so insert it directly
        # if there is no such StudentNode, then it has several situations too.
        # i) the queue is empty, then insert it directly
        # ii) the priority value of self.__tail is bigger than the given value, then insert it to the self.__tail
        # iii) the priority value of self.__head is smaller than the given value, then insert it to the self.__head  
        # iv) there is StudentNode's priority value bigger than the given one and there also exists a smaller one
        # then it will call the self.__search
        priority_value = self.__getPriority(item)
        if self.isEmpty():
            self.__head = item
            self.__tail = item
        else:
            if self.__getPriority(self.__tail) >= priority_value:
                self.__tail.setNext(item)
                item.setPrev(self.__tail)
                self.__tail = item
            elif self.__getPriority(self.__head) < priority_value:
                self.__head.setPrev(item)
                item.setNext(self.__head)
                self.__head = item
            else:
                node = self.__search(self.__tail, priority_value)
                next_node = node.getNext()
                item.setNext(next_node)
                item.setPrev(node)
                next_node.setPrev(item)
                node.setNext(item)     
        self.__size = self.__size + 1
        
    def dequeue(self,):
        '''
        dequeues and returns the highest priority student node from the front of the queue 
        and size decrementing 1. An Exception is raised if dequeueing from an empty queue. 
        it return a StudentNode
        '''
        if self.isEmpty():  # when dequeueing from an empty queue
            raise Exception("Priority queue is empty")
        else:
            node = self.__head
            new_head = node.getNext()
            self.__head = new_head
            new_head.setPrev(None)
            node.setNext(None)
            self.__size = self.__size - 1
            return node
    
    def isEmpty(self):
        '''
        returns True if the priority queue is empty, if its size is 0, or False otherwise
        '''
        return self.__size == 0
    
    def __studentstr(self,student):
        return "%s %s %s %s" % (student.getID(), student.getFac(), student.getFirstName(), student.getLastName())
    
    def size(self):
        '''
        just return the size of priority queue
        '''
        return self.__size
    
    def __str__(self):
        string = "["
        if not self.isEmpty():
            node = self.__head
            string = string + self.__studentstr(node) + ",\n" 
            for times in range(self.__size-1):
                node = node.getNext()
                string = string + " " + self.__studentstr(node) + ",\n" 
            string = string.rstrip(",\n") + "]"
        else:
            string = string + "]"
        return string
    

if __name__ == "__main__":
    # StudentNode test
    # 129051 ART Paul Johnston
    student = StudentNode("None","None","None","None")
    peishu = StudentNode("510000","ART","Peishu","Huang")
    
    student.setID("129051")
    isPass = (student.getID() == "129051")
    assert isPass == True, ("Fail the setID or getID check")
    
    student.setFac("ART")
    isPass = (student.getFac() == "ART")
    assert isPass == True, ("Fail the setFac or getFac check")
    
    student.setFirstName("Paul")
    isPass = (student.getFirstName() == "Paul")
    assert isPass == True, ("Fail the setFirstName or getFirstName check")
    
    student.setLastName("Johnston")
    isPass = (student.getLastName() == "Johnston")
    assert isPass == True, ("Fail the setLastName or getLastName check")
    
    student.setNext(peishu)
    isPass = (student.getNext() != None)
    assert isPass == True, ("Fail the setNext or getNext check")
    
    student.setPrev(peishu)
    isPass = (student.getPrev() != None)
    assert isPass == True, ("Fail the setPrev or getPrev check") 
    
    if isPass:
        print("StudentNode class seems good")
    
    # EnrollTable test, capacity 51
    table = EnrollTable(51)
    student.setNext(None)
    student.setPrev(None)
    
    isPass = (table.isEmpty())
    assert isPass == True, ("Fail the isEmpty check")
    
    isPass = (table.computIndex(student.getID()) == 0)
    assert isPass == True, ("Fail the computIndex check")
    
    table.insert(student)
    isPass = (table.isEnrolled(129051) == True)
    assert isPass == True, ("Fail the insert or isEnrolled check")
        
    table.insert(peishu)
    isPass = (table.size() == 2)
    assert isPass == True, ("Fail the size check")

    table.remove("510000")
    isPass = (table.size() == 1)
    assert isPass == True, ("Fail the remove check")
    
    isPass = ((not table.isEnrolled("510000")) and table.isEnrolled("129051"))
    assert isPass == True, ("Fail the isEnrolled check")
    
    isPass = (str(table) == "[0: 129051 ART Paul Johnston]")
    assert isPass == True, ("Fail the __str__ check")
    
    if isPass:
        print("EnrollTable class seems good")    
    
    # PriorityQueue test
    queue=PriorityQueue()
    student1 = StudentNode("000001","ART","P1","Huang")
    student2 = StudentNode("000002","ART","P2","Huang")
    student3 = StudentNode("000003","EDU","P3","Huang") 
    student4 = StudentNode("000004","SCI","P4","Huang")
    student5 = StudentNode("000005","ART","P5","Huang")
    student6 = StudentNode("000006","SCI","P6","Huang")
    student7 = StudentNode("000005","ENG","P7","Huang")    
    
    
    isPass = (queue.isEmpty() == True)
    assert isPass == True, ("Fail the isEmpty check")
    
    queue.enqueue(student1)
    isPass = (queue.isEmpty() == False)
    assert isPass ==True, ("Fail the enqueue check")
    
    queue.enqueue(student2)
    queue.enqueue(student3)
    queue.enqueue(student4)
    queue.enqueue(student5)
    queue.enqueue(student6)
    queue.enqueue(student7)    
    isPass = (queue.size() == 7)
    assert isPass == True, ("Fail the size check")
    
    queue.dequeue()
    isPass = (queue.size() == 6)
    assert isPass == True, ("Fail the dequeue check")
    
    string = "[000006 SCI P6 Huang,\n 000005 ENG P7 Huang,\n 000001 ART P1 Huang,\n 000002 ART P2 Huang,\n 000005 ART P5 Huang,\n 000003 EDU P3 Huang]"
    isPass = (str(queue) == string)
    assert isPass == True, ("Fail the __str__ check")

    if isPass:
        print("PriorityQueue class seems good")       
    
    
    
    
    
    
    