lists =[2,4,6,3,6]   #["Niraj",44,32.2,"S1ngh","Rajput",2,23,44.22,"Kumar"]

lists.append(11)
lists.sort()
lists.sort(reverse=True)
lists.reverse()
lists.insert(3,4) #lists.insert(idx,el) insert element at index
lists.remove(3) #removes first occurrence of element
lists.pop(3) #removes element at idx

print("lists =",lists)
print("length of list = ",len(lists))
print(lists[1:5])
print(lists[-4:])