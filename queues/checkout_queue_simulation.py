#Modified By Katherine Botticelli
#PA 4.6

class Queue(object):
    
    def __init__(self, size):             # Constructor
        self.__maxSize = size              # Size of [circular] array
        self.__que = [None] * size         # Queue stored as a list
        self.__front = 1                   # Empty Queue has front 1
        self.__rear = 0                    # after rear and
        self.__nItems = 0                  # No items in queue

    def insert(self, item):               # Insert item at rear of queue
        if self.isFull():                  # if not full
            raise Exception("Queue overflow")
        self.__rear += 1                   # Rear moves one to the right
        if self.__rear == self.__maxSize:  # Wrap around circular array
            self.__rear = 0
        self.__que[self.__rear] = item     # Store item at rear
        self.__nItems += 1
        return True

    def remove(self):                     # Remove front item of queue
        if self.isEmpty():                 # and return it, if not empty
            raise Exception("Queue underflow")
        front = self.__que[self.__front]   # get the value at front
        self.__que[self.__front] = None    # Remove item reference
        self.__front += 1                  # front moves one to the right
        if self.__front == self.__maxSize: # Wrap around circular arr.
            self.__front = 0
        self.__nItems -= 1
        return front

    def peek(self):                       # Return frontmost item
        return None if self.isEmpty() else self.__que[self.__front]

    def isEmpty(self): return self.__nItems == 0

    def isFull(self): return self.__nItems == self.__maxSize

    def __len__(self): return self.__nItems
    
    def __str__(self):                    # Convert queue to string
        ans = "["                          # Start with left bracket
        for i in range(self.__nItems):     # Loop through current items
            if len(ans) > 1:                # Except next to left bracket,
                ans += ", "                  # separate items with comma
            j = i + self.__front            # Offset from front
            if j >= self.__maxSize:         # Wrap around circular array
                j -= self.__maxSize
            ans += str(self.__que[j])       # Add string form of item
        ans += "]"                         # Close with right bracket
        return ans

    def add(self, index, item):         #adds most recent customer to a queue
        customer = index                #copy of the index value 
        customer += 1                   #index plus one because the index of an array starts at 0 and a customer has to start at 1.
        customer = str(customer)       #converts customer to string
        rear = item.capitalize() + customer     #combines the queue the user selected with the number of customer they are will look like "A1"
        self.insert(rear)                       #inserts the customer into the queue

    
    def queueMod(self, index, item):        #This method handles adding and removing from the queue.
        if item.islower():                  #if the item or letter is lowercase then add the customer to the queue.
            if self.isFull():               #checks if queue is full
                print(item, "queue is full can not go into checkout line") #if queue is full customer cannot be added 
                return self                 #returns queue with no new customers 
            else:
                self.add(index, item)           #calls on add method that adds the customer to queue
                return self                     #returns the queue
        elif item.isupper():                #if the item or letter is uppercase than remove the customer for queue
            if self.isEmpty():              #checks if queue is empty 
                print(item, "queue is empty can not checkout") #when queue is empty print message that line is empty
                return self                 #returns the queue with all no customers 
            if self.isEmpty() == False:     #if line is not empty 
                self.remove()               #checks out the first person in line 
                return self                 #returns new queue 
def main():                         #main code for running tests 
    def customer(line):             #takes in a string of customers and sends them to their correct queue to be handled
        A = Queue(len(line))        #Declares Queue A
        B = Queue(len(line))        #Declares Queue B
        C = Queue(len(line))        #Declares Queue C
        D = Queue(len(line))        #Declares Queue D
    
    
        copyLine = line                 #copy of the input string 
        for i in range (len(copyLine)):     #loops through the string object 
            if copyLine[i] == "a" or copyLine[i] == "A":       #if i is "a" or "A"
                A = A.queueMod(i, copyLine[i])                 #then execute method queueMod on A queue 
            elif copyLine[i] == "b" or  copyLine[i] == "B":    #if i is "b" or "B"
                B = B.queueMod(i, copyLine[i])                 #then execute method queueMod on B queue 
            elif copyLine[i] == "c" or copyLine[i] ==  "C":    #if i is "c" or "C"
                C = C.queueMod(i, copyLine[i])                 #then execute method queueMod on C queue 
            elif copyLine[i] == "d" or copyLine[i] == "D":     #if i is "d" or "D"
                D = D.queueMod(i, copyLine[i])                 #then execute method queueMod on D queue 
            if copyLine[i].isalpha() == False or i == len(copyLine)-1:  #checks if i is a letter or if i is the last index in the array 
                print(copyLine[:i])                                     #prints the string from 0 to i 
                if A.isEmpty():                                         #if queue is empty 
                    print("[A line has no customers]")                  #prints out that the queue is empty 
                elif A.isEmpty() == False:                              #if queue is not empty 
                    print(A.__str__())                                  #prints out all contents of queue 
                if B.isEmpty():                                         #if queue is empty  
                    print("[B line has no customers]")                  #prints out that the queue is empty 
                elif B.isEmpty() == False:                              #if queue is not empty
                    print(B.__str__())                                  #prints out all contents of queue
                if C.isEmpty():                                         #if queue is empty 
                    print("[C line has no customers]")                  #prints out that the queue is empty 
                elif C.isEmpty() == False:                              #if queue is not empty
                    print(C.__str__())                                  #prints out that the queue is empty 
                if D.isEmpty():                                         #if queue is empty 
                    print("[D line has no customers]")                  #prints out that the queue is empty 
                elif D.isEmpty() == False:                              #if queue is not empty
                    print(D.__str__())                                
        
    customer("aababbAbA")                       #tests customers method with string 
    customer("aaaa,AAbcd,abababcabc,Adb,Adb,Ca,dcbadcbaDCBA-ddAcccBbbbCaaaD-") #test customer method with string 

if __name__ == "__main__" :                     #runs the main method. 
    main()


#Lafore, Robert; Broder, Alan; Canning, John. Data Structures & Algorithms in Python (pp. 120-121). Pearson Education. Kindle Edition. 
