###Each element in the set must be unique & immutable.

set1 = {2,3,4,6,3,7}
set2 = {0,9,8,5}

# null_set = set()

set1.add(1)
set1.remove(4)
#set1.clear() #empties the set
set1.pop() #removes a random value

print(set1.pop()) #prints a random el

un_set = set1.union(set2)
print(un_set)

in_set = set1.intersection(set2)
print(in_set)
