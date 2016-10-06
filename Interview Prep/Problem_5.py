"""
Find the element in a singly linked list that's m elements from the end. For example, if a linked list has 
5 elements, the 3rd element from the end is the 3rd element. The function definition should look like 
"question5(ll, m)", where ll is the first node of a linked list and m is the "mth number from the end". 
You should copy/paste the Node class below to use as a representation of a node in the linked list. Return 
the value of the node at that position.
"""

class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None

def question5(ll, m):
    i = ll
    j = ll
    #increment i m spaces forward from the start
    for val in range(m):
        if i is None:
            return None
        i = i.next
    #when i is none, j is the ith element from the end
    while i is not None:
        i = i.next
        j = j.next
    return j.data


ll = Node(1)
ll.next = Node(2)
ll.next.next = Node(3)
ll.next.next.next = Node(4)
ll.next.next.next.next = Node(5)
ll.next.next.next.next.next = Node(6)



print question5(ll, 1)
print question5(ll, 2)
print question5(ll, 3)
print question5(ll, 4)
print question5(ll, 5)
print question5(ll, 6)
print question5(ll, 7)



