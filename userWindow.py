from Tkinter import *
from scroll import VerticalScrolledFrame
import webbrowser
import tkSimpleDialog,tkFileDialog
from html_source import *
from tkColorChooser import askcolor
from addComponents import *

import pickle
"""*[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]"""
shapeObjArr = []
shapeObjCount=0
shapeobAr = []

shape="rectangle"
fo = open("button.html", "wb+")
flag = 0
prev_x = 0
prev_y = 0
shapeob = object
operation = "draw"
victim = 0

move_prev_x = 0
move_prev_y = 0

event_x = 0
event_y = 0
nest_vict = 0

button_text = "none"
""""""
check_to_replace=""

root = Tk()

root.minsize(1300, 700)
root.maxsize(1300, 700)
root.title("User Window")

nav_menu_opt=""

"""*"""

def draw_rectangle():
    global operation, shape
    operation = "draw"
    shape = "rectangle"

def draw_circle():
    global operation, shape
    operation = "draw"
    shape = "circle"
    print "circle pressed"

def draw_line():
    global operation, shape
    operation = "draw"
    shape = "line"
    print "line pressed"


def onLeftDrag(event):
    global flag,prev_x,prev_y, shape, shapeob, operation, victim, move_prev_x, move_prev_y, event_x, event_y, nest_vict
    if operation == "draw":
        """***"""
        # Left drag started
        if flag == 0:
            # save initial coordinates
            print "Shape: ", shape
            prev_x = event.x
            prev_y = event.y
            flag = 1
        else:
            # trace cursor and draw shape using current and initial coordinates
            co = prev_x, prev_y, event.x, event.y

            # for nested divs
            event_x = prev_x
            event_y = prev_y
            nest_vict = findObject()
            # delete previous shape
            w.delete(shapeob)
            if shape == "rectangle":
                shapeob = w.create_rectangle(co, outline="black")
            elif shape == "circle":
                shapeob = w.create_oval(co, outline="black")
            elif shape == "line":
                shapeob = w.create_line(co, fill="black")
    elif operation == "resize":
        co = shapeObjArr[victim][0], shapeObjArr[victim][1], event.x, event.y
        shapeObjArr[victim] = co
        if flag != 0:
            w.delete(shapeob)
        else:
            print "resize"
            print "selected: ", shapeobAr[victim]
            w.delete(shapeobAr[victim])
        if shape == "rectangle":
            flag = 1
            shapeob = w.create_rectangle(co, outline = "black")
        elif shape == "circle":
            flag = 1
            shapeob = w.create_oval(co, outline = "black")
        elif shape == "line":
            flag = 1
            shapeob = w.create_line(co, fill = "black")

    elif operation == "move":
        if flag == 0:
            print "move"
            move_prev_x = event.x
            move_prev_y = event.y
            flag = 1
            w.delete(shapeobAr[victim])
        else:
            x_offset = event.x - move_prev_x
            y_offset = event.y - move_prev_y
            move_prev_x = event.x
            move_prev_y = event.y
            lst = list(shapeObjArr[victim])
            lst[0] += x_offset
            lst[2] += x_offset
            lst[1] += y_offset
            lst[3] += y_offset
            co = lst
            shapeObjArr[victim] = lst
            w.delete(shapeob)
            if shape == "rectangle":
                shapeob = w.create_rectangle(co, outline="black")
            elif shape == "circle":
                shapeob = w.create_oval(co, outline="black")
            elif shape == "line":
                shapeob = w.create_line(co, fill ="black")


def releaseLeftDrag(event):
    global flag,prev_x,prev_y,fo,shapeObjCount,shapeObjArr, shapeob, operation, victim,nav_menu_opt, nest_vict
    flag = 0
    if operation == "resize":
        co = shapeObjArr[victim]
        nm = shapeobAr[victim]
        cds = w.coords(nm)
        coords = shapeObjArr[victim][0], shapeObjArr[victim][1], event.x, event.y
        resizeInHtml(victim, coords)

    if operation == "move":
        co = shapeObjArr[victim]
        coords = shapeObjArr[victim][0], shapeObjArr[victim][1], event.x, event.y
        moveInHtml(victim,coords)
    else:
        co = prev_x, prev_y, event.x, event.y
    print "shapeob: ", shapeob
    if operation != "draw":
        shapeObjArr[victim] = co
        shapeobAr[victim] = shapeob
        operation = "draw"
    else:
        print "objCount: ", shapeObjCount
        shapeObjArr.append(co)
        shapeobAr.append(shapeob)
        print "saved obj: ", shapeobAr[shapeObjCount]
        # print("in release left drag")
        """if (nav_menu_opt == "table"):
            drawTable(co)"""
        # print("in release left drag")

        if(nest_vict==-1):
            parObjCo=0,0,0,0
        else:
            parObjCo=shapeObjArr[nest_vict]
        write_to_html(nest_vict, "button", co, shapeObjCount,shape,parObjCo)
        # webbrowser.open_new_tab("index.html")
        shapeObjCount += 1
    print "Coordinates: ", co
    over_button = button_text = "none"
    shapeob = 0

"""Root functions called when an option from popup is selected"""
# Resize
def resize_root():
    # get event
    global event_x, event_y, operation, victim
    victim = findObject()
    operation = "resize"
    print "victim: ", victim

# Move
def move_root():
    global event_x, event_y, operation, victim
    victim = findObject()
    operation = "move"
    print "victim: ", victim
# Delete
def remove_root():
    print "remove"
    global event_x, event_y, operation, victim,shapeObjCount
    victim = findObject()
    delete(victim)
    nm = shapeobAr[victim]
    w.delete(nm)
    shapeObjArr.remove(shapeObjArr[victim])
    shapeobAr.remove(shapeobAr[victim])
    shapeObjCount-=1

over_button = "none"
def addText():
    global  check_to_replace
    #name of button
    button_text = tkSimpleDialog.askstring("Input Text","Enter Text")
    print button_text;
    victim = findObject()

    #size of text    delete(victim)

    text_size = tkSimpleDialog.askinteger("Input Text","Size of text")
    text_family = tkSimpleDialog.askstring("Input Text","font family")
    text_color = tkSimpleDialog.askstring("Input Text", "Text color")
  #  text_family = tkSimpleDialog.Radiobutton.
    # print var
    search_text1="font-size:;"
    rep_text1="\t\t\tfont-size: "+str(text_size)+"px;\n"

    search_text2="font-family:;"
    rep_text2="\t\t\tfont-family: "+text_family+";\n"

    search_text3 = "color:;"
    rep_text3 = "\t\t\tcolor: " + text_color + ";\n"
    w.create_text((shapeObjArr[victim][0] + shapeObjArr[victim][2]) / 2, shapeObjArr[victim][1] + 10, fill=text_color,text=button_text)
    alterCSSFile(victim, search_text1, rep_text1, check_to_replace)
    alterCSSFile(victim, search_text2, rep_text2, check_to_replace)
    alterCSSFile(victim, search_text3, rep_text3, check_to_replace)
    #print "%"+check_to_replace
    if(check_to_replace=="anchor"):
        replace_text(victim, "<!--anchor text-->", button_text)
    elif (check_to_replace == "paragraph"):
        replace_text(victim, "<!--paragraph text-->", button_text)

def addImage():
    print "hoy na be"
    global over_button
    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    print (root.filename)
    victim = findObject()
    width = shapeObjArr[victim][2] - shapeObjArr[victim][0];
    height = shapeObjArr[victim][3] - shapeObjArr[victim][1];
    #addImageTag(victim, root.filename)
    addTag(victim, shapeObjArr[victim], "img", -1)
    addPath(victim, root.filename, height, width, "img", -1)
    over_button = "image"


def addLink():
    global over_button
    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("jpeg files", "*.jpg"),("all files", "*.*")))
    print (root.filename)
    victim = findObject()
    addLinkToAnchorTag(victim, root.filename)

def addColor():
    victim = findObject()
    color = askcolor()
    find = "background-color:;"
    rep_color = "\t\t\t\tbackground-color: "+color[1]+";\n"
    alterCSSFile(victim,find,rep_color,"")
    ob = shapeobAr[victim]
    w.itemconfig(ob, fill=color[1])


def addButton():
    global check_to_replace
    check_to_replace="anchor"
    print 'button'
    victim=findObject()
    addTag(victim,shapeObjArr[victim],"anchor", -1)

def addParagraph():
    global check_to_replace
    check_to_replace = "paragraph"
    print 'paragraph'
    victim=findObject()
    addTag(victim,shapeObjArr[victim],"paragraph", -1)

def addTable():
    victim = findObject()
    drawTable(shapeObjArr[victim])

def addNestedDiv():
    print "nested div"

def readLogFile():
    global shapeObjCount, shapeobAr, shapeObjArr
    f = open("log.txt", mode="r")
    for line in f:
        print "From logs: "+line
        endParanthesis=line.find(')')
        if(endParanthesis==-1):
            endParanthesis = line.find(']')
        co= map(int, line[1:endParanthesis].split(", "))

        fillS=line.find("fill:")
        fillE=line.find('\n')
        fillColor=line[fillS+6:fillE]
        obj=w.create_rectangle(co,fill=fillColor)
        shapeobAr.append(obj)
        shapeObjArr.append(co)
        shapeObjCount+=1

def createLogFile():
    f=open("log.txt","w")
    i=0
    for x in shapeObjArr:
        print "Into Logs: "+str(x)
        f.write(str(x)+" fill: "+w.itemcget(shapeobAr[i],"fill")+"\n")
        i+=1
    f.close()
    root.destroy()

# create a menu
popup = Menu(root, tearoff=0)
popup.add_command(label="Resize", command=resize_root)
popup.add_command(label="Move", command=move_root)
popup.add_command(label="Remove", command=remove_root)
popup.add_command(label="Image" ,command=addImage)
popup.add_command(label="Text",command=addText)
popup.add_command(label="Link",command=addLink)
popup.add_command(label="Color",command=addColor)


def key(event):
    print "pressed", repr(event.char)

prev_x = 0
prev_y = 0
new_x = 0
new_y = 0
flag1 = 0

# return id of object from shapeObjArr[]
def findObject():
    # x=event.x
    # y=event.y
    x = event_x
    y = event_y

    area = 0
    finalObject = -1
    # print "in find object"
    for i in range(shapeObjCount):
        nm=shapeObjArr[i]
        # cds= C.coords(nm)
        cds = nm
        # print 'find= X=%s Y=%s Bound0=%s Bound1=%s Bound2=%s Bound3=%s' % (x, y, cds[0], cds[1], cds[2], cds[3])
        if x >= cds[0] and x <= cds[2] and y >= cds[1] and y <= cds[3]:
            # resize(shapeObjArr[i])
            if area == 0 or area > (abs(cds[2]-cds[0]) * abs(cds[3]-cds[1])):
                area = abs(cds[2]-cds[0]) * abs(cds[3]-cds[1])
                finalObject = i

            #print("heree")
            #return i

            #print "not this one"
    return finalObject

def do_popup(event):
    global popup
    global event_x, event_y
    event_x = event.x
    event_y = event.y
    # display the popup menu
    try:
        #print 'event= X=%s Y=%s' % (event.x, event.y)
        popup.tk_popup(event.x_root, event.y_root, 0)
        # findObject(event.x, event.y)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()
    #C.unbind("<Button-3>", do_popup)

def run_html():
    webbrowser.open_new_tab("index.html")
""""""

shapeframe = Frame(root, height="100")
optionframe = Frame(root, bg="pink", height="400", width="300")
gridframe = Frame(root, bg="white", height="400", width="1000")

shapeframe.pack(fill = X)
optionframe.pack(side = LEFT, fill = BOTH)
gridframe.pack(side = LEFT, fill = BOTH)


rectangle = PhotoImage(file="images/paintrect.gif")
circle= PhotoImage(file="images/paintcircle.gif")
line = PhotoImage(file="images/paintline.gif")
runb = PhotoImage(file="images/paintrun.gif")
topbtn1 = Button(shapeframe, text="Rectangle", height="5",width="30", command=draw_rectangle)
topbtn1.config(image = rectangle, height="80",width="200")
topbtn2 = Button(shapeframe, text="Circle", height="5",width="30", command=draw_circle)
topbtn2.config(image = circle, height="80",width="200")
topbtn3 = Button(shapeframe, text="Line", height="5",width="30", command=draw_line)
topbtn3.config(image = line, height="80",width="200")
topbtn4 = Button(shapeframe, text="Shape 4", height="5",width="30")
topbtn5 = Button(shapeframe, text="Shape 5", fg="black", height = "5", width = "30")
topbtn6 = Button(shapeframe, text="Run",  height = "5", width = "30", command=run_html)
topbtn6.config(image = runb, height="80",width="200")

topbtn1.grid(row=0, column=0)
topbtn2.grid(row=0, column=1)
topbtn3.grid(row=0, column=2)
topbtn4.grid(row=0, column=3)
topbtn5.grid(row=0, column=4)
topbtn6.grid(row=0, column=5)

'''topbtn1.pack()
'''

lefttext1 = Label(optionframe, text="Options Menu")
leftbtn1 = Button(optionframe, text="Option 1", fg="black", height = "8", width = "25")
leftbtn2 = Button(optionframe, text="Option 2", fg="black", height = "8", width = "25")
leftbtn3 = Button(optionframe, text="Option 3", fg="black", height = "8", width = "25")
leftbtn4 = Button(optionframe, text="Option 4", fg="black", height = "8", width = "25")
leftbtn5 = Button(optionframe, text="Option 5", fg="black", height = "8", width = "25")
leftbtn6 = Button(optionframe, text="Option 6", fg="black", height = "8", width = "25")
leftbtn7 = Button(optionframe, text="Option 7", fg="black", height = "8", width = "25")

scframe1 = VerticalScrolledFrame(gridframe)
scframe1.pack()

canvas_width = 1000
canvas_height = 1600
w = Canvas(scframe1.interior, width=canvas_width, height=canvas_height, bg="white")
w.bind('<B1-Motion>', onLeftDrag)
w.bind('<ButtonRelease-1>', releaseLeftDrag)
w.bind("<Button-3>", do_popup)

#makes horizontal lines
for height in range(30, 1600, 10):
    w.create_line(40, height, canvas_width-10, height, fill="#bbbbbb")
#makes vertical lines
for width in range(40, 1000, 10):
    w.create_line(width, 30, width, canvas_height-10, fill="#bbbbbb")

readLogFile()
###############

#root.configure(background="gray99")

scframe = VerticalScrolledFrame(optionframe)
scframe.pack()

lis = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#for i, x in enumerate(lis):
btn = Button(scframe.interior, height=8, width=25, relief=FLAT,
        bg="gray99", fg="purple3",
        font="Dosis", text='Button ',
        command=addButton)
para = Button(scframe.interior, height=8, width=25, relief=FLAT,
        bg="gray99", fg="purple3",
        font="Dosis", text='Paragraph ',
        command=addParagraph)
table = Button(scframe.interior, height=8, width=25, relief=FLAT,
        bg="gray99", fg="purple3",
        font="Dosis", text='Table',
        command=addTable)

div = Button(scframe.interior, height=8, width=25, relief=FLAT,
        bg="gray99", fg="purple3",
        font="Dosis", text='Div',
        command=addNestedDiv)

btn.pack(padx=10, pady=5, side=TOP)
para.pack(padx=10,pady=5, side=TOP)
table.pack(padx=10, pady=5, side=TOP)
div.pack(padx=10, pady=5, side=TOP)

w.pack()

def drawTable(coords):
    global shapeobAr,shapeObjArr,shapeObjCount;
    numRows = tkSimpleDialog.askinteger("Input Text", "No. of rows: ")
    numCols = tkSimpleDialog.askinteger("Input Text", "No. of cols: ")
    height=coords[3]-coords[1]
    width=coords[2]-coords[0]
    hinc=height/numRows
    winc=width/numCols
    x=coords[0]
    y=coords[1]
    victim = findObject()
    for i in range(0,numRows):
        for j in range(0,numCols):
            co=x,y,x+winc,y+hinc
            write_to_html(victim, "button",co,shapeObjCount,"rectangle",coords)
            obj = w.create_rectangle(co)
            shapeobAr.append(obj)
            shapeObjArr.append(co)
            shapeObjCount+=1
            x+=winc
        x=coords[0]
        y+=hinc

def openlink(i):
    global nav_menu_opt
    print(lis[i])


root.protocol("WM_DELETE_WINDOW", createLogFile)
root.mainloop()
