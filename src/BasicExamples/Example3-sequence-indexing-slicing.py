
x = 9.375
string_4 = 'he said "I will not!"'
tuple_1 = (1, 2, "abc", x, None)
list_1 = [1, 2, "abc", x, tuple_1]
dict_1 = {"color" : "red", "size" : 10, "list" : [1, 5, 8]}

print(string_4[3])	# 4th element
print(string_4[3:5])	# 4th & 5th elements
print(list_1[0::2] )	# even elements
print(list_1[1::2] )	# odd elements
print(list_1[-1])	# last element
print(list_1[2:-1])# 3rd through next-to-last element
print(list_1[2:len(list_1)])	# 3rd through last element (also list_1[2:])
print(dict_1["size"])	# value associated with "size" key
i = len(list_1)	# length of list_1