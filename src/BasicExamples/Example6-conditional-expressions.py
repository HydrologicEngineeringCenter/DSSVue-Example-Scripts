x, y, z = 1, 5, 5

string_1 = "debug time"
value_list = [3,2,8,10]

if(x < y or y >= x) and string_1.find("debug") != -1:
    print("first statement passed")

elif z not in value_list or (x < z * 2):
    print("second statement passed")

else:
    print("third statement passed")