'''
Author: Kyle Strokes
Purpose: This is the imported classes for friends.py methods
    allow to find mutual friends of two people
Course: CS 120, Section 1F, Spring 2018.
'''

'''This class represents a person node and contains their name, linked
    list of friends, and next person in list'''
class Node:
    '''Initializing the name, friends, and next for person'''
    def __init__(self, name):
        self.name = name
        self.friends = LinkedList()
        self.next = None

    '''Returns name of person'''
    def get_name(self):
        return self.name

    '''Returns the linked list of friends of the person'''
    def get_friends(self):
        return self.friends
    
    '''This adds a node to the linked list (friends list)
        of another node'''
    def add_friend(self, node):
        self.friends.add(node)
    
    '''Returns the next person in linked list main'''
    def get_next(self):
        return self.next

    '''Retuns all data for a person as string'''
    def __str__(self):
        return self.name


'''This class represents a main list of people in a file'''
class LinkedList:
    '''Sets the head of the list to None'''
    def __init__(self):
        self.head = None
        
    '''Returns the head of list'''
    def get_head(self):
        return self.head
    
    '''Returns True if list is empty'''
    def is_empty(self):
        return self.head == None
    
    '''Returns boolean whether a passed in node is in the linked listed'''
    def contains(self, other):
        temp = self.head
        '''Traverses the list of self'''
        while temp != None:
            '''if other is found then returns True'''
            if other == temp.get_name():
                return True
            '''moves to next node'''
            temp = temp.next
        return False

    '''Gets the node of the string name'''
    def get_node_of(self, name):
        temp = self.head
        '''Traverses list'''
        while temp != None:
            '''if the string matches the string of node'''
            if name == temp.get_name():
                return temp
            '''goes on to next node'''
            temp = temp.next
        
    '''Finds the mutual friends of self and another friendlist'''
    def find_mut_friend(self, temp1):
        temp2 = self.head
        '''Traverses list'''
        while temp2 != None:
            '''If the two names are the same returns the name'''
            if temp1.get_name() == temp2.get_name():
                return temp1
            '''goes to next node in self'''
            temp2 = temp2.next

        
    
    '''adds a new node (new) to the front of list'''
    def add(self, new):
        '''current head is new's next'''
        new.next = self.head
        '''list head is new'''
        self.head = new
    
    '''prints out the values of the list for debugging'''
    def __str__(self):
        '''Shows the last name added as the head'''
        result = 'Head ->'
        temp = self.head
        while temp != None:
            result += ' ' + temp.__str__() + ','
            temp = temp.next
        '''Shows the first name added their next is None'''
        result += '-> None'
        return result


