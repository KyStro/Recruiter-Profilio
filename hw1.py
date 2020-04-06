"""
Kyle Strokes
SL: Sean Current
2/3/2020
ISTA 331 HW1

This module is meant to prompt the user for a customer to search.
When a customer is entered then the program returns the customer's 
purchase history. It then reccommends books to the user for the customer.'
"""

import pandas as pd, numpy as np, random, sqlite3, itertools as it

def isbn_to_title(conn):
    c = conn.cursor()
    query = 'SELECT isbn, book_title FROM Books;'
    return {row['isbn']: row['book_title'] for row in c.execute(query).fetchall()}


def select_book(itt):
    isbns = sorted(itt)
    print('All books:')
    print('----------')
    for i, isbn in enumerate(isbns):
        print(' ', i, '-->', isbn, itt[isbn][:60])
    print('-' * 40)
    selection = input('Enter book number or return to quit: ')
    return isbns[int(selection)] if selection else None
    
def similar_books(key, cm, pm, itt, spm): # an isbn, count_matrix, p_matrix, isbn_to_title
    bk_lst = []
    for isbn in cm.columns:
        if key != isbn:
            bk_lst.append((cm.loc[key, isbn], isbn))
    bk_lst.sort(reverse=True)
    print('Books similar to', itt[key] + ':')
    print('-----------------' + '-' * (len(itt[key]) + 1))
    for i in range(5):
        print(str(i) + ':')
        print(' ', bk_lst[i][0], '--', itt[bk_lst[i][1]][:80])
        print('  spm:', itt[spm[key][i]][:80])
        print('  p_matrix:', pm.loc[key, bk_lst[i][1]])
        
  
    
  
'''
This function takes a connection object to a bookstore transaction db and returns
 a dictionary that maps customer id's to a sorted lists of books they have
purchased in sorted order. Duplicates are omitted. 
'''
    
def get_purchase_matrix(conn):
    cur = conn.cursor()
    q = 'select * from orderitems natural join orders;'
    dic = {}
    for row in cur.execute(q).fetchall():
        #if customer isnt in dic add them if they are then
        #add the book in the row
        if row[-1] not in dic:
            dic[row[-1]] = []
            dic[row[-1]].append(row[1])
        elif row[1] not in dic[row[-1]]:
            dic[row[-1]].append(row[1])
            dic[row[-1]].sort()
    return dic
 
'''
This function takes a connection object to a bookstore db and returns a
DataFrame with index and columns that are the ISBN's of the books available
in the bookstore and initalizes data to zeros.
'''       
def get_empty_count_matrix(conn):
    cur = conn.cursor()
    q = 'select isbn from books;'
    books = []
    #row[0] is the isbn
    for row in cur.execute(q).fetchall():
        books.append(row[0])
    #dataframe with all isbn as index and columns initialized to zero
    df = pd.DataFrame(index=books,columns=books).fillna(0)
    return df

'''
This function takes an empty count matrix and a purchase matrix and fills 
the count matrix. It goes through each customer's list of ISBN's. For each ISBN 
in the list, it increments the appropriate spot on the diagonal; for how many total
purchases of that book. For each pair of books purchased by the same customer, it 
increments the intersection between the two books in the matrix. 
'''
def fill_count_matrix(cm, pm):
    # first fills in the diagonal, the number of occurences of a book
    vals = list(pm.values())
    for order in vals:
        for isbn in order:
            cm.loc[isbn,isbn] += 1
        # next we use itertools to find all permutations of each order
        # the permuatations are stored as tuples so we unbox them in for loop
        perms = list(it.permutations(order,2))
        for p in perms:
            cm.loc[p[0],p[1]] += 1
  
'''
This function returns the matrix which is the probability that a customer has
purchased the column book given that that customer has purchased the row book.
The diagonal is set to -1 because we do not want to recommend the same book a
customer has ordered.
'''      
def make_probability_matrix(cm):
    for row in cm.index:
        dom = cm.loc[row,row]
        for col in cm.columns:
            if row == col:
                continue
            num = cm.loc[row,col]
            cm.loc[row,col] = num/dom
        cm.loc[row,row] = -1
    return cm

'''
This function takes a probability matrix and returns a dictionary that maps ISBN's 
to a list of the 15 books most likely to be purchased by a customer who has 
purchased the key book in descending order of likelihood.
'''
def sparse_p_matrix(p_matrix):
    """
    Maps ISBN's to lists of ISBN's of other books sorted in descending order
    of likelihood that the other book was purchased if the key was purchased.
    Now that I thought of this way, we could map to index objects or arrays.
    """
    spm = {}
    for book in p_matrix.index:
        spm[book] = list(p_matrix.loc[book].sort_values(ascending=False, kind='mergesort')[:15].index)
    return spm
    
'''
This function takes a connection object and returns an integer customer id or None, 
depending upon user input. If user input is not a valid integer then defaults to None.
'''
def get_cust_id(conn):
    cur = conn.cursor()
    q = 'select cust_id as CID, last ||\', \'|| first as Name from customers;'
    print('CID       Name\n-----     -----')
    valid_nums = []
    for row in cur.execute(q).fetchall():
        print('    '+str(row[0])+'     '+row[1])
        valid_nums.append(row[0])
    print('---------------')
    i = input('Enter customer number or enter to quit: ')
    if is_num(i) and int(i) in valid_nums:
        i = int(i)
        return i
    return None

'''
This is a helper function for get_cust_id(conn), it checks if input s
is a integer, if so, returns True, else; False.
'''
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

'''
This function takes a customer id, a list of ISBN's that the customer has 
purchased, and a connection to the db, and returns a string containing the 
customer's purchase history as titles instead of ISBN's
'''  
def purchase_history(cid, isbns, conn):
    cur = conn.cursor()
    q = 'select first || \' \' || last from customers where cust_id={}'.format(cid)  
    name = cur.execute(q).fetchone()[0]
    s = 'Purchase history for {}\n'.format(name)
    s+='-'*(len(s)-1)+'\n'
    w = 'select isbn, book_title from OrderItems natural join orders natural join books where cust_id={}'.format(cid)
    for row in cur.execute(w).fetchall():
        s+=row[1]+'\n'
    s+='-'*40+'\n'
    return s

'''
This function takes a customer id and a connection. It returns an ISBN chosen 
randomly from the customers most recent order. It makes a list of the ISBN's in the 
most recent order and uses random.randrange to randomly index into the list to 
grab a book.
'''
def get_recent(cid, conn):
    cur = conn.cursor()
    q = 'select order_num from orders where cust_id={} order by order_date desc;'.format(cid)
    rec_order = cur.execute(q).fetchone()[0]
    q = 'select isbn from orderitems where order_num={}'.format(rec_order)
    isbns = [row[0] for row in cur.execute(q).fetchall()]
    r = random.randrange(len(isbns))
    return isbns[r]

'''
This function takes a customer id, a sparse probability matrix, purchase history ISBN 
list, and a connection. It uses the previous function to randomly grab a book from the 
customer's most recent purchase. Then gets the customer's name. After, gets the two books most similar 
to the recently purchased book, not including any books already purchased by the customer. 
If recommender has not books to recommend: Prints: "Out of ideas, go to Amazon.
'''       
def get_recommendation(cid, spm, pur_hist, conn):
    isbn = get_recent(cid, conn)
    cur = conn.cursor()
    q = 'select first||\' \'|| last from customers where cust_id={}'.format(cid)
    name = cur.execute(q).fetchone()[0]
    recs = spm[isbn]
    recs = [b for b in recs if b not in pur_hist][:2]
      

    if isbn in recs:
        recs.remove(isbn)
    head = 'Recommendations for {}\n'.format(name)
    head += '-'*(len(head)-1)+'\n'
    if (len(recs) == 0):
        head += "Out of ideas, go to Amazon\n"
    for isbn in recs:
        q = 'select book_title from books where isbn={}'.format(isbn)
        book = cur.execute(q).fetchone()[0]
        head += book+'\n'
    return head
    
def main1():
    conn = sqlite3.connect('small.db')
    conn.row_factory = sqlite3.Row
    purchase_matrix = get_purchase_matrix(conn)
    count_matrix = get_empty_count_matrix(conn)
    fill_count_matrix(count_matrix, purchase_matrix)
    p_matrix = make_probability_matrix(count_matrix)
    spm = sparse_p_matrix(p_matrix)
    ######
    
    itt = isbn_to_title(conn)
    selection = select_book(itt)
    print(itt)
    while selection:
        similar_books(selection, count_matrix, p_matrix, itt, spm)
        input('Enter to continue:')
        selection = select_book(itt)
      
    ######
    cid = get_cust_id(conn)
    while cid:
        print()
        titles = purchase_history(cid, purchase_matrix[cid], conn)
        print(titles)
        print(get_recommendation(cid, spm, purchase_matrix[cid], conn))
        input('Enter to continue:')
        cid = get_cust_id(conn)
    
def main2():
    conn = sqlite3.connect('small.db')
    conn.row_factory = sqlite3.Row
    
    purchase_matrix = get_purchase_matrix(conn)
    print('*' * 20, 'Purchase Matrix', '*' * 20)
    print(purchase_matrix)
    print()
    
    count_matrix = get_empty_count_matrix(conn)
    print('*' * 20, 'Empty Count Matrix', '*' * 20)
    print(count_matrix)
    print()
    
    fill_count_matrix(count_matrix, purchase_matrix)
    print('*' * 20, 'Full Count Matrix', '*' * 20)
    print(count_matrix)
    print()
    
    p_matrix = make_probability_matrix(count_matrix)
    print('*' * 20, 'Probability Matrix', '*' * 20)
    print(p_matrix)
    print()
    
    spm = sparse_p_matrix(p_matrix)
    print('*' * 20, 'Sparse Probability Matrix', '*' * 20)
    print(spm)
    print()
    
    ######
    itt = isbn_to_title(conn)
    print('*' * 20, 'itt dict', '*' * 20)
    print(itt)
    print()
    
    
    selection = select_book(itt)
    while selection:
        similar_books(selection, count_matrix, p_matrix, itt, spm)
        input('Enter to continue:')
        selection = select_book(itt)
    ######
    cid = get_cust_id(conn)
    while cid:
        print()
        titles = purchase_history(cid, purchase_matrix[cid], conn)
        print(titles)
        print(get_recommendation(cid, spm, purchase_matrix[cid], conn))
        input('Enter to continue:')
        cid = get_cust_id(conn)
        
def main3():
    conn = sqlite3.connect('small.db')
    conn.row_factory = sqlite3.Row
    purchase_matrix = get_purchase_matrix(conn)
    count_matrix = get_empty_count_matrix(conn)
    fill_count_matrix(count_matrix, purchase_matrix)
    p_matrix = make_probability_matrix(count_matrix)
    spm = sparse_p_matrix(p_matrix)
    cid = get_cust_id(conn)
    print(purchase_history(cid, [], conn))

    
if __name__ == "__main__":
    main1()
    
    
    
    
    
    
    
    
