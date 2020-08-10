# this is the main script group
x1=10
x2=5
dist = x2 - x1
if dist > 100.:
    # this is the "if" conditional group
    y = dist / 2.
    z = y ** 2.
else :
    # this is the "else" conditional group
    y = dist 
    z = y ** 2. / 1.5
# back to main script group
q = y * z
print(q)