'''
Author: Kyle Strokes
Purpose:    allow to find mutual friends of two people
Course: CS 120, Section 1F, Spring 2018.
'''
'''Imported linked_list.py to use methods and sys to exit errors'''
from linked_list import *
import sys

def main():
    file = input('Input file: ')
    file_check(file)
    file = open(file)
    '''main linked list'''
    ll = LinkedList()
    for line in file:
        arrange_nodes(line, ll)
    name1 = input('Name 1: ')
    name_check(name1, ll)
    name2 = input('Name 2: ')
    name_check(name2, ll)
    '''For node1 and node2, gets the node of name1 and name2
        then get the friends list of those names'''
    node1 = ll.get_node_of(name1).get_friends()
    node2 = ll.get_node_of(name2).get_friends()
    '''To traverse through node1's friend list'''
    temp1 = node1.head
    header = 0
    find_friends(temp1, node2, header)

'''This function takes the temp1 which is the head of one friend
    list and traverses another friend list to find mutual friends

    Parameters: temp1: the node1 (friend's list of name1), node2
        (friend's list of name2), header (which pretty much decides
        when the first name is printed)

    Returns: None

    Pre-Conditions: temp1 is a node of name1 friend list, node2
        is a linked list of friend's list of name2, header is a
        number greater than 0

    Post-Conditions: temp1 is the next node in name1 friend list,
        node2 is still the name2 friend list, header is either
        0 or +1'''

def find_friends(temp1, node2, header):
    while temp1 != None:
        '''Returns the friend found'''
        friend = node2.find_mut_friend(temp1)
        '''Returns the header +1 if a friend is found and
            prints the friend'''
        header = printme(friend, header)
        '''Goes to next node in friend list 1'''
        temp1 = temp1.next
    
'''This function parses the line and puts the x and y people in the
    correct lists of friends and main linked list

    Parameters: the line of the file, ll is main linked list

    Returns: None

    Pre-Conditions: line has two names, ll is empty first run

    Post-Conditions: x and y are in ll, and x is in y's friend
        list and y is in x's friend list'''
def arrange_nodes(line, ll):
    '''returns the x and y people from line'''
    x, y = parse_file(line)
    '''if x is not in linked list it adds it'''
    if not ll.contains(x):
        ll.add(Node(x))
    '''if x is not in linked list it adds it'''
    if not ll.contains(y):
        ll.add(Node(y))
    '''if y is not in friend list of x it adds it as
        a node'''
    if not ll.get_node_of(x).get_friends().contains(y):
        ll.get_node_of(x).add_friend(Node(y))
    '''if x is not in friend list of y it adds it as
        a node'''
    if not ll.get_node_of(y).get_friends().contains(x):
        ll.get_node_of(y).add_friend(Node(x))


'''This function prints the friends that are returned from
    find mutual friends

    Parameters: friend is a node returned, header is a number
        dictates whether to print friends in common:

    Returns: header for whether its the first iteration

    Pre-Conditions: friend is a node and header is 0

    Post-Condition: friend is printed and header is
        above 0'''
def printme(friend, header):
    if friend != None:
        if header == 0:
            header += 1
            print('Friends in common:')
            print(friend)
            return header
        else:
            print(friend)
            return header
    return header
            
'''This function checks that the name is in ll

    Parameters: name which is user input, and the linked list
        ll

    Returns: None

    Pre-Conditions: name is what user puts, ll is the completed
        main list of names in file

    Post-Conditions: Error is thrown or nothing happens'''       
def name_check(name, ll):
    try:
        assert(ll.contains(name))
    except AssertionError:
        print("ERROR: Unknown person " + name)
        sys.exit(1)

'''This function parses the raw file

    Parameters: the raw line of file

    Returns: a string of first and second name

    Pre-Conditions: line is a line in the file

    Post-Conditions: x is frist name, y is second name'''
def parse_file(line):
    line = line.split()
    x = line[0]
    y = line[1]
    return x, y

'''Checks if the file is in the directory

    Parameters: the file the user inputs

    Returns: None

    Pre-Conditions: the file is user input

    Post-Conditions: Error or nothing'''
def file_check(file):
    try:
        open(file)
    except IOError:
        print('ERROR: Could not open file', file)
        sys.exit(1)












main()
