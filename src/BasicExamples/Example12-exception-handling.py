string_1 = 'str1 '
substring = ''

try :
    try :
        12.0/0.0 # will raise exception
    except :
        print substring + " is not in " + string_1
        # do some stuff that might raise another exception
        #
    else : 
        print substring + " is in "  + string_1
        # do some stuff that might raise another exception
        #
finally :
    print "No matter what, we get here!"
