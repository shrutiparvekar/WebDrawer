from html_source import *

def addTag(id,shape_obj,tag, nest):
    flag = 0
    button_code = """<!--nested div-->
        <div id='object""" + str(nest) + """'>
           <!--anchor text-->
           <!--paragraph text-->
           <!--nested div-->
        </div>"""
    id = "object" + str(id)
    o = open("temp.html", "a")  # open for append
    for line in open("index.html"):
        if id in line:
            flag = 1
        elif "</" in line and flag==1:
            if tag=="anchor":
                line = line.replace("/div", "/a")
            if tag=="paragraph":
                line = line.replace("/div", "/p")
            if tag=="img":
                line = line.replace("/div", "/img")
            flag = 0
        elif "object" in line:
            flag = 0
        if tag == "div" and flag == 1 and "<!"  in line:
            line = line.replace("<!--anchor text-->", "")
            line = line.replace("<!--paragraph text-->", "")

        if flag == 1:
            if(tag=="anchor") and "nested" not in line:
                line = line.replace("div", "a class='btn btn-default' href='#'")
            elif(tag=="paragraph") and "nested" not in line:
                line = line.replace("div", "p")
            elif (tag == "img") and "nested" not in line:
                line = line.replace("div", "img src=''")
            elif(tag == "div"):
                line = line.replace("<!--nested div-->", button_code)
        o.write(line)
    o.close()
    f = open('index.html', 'r+')
    f.truncate()
    f.close()
    f = open('index.html', 'a')
    g = open('temp.html', 'r+')
    for l in g.readlines():
        f.write(l)
    f.close()
    f = open('temp.html', 'r+')
    f.truncate()
    f.close()
    g.close()

    x1 = shape_obj[0]
    y1 = shape_obj[1]
    x2 = shape_obj[2]
    y2 = shape_obj[3]

    # get properties
    height = abs(y2 - y1)
    width = abs(x2 - x1)
    top = y1
    left = x1
    if(tag=="anchor"):
        # css code for anchor
        anchor_css = """#"""+ id + """ a{
                        text-decoration:;
                        color:;
                        }
                    \n """
    elif(tag=="paragraph"):
        # css code for paragraph
        anchor_css = """#""" + id + """ p{
                               color:;
                               }
                           \n """

    elif(tag=="div"):
        anchor_css = ""

    #fcss = open("main.css", "a+")
    #fcss.write(anchor_css)
    #fcss.close()

def addPath(id,path,h,w,tag,nest):
    flag = 0
    button_code = """src='"""+path+"""'>"""
    id = "object" + str(id)
    o = open("temp.html", "a")  # open for append
    for line in open("index.html"):
        if id in line:
            flag = 1
        elif "</" in line or "object" in line:
            flag = 0
        if flag == 1:
            if (tag == "img"):
                line = line.replace("img src=''","img src='"+path+"' style='height:"+str(h)+";width:"+str(w)+";'" )

        o.write(line)
    o.close()
    f = open('index.html', 'r+')
    f.truncate()
    f.close()
    f = open('index.html', 'a')
    g = open('temp.html', 'r+')
    for l in g.readlines():
        f.write(l)
    f.close()
    f = open('temp.html', 'r+')
    f.truncate()
    f.close()
    g.close()
