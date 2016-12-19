import graphics
from graphics import * #color_rgb
import math
import random, time
from PIL import Image
from Tkinter import Tk, Canvas, PhotoImage, mainloop
from math import sin

global calls
calls = 0
global base
base = 0
randomiser = 1
precision = 50
max_iterations = 255
max_magnitude = 256
win_max_x = 640
win_max_y = 640
scale = 100
x_offset = -1.793
y_offset = -.02769
x_offset_end = -1.741
y_offset_end = .0238

x_offset = -2.25
y_offset = -1.5
x_offset_end = .75
y_offset_end = 1.5
xstep = 16
ystep = 16

base = 255/max_iterations
global canvas
#win = graphics.GraphWin("Mandlebrot", win_max_x, win_max_y)

def main():
    win = graphics.GraphWin("Random Circles", 300, 300)
    win.getMouse()
    for i in range(50):
        r = random.randrange(256)
        b = random.randrange(256)
        g = random.randrange(256)

        xx = random.randrange(300)
        yy = random.randrange(300)
        color = color_rgb(r, g, b)

        radius = random.randrange(3, 40)
        x = random.randrange(5, 295)
        y = random.randrange(5, 295)

        circle = Circle(Point(x,y), radius)
        circle.setFill(color)
        #circle.draw(win)

        rectangle = graphics.Rectangle(Point(x,y), Point(x+radius, y+radius))
        rectangle.setFill(color)
        rectangle.draw(win)

    win.getMouse()
    win.close()

def SetupCanvas():
    global canvas
    master = Tk()

    canvas_width = win_max_x
    canvas_height = win_max_y
    canvas = Canvas(master, 
            width=win_max_x,
            height=win_max_y)
    canvas.pack()
    master.update()
        #point = graphics.Point(xx, yy)
        #point.setFill(color)
        #point.draw(win)
        #time.sleep(.05)

    #win.promptClose(win.getWidth()/2, 20)

def Mandelbrot():
    #win = graphics.GraphWin("Mandlerot", win_max_x, win_max_y)
    #iterate over size of graphics window
    for x in range(0, win_max_x + 1, xstep):
        for y in range(0, win_max_y + 1, ystep):

            a = x_offset + (3.0 /win_max_x) * x
            b = y_offset + (3.0 /win_max_y) * y
            count = 0
            re = a
            im = b
            magnitude = 0

            while count < max_iterations and abs(magnitude) < precision:
                count += 1

                partial_re = re * re
                partial_im = im * im
                partial_re_im = re * im

                re = partial_re - partial_im + a
                im = partial_re_im + partial_re_im + b
                magnitude = partial_re + partial_im

                #realsave = re
                #re = re * re - im * im + a
                #im = 2 * realsave * im  + b

                #magnitude = re*re + im*im
                #print "a, b (", a,b, ") re, im (", re, im, ") mag", magnitude

            point = graphics.Point(x, y)
            #print "(x,y) (", x,y, ") count: ", count ,"magnitude: " ,magnitude
            if count < precision :
                #drawColor = color_rgb(255, abs(math.ceil(255*math.sin(count))), count)
                drawColor = color_rgb(128, count*5, count*5)
                #print "color", drawColor
                point.setFill(drawColor)

            else :
                point.setFill("black")
            point.draw(win)
    time.sleep(60*60*24)


def MandlebrotFunction (x_max, y_max, xlocation, ylocation, max_iterations, max_magnitude):
    global calls
    calls = calls + 1
    a = x_offset + (abs(x_offset - x_offset_end) /x_max) * xlocation
    b = y_offset + (abs(y_offset - y_offset_end) /y_max) * ylocation
    iterations = 0
    magnitude = 0
    re= a
    im= b
    while iterations < max_iterations and abs(magnitude) < max_magnitude:
        iterations += 1

        partial_re = re * re
        partial_im = im * im
        partial_re_im = re * im

        re = partial_re - partial_im + a
        im = partial_re_im + partial_re_im + b
        magnitude = partial_re + partial_im

    if iterations >= max_iterations:
        return 0
    else :
        return iterations

def Test():
    #win = graphics.GraphWin("Mandlerot", win_max_x, win_max_y)
    #iterate over size of graphics window
    global base
    for x in range(0, win_max_x + 1, xstep):
        for y in range(0, win_max_y + 1, ystep):
            iterations = MandlebrotFunction(win_max_x, win_max_y, x, y, max_iterations, max_magnitude)

            point = graphics.Point(x, y)
            if iterations >= 0:
                color = iterations * base
                color = abs(math.ceil(255*math.sin(iterations)))
                drawColor = color_rgb(128, color, color)
                point.setFill(drawColor)
            else:
                point.setFill("black")
            point.draw(win)
    print "total calls to mandlebrot ", calls
    win.getMouse()
    win.close()


def BoxMethod():

    #iterate over size of graphics window
    done = False
    x = 0
    y = 0
    my_xstep = xstep
    my_ystep = ystep
    iterations1 = -1
    iterations2 = 0
    iterations3 = 0
    iterations4 = 0
    sub_dividing_level = 0

    while done == False:
        if y >= win_max_y:
            x += my_xstep
            y = 0
        if x >= win_max_x:
            done = True

        #if iterations1 == -1:
        iterations1 = MandlebrotFunction(win_max_x, win_max_y, x, y, max_iterations, max_magnitude)
        iterations2 = MandlebrotFunction(win_max_x, win_max_y, x+my_xstep-1, y, max_iterations, max_magnitude)
        iterations3 = MandlebrotFunction(win_max_x, win_max_y, x+my_xstep-1, y+my_ystep-1, max_iterations, max_magnitude)
        iterations4 = MandlebrotFunction(win_max_x, win_max_y, x, y+my_ystep-1, max_iterations, max_magnitude)

        #iterations5 = MandlebrotFunction(win_max_x, win_max_y, x+my_xstep/2, y+my_ystep/2, 100, 50)

        if iterations1 == iterations2 and iterations2 == iterations3 and iterations3 == iterations4:
            rectangle = graphics.Rectangle(Point(x,y), Point(x+my_xstep-1, y+my_ystep-1))
            color = iterations1 * base
            #color = abs(math.ceil(255*math.sin(iterations1)))
            drawColor = color_rgb(128,color,color)
            rectangle.setFill(drawColor)
            rectangle.setOutline(drawColor)
            rectangle.draw(win)
        else:
            MandlebrotRecursive(x,y,x+my_xstep-1, y+my_ystep-1)

        y += ystep

    print "total calls to mandlebrot ", calls
    win.getMouse()
    win.close()


def BoxMethod2():

    #iterate over size of graphics window
    done = False
    x = 0
    y = 0
    my_xstep = xstep
    my_ystep = ystep
    iterations1 = -1
    iterations2 = 0
    iterations3 = 0
    iterations4 = 0
    sub_dividing_level = 0

    while done == False :
        if y >= win_max_y:
            x += my_xstep
            y = 0
        if x >= win_max_x:
            done = True

        MandlebrotRecursive(x,y,x+my_xstep, y+my_ystep, -1, -1, -1, -1)

        y += ystep

    print "total calls to mandlebrot ", calls
    win.getMouse()

def BoxMethod3():
    
    SetupCanvas()
    #iterate over size of graphics window
    done = False
    x = 0
    y = 0
    my_xstep = xstep
    my_ystep = ystep
    iterations1 = -1
    iterations2 = 0
    iterations3 = 0
    iterations4 = 0
    sub_dividing_level = 0

    while done == False :
        if y >= win_max_y:
            x += my_xstep
            y = 0
        if x >= win_max_x:
            done = True

        MandelbrotDivide(x,y,x+my_xstep, y+my_ystep, -1, -1, -1, -1)

        y += ystep

    print "total calls to mandlebrot ", calls, "(xstep, ystep) (", xstep, ystep,")"
    print "this is a sample {0}, {1}, {2}".format("test", "second", "three")
    
    t = True 
    while t == True:
        canvas.update()
        time.sleep(.1) # give up thread 

    canvas.bind("<Button-1>", click)
    #mainloop()

def Plot(shape, iterations):
    global base
    
    if iterations != -1:
        color = iterations * base - 1
        #color = abs(math.ceil(255*math.sin(iterations1)))
        drawColor = color_rgb(color,color,color)
    else:
        drawColor = color_rgb(0,0,0)

    shape.setFill(drawColor)
    shape.setOutline(drawColor)
    shape.draw(win)
    return
    img = PhotoImage(width = x, height = y)
    canvas.create_image((0, 0), image = img, state = "normal", anchor = NW)
    pixels=" ".join(("{"+" ".join(('#%02x%02x%02x' % iterations for i in xm))+"}" for j in ym))
    img.put(pixels)  

def PlotCanvas(p1, p2, color):
    global canvas
    canvas.create_rectangle(p1.x, p1.y, p2.x, p2.y,fill=color, outline=color)



def click(event):
    exit()
    return
    global canvas
    canvas.create_line(0, 50, win_max_x, 55, fill="#476042")
    canvas.create_rectangle(0,0, 100, 100,fill="#476042")
    drawColor = color_rgb(255,128,126)

    x1 = random.randrange(300)
    y1 = random.randrange(300)
    
    PlotCanvas(Point(x1, y1), Point(x1+10, y1+20), drawColor)
    
    exit()



def paintTest():
    global canvas
    master = Tk()

    canvas_width = win_max_x
    canvas_height = win_max_y
    canvas = Canvas(master, 
            width=win_max_x,
            height=win_max_y)
    canvas.pack()


    y = int(win_max_y / 2)
    #w.create_line(0, y, win_max_x, y, fill="#476042")
    img = PhotoImage(master = master, width=win_max_x, height=win_max_y)
    #img = w.create_image(0,0, state="normal")
    canvas.bind("<Button-1>", click)

    mainloop()
    return
    for x in range(0, win_max_x):
        for y in range(0, win_max_y):
            color = 128 + int(64 * sin(x*y/16.0))
            drawColor = color_rgb(255,color,color)
            img.put(drawColor, (x,y))    

    w.create_image((win_max_x/2,win_max_y/2), image=img, state="normal")
    #w.create_image((win_max_x/2, win_max_y/2), image=img, state="normal")


    mainloop()
    return

    WIDTH, HEIGHT = 640, 480

    window = Tk()
    canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
    canvas.pack()
    img = PhotoImage(width=WIDTH, height=HEIGHT)
    canvas.add
    #canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

    for x in range(4 * WIDTH):
        y = int(HEIGHT/2 + HEIGHT/4 * sin(x/80.0))
        img.put("#ffffff", (x//4,y))

   #win.getMouse()
    return

    img = Image.New( 'RGB', (255,255), "black") # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every pixel:
        for j in range(img.size[1]):
            pixels[i,j] = (i, j, 100) # set the colour accordingly

    img.show()

    return

    master = Tk()

    canvas = Canvas(master, 
            width=win_max_x, 
            height=win_max_y)
    canvas.pack()

    #img = PhotoImage(file="myimage.jpg")
    #canvas.create_image(20,20, anchor=NW, image=img)
    
    return

    #pixels = " ".join('#%02x%02x%02x')
    img = Image.new( 'RGB', (255,255), "black") # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every pixel:
        for j in range(img.size[1]):
            pixels[i,j] = (i, j, 100) # set the colour accordingly

    #img.Show(win)

    myImage = graphics.Image(pixels)
    myImage.draw(window)
    #image.draw(win)
    
def MandelbrotDivide(x1, y1, x2, y2, it1, it2, it3, it4):
    global base
    if x2-x1 <=1  or y2 - y1 <= 1 :
        if it1 == -1 :
            iterations1 = MandlebrotFunction(win_max_x, win_max_y, x1, y1, max_iterations, max_magnitude)
        else:
            iterations1 = it1

        color = iterations1 * base
        drawColor = color_rgb(color,color,color)
        PlotCanvas(Point(x1, y1), Point(x2, y2), drawColor)

        return

    if it1 == -1:
        iterations1 = MandlebrotFunction(win_max_x, win_max_y, x1, y1, max_iterations, max_magnitude)
    else:
        iterations1 = it1
    if it2 == -1:
        iterations2 = MandlebrotFunction(win_max_x, win_max_y, x2, y1, max_iterations, max_magnitude)
    else:
        iterations2 = it2
    if it3 == -1:
        iterations3 = MandlebrotFunction(win_max_x, win_max_y, x2, y2, max_iterations, max_magnitude)
    else:
        iterations3 = it3
    if it4 == -1:
        iterations4 = MandlebrotFunction(win_max_x, win_max_y, x1, y2, max_iterations, max_magnitude)
    else:
        iterations4 = it4

    iterations5 = MandlebrotFunction(win_max_x, win_max_y, x1 + (x2-x1)/2, y1 + (y2-y1)/2, max_iterations, max_magnitude)

    if iterations1 == iterations2 and iterations2 == iterations3 and iterations3 == iterations4 and iterations4 == iterations5:
        color = iterations1 * base
        drawColor = color_rgb(color,color,color)
        PlotCanvas(Point(x1, y1), Point(x2, y2), drawColor)
    else:
        MandelbrotDivide(x1, y1, x1 + (x2-x1)/2, y1 + (y2-y1)/2, iterations1, -1, iterations5, -1)
        MandelbrotDivide(x1 + (x2-x1)/2, y1, x2, y1 + (y2-y1)/2, -1, iterations2, -1, iterations5)
        MandelbrotDivide(x1, y1 + (y2-y1)/2, x1 + (x2-x1)/2, y2, -1, iterations5, iterations3, -1)
        MandelbrotDivide(x1 + (x2-x1)/2, y1 + (y2-y1)/2, x2, y2, iterations5, -1, -1,  iterations4)

def MandlebrotRecursive(x1, y1, x2, y2, it1, it2, it3, it4):
    global base
    if x2-x1 <=1  or y2 - y1 <= 1 :
        if it1 == -1 :
            iterations1 = MandlebrotFunction(win_max_x, win_max_y, x1, y1, max_iterations, max_magnitude)
        else:
            iterations1 = it1

        #iterations1 = MandlebrotFunction(win_max_x, win_max_y, x1, y1, max_iterations, max_magnitude)
        #point = graphics.Point(x1, y1)

        rectangle = graphics.Rectangle(Point(x1, y2), Point(x2, y2))
        Plot(rectangle, iterations1)

        return

    if it1 == -1:
        iterations1 = MandlebrotFunction(win_max_x, win_max_y, x1, y1, max_iterations, max_magnitude)
    else:
        iterations1 = it1
    if it2 == -1:
        iterations2 = MandlebrotFunction(win_max_x, win_max_y, x2, y1, max_iterations, max_magnitude)
    else:
        iterations2 = it2
    if it3 == -1:
        iterations3 = MandlebrotFunction(win_max_x, win_max_y, x2, y2, max_iterations, max_magnitude)
    else:
        iterations3 = it3
    if it4 == -1:
        iterations4 = MandlebrotFunction(win_max_x, win_max_y, x1, y2, max_iterations, max_magnitude)
    else:
        iterations4 = it4

    iterations5 = MandlebrotFunction(win_max_x, win_max_y, x1 + (x2-x1)/2, y1 + (y2-y1)/2, max_iterations, max_magnitude)

    if iterations1 == iterations2 and iterations2 == iterations3 and iterations3 == iterations4 and iterations4 == iterations5:
        rectangle = graphics.Rectangle(Point(x1,y1),Point(x2, y2))
        Plot(rectangle, iterations1)
    else:
        MandlebrotRecursive(x1, y1, x1 + (x2-x1)/2, y1 + (y2-y1)/2, iterations1, -1, -1, -1)
        MandlebrotRecursive(x1 + (x2-x1)/2, y1, x2, y1 + (y2-y1)/2, -1, iterations2, -1, -1)
        MandlebrotRecursive(x1, y1 + (y2-y1)/2, x1 + (x2-x1)/2, y2, -1, -1, iterations3, -1)
        MandlebrotRecursive(x1 + (x2-x1)/2, y1 + (y2-y1)/2, x2, y2, -1, -1, -1,  iterations4)

#paintTest()
#3Test()
BoxMethod3()
#main()
