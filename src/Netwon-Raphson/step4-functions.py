
# defining functions is a powerful tool to manage complexity
# * program is easy to add another equation
# * put important information up front that future programmer (usually you!) can use
def f1(x):
    return 3*x**2 - 5.0

# solver finds and returns a x value that is close to zero
# f :  function to find root (x = 0)
# xstart starting guess for root
# tolerance: positive value representing close enought to zero by tolerance amount
def solver(f,xstart,tolerance):
    x = xstart
    y=f(x)
    best = [x,y]
    counter = 0
    dx = 0.01
    while abs(y) > tolerance:
        y=f(x)
        if( abs(y) < abs(best[1]) ): best = [x,y]
        print("x= "+str(x)+", y= "+str(y))
        x=x+dx
        counter=counter +1
        if counter > 1000: break
    return best[0]




# high level program begins here
# I really like programs that are just a few lines of code at the highest level.
# makes is more like reading a book, so you can read what parts your are interested in
# check:  https://www.wolframalpha.com/input/?i=y%3D3x%5E3-5
answer = solver(f1,1,0.01)
    