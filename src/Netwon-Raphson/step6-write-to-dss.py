from hec.heclib.dss import HecDss
from hec.io import PairedDataContainer

# defining functions is a powerful tool to manage complexity
# int his example it is easy to add another equation
# put important information up front that future programmer (usually you!) 
def f1(x):
    return 3*x**3 - 5.0

# saves function (x,y) values to a file.
# func -- function to write values to DSS
# x1 - starting x value
# x2 - ending x value
# path - dss path /a/b/x-y/d/e/f/
# fileName - output dss file
def write_to_dss(func,x1,x2,path,fileName):
    
    pdc = PairedDataContainer() # constructor
    pdc.fullName = path
    ylist = []
    xlist = []
    step = (x2-x1)/100.0
    x=x1
    while x <=x2 :
        ylist.append(func(x))
        xlist.append(x)
        x = x + step

    pdc.xOrdinates = xlist
    pdc.yOrdinates = [ylist]
    pdc.numberCurves = 1
    pdc.numberOrdinates = len(xlist)
    pdc.xparameter = "x"
    pdc.yparameter = "y"

    dss = HecDss.open(fileName)
    dss.put(pdc)
    dss.done()

        




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
# check function here:  https://www.wolframalpha.com/input/?i=y%3D3x%5E3-5
x = newton_solver(f1,1,0.0001)
print("solution = "+str(x))

write_to_dss(f1,-4,4,"/demo/chicago/x-y///v1/",R"c:\temp\func.dss")    
