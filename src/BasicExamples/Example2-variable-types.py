from hec.script import Constants

# set some integer values
i = 0
j = 1
k = -10998
m = True
 
# set a long integer
n = 79228162514264337593543950336L
 
# set some floating-point values
x = 9.375
y = 6.023e23
z = -7.2e-3
t = Constants.UNDEFINED
 
# set some strings
string_1 = "abc"
string_2 = 'xyz'
string_3 = "he said \"I won't!\""
print (string_3)
string_4 = 'he said "I will not!"'
string_5 = """this is a
              multi-line string"""
 
# set a tuple - tuples are contained within ()
tuple_1 = (1, 2, "abc", x, None)
 
# set a list - lists are contained within []
list_1 = [1, 2, "abc", x, tuple_1]
 
# set a dictionary, using key : value syntax
# dictionaries are contained within {}
dict_1 = {"color" : "red", "size" : 10, "list" : [1, 5, 8]}
 
# multiple assignment
a, b, c = string_1
a, b, c = "abc"
a, b, c, d, e = tuple_1
a, b, c, d, e = (1, 2, "abc", x, None)
a, b, c, d, e = 1, 2, "abc", x, None     # "Naked" tuple assignment
a, b, c, d, e = list_1
a, b, c, d, e = [1, 2, "abc", x, tuple_1]
a, b, c = dict_1
a, b, c = {"color" : "red", "size" : 10, "list" : [1, 5, 8]}
