

# defining functions is a powerful tool to manage complexity
# * program is easy to add another equation
# * put important information up front that future programmer (usually you!) can use
def f1(x):
    return 3*x**3 - 5.0


# f:  function
# xstart: is starting x value
# tolerance: positive value representing close enought to zero by tolerance amount
# sometimes the better solution also takes less code, but takes time to find.
def newton_solver(f,xstart,tolerance):
    x = xstart 
    dx = 0.00001
    counter = 0
    while (abs(f(x)) > tolerance):
        print("x= "+str(x)+"f(x)="+str(f(x)))
        m = (f(x+dx)-f(x))/dx
        x=x - f(x)/m  # newton-raphson method
        counter=counter +1
        if counter > 1000: break
    print("x= "+str(x)+"f(x)="+str(f(x)))
    return x


# high level program begins here
# I really like programs that are just a few lines of code at the highest level.
# makes is more like reading a book, so you can read what parts your are interested in
# check:  https://www.wolframalpha.com/input/?i=y%3D3x%5E3-5
x = newton_solver(f1,1,0.0001)
print("solution = "+str(x))
    