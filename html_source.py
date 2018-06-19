import fileinput
import sys
from addComponents import *

"""Remove html code of a particular element from code"""
def remove_from_html(obj_id):
    fo = open("index.html", "w+")
    file_content = fo.read()
    print file_content
    fo.close()

def moveInHtml(objid,coords):
    lmargin = coords[0]
    tmargin = coords[1]
    resizedHeight = coords[3] - coords[1]
    resizedWidth = coords[2] - coords[0]
    replacerString = "top: " + str(tmargin) + ";\n"
    alterCSSFile(objid, "top:", replacerString,"")
    replacerString = "left: " + str(tmargin) + ";\n"
    alterCSSFile(objid, "left:", replacerString,"")


def resizeInHtml(objid,coords):
    lmargin=coords[0]
    tmargin=coords[1]
    resizedHeight=coords[3]-coords[1]
    resizedWidth=coords[2]-coords[0]
    replacerString="height: "+str(resizedHeight)+";\n"
    alterCSSFile(objid,"height:",replacerString,"")
    print "height zala"
    replacerString="width: "+str(resizedWidth)+";\n"
    alterCSSFile(objid,"width:",replacerString,"")

def get_line_number(tag):
    fhtml = open("index.html", "r")
    lines = fhtml.readlines()
    count = 1
    for line in lines:
        if line == tag:
            return count
        count += 1
    return -1

def delete(pid):
    # fcss = open("main.css", "r")
    # lines = fcss.readlines()
    print "indelete"
    alterCSSFile(pid,"}","\t\t\tdisplay:none;\n}\n","")


def alterCSSFile(objId,attributeToBeSearched,replaceBy,tag):
    if(attributeToBeSearched=="color:;"):
        if(tag=="anchor"):
            tid = "#object" + str(objId) + "{"
        elif(tag=="paragraph"):
            tid = "#object" + str(objId) + "{"
    else:
        tid = "#object" + str(objId) + "{"
    print tid
    flag = 0
    f = open("main.css", "r+")
    counter_index = 0
    while (1):
        line = f.readline()
        sindex = 0
        counter_index = counter_index + 1
        if tid in line:
            flag = 1
            sindex = counter_index

        elif attributeToBeSearched in line:
            if (flag == 1):
                print ("to replace")
                # f.write(line.replace("}", "display: none; }"))
                index = counter_index
                break
            flag = 0
        elif flag == 1 and "display" in line:
            print "replaced"
            sys.stdout.write(line.replace("display: block;", "display: none;"))
            break
    f.seek(0)
    contents = f.readlines()
    f.truncate(0)
    f.seek(0)
    #contents.insert(index - 1, replaceBy)
    contents[index-1]=replaceBy
    contents = "".join(contents)
    f.write(contents)
    f.close()


firstAccessToHtmlFile=0
"""Write the html code of a component to html file"""
def write_to_html(ob, element, shape_obj, obj_id,shape,parentObj):
    global firstAccessToHtmlFile
    if element == "button":
        """code to draw button"""
        # get coordinates of shape
        x1 = shape_obj[0]-parentObj[0]
        y1 = shape_obj[1]-parentObj[1]
        x2 = shape_obj[2]-parentObj[0]
        y2 = shape_obj[3]-parentObj[1]
        p1=parentObj[2]
        p2=parentObj[0]
        p=abs(p2-p1)
        x=abs(x2-x1)
        print parentObj
        print "x"+str(x)
        print "p"+str(p)
        # get properties
        height = abs(y2 - y1)
        top = y1

        if(p!=0):
            width = (x*100)/p
            left= (x1*100)/p
        else:
            width=x/(1000/97)
            left = x1 / (1000 / 97)


        # html code  #<a href='#'>Default</a>

        button_code = """<div id='object"""+str(obj_id)+"""'>
        <!--anchor text-->
        <!--paragraph text-->
        <!--nested div-->
    </div>\n"""
        if(shape=="circle"):
            button_code = """<div class="btn btn-default" style="border-radius:50%" id='object""" + str(obj_id) + """'>
                    </div>\n"""

        # css code
        button_css=""
        if shape=="circle":
            button_css = """#object""" + str(obj_id) + """{
                            height: """ + str(height) + """px;
                            width: """ + str(width) + """%;
                            top: """ + str(top) + """px;
                            left: """ + str(left) + """%;
                            position: absolute;
                            font-size:;
                            font-family:;
                            text-decoration:;
                            color:;
                            background-color:;
                            border-radius:50%;
                    }\n """
        else:
            button_css = """#object""" + str(obj_id) + """{
                    height: """ + str(height) + """px;
                    width: """ + str(width) + """%;
                    top: """ + str(top) + """px;
                    left: """ + str(left) + """%;
                    position: absolute;
                    text-align:center;
                    font-size:;
                    font-family:;
                    text-decoration:;
                    color:;
                    background-color:;
            }\n """

        fhtml = open("index.html", "a+")
        fcss = open("main.css", "a+")
        if (firstAccessToHtmlFile == 0):
            firstAccessToHtmlFile = 1
            #fhtml.truncate(0)
            #fhtml.seek(0)
            fcss.truncate(0)
            fcss.seek(0)

            fhtml.write(
                "<html><head><title>Index</title><link rel=\"stylesheet\" href=\"main.css\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">  <link rel=\"stylesheet\" href=\"bootstrap.css\"><script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js\"></script><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script></head>\n<body>\n")
        if ob != -1:
            print "parent ob" + str(ob)
            addTag(ob, shape_obj, "div", obj_id)
        else:
            fhtml.write(button_code)
        fcss.write(button_css)
        fhtml.close()
        fcss.close()



def replace_text(id, old, new):
    flag = 0
    id = "object" + str(id)
    o = open("temp.html", "a")  # open for append
    for line in open("index.html"):
        if id in line:
            flag = 1
        elif "object" in line:
            flag = 0
        if flag == 1 and "a" in line:
            line = line.replace(old, new)
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

def addImageTag(id, imageName):
    flag = 0
    id = "object" + str(id)
    o = open("temp.html", "a")  # open for append
    for line in open("index.html"):
        if id in line:
            flag = 1
        elif "object" in line:
            flag = 0
        if flag == 1:
            line = line.replace("<!--anchor text-->", "<img src='"+imageName+"' />")
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


def addLinkToAnchorTag(id, filename):
    flag = 0
    id = "object" + str(id)
    o = open("temp.html", "a")  # open for append
    for line in open("index.html"):
        if id in line:
            flag = 1
        elif "object" in line:
            flag = 0
        if flag == 1:
            line = line.replace("#", filename)
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






"""if(flag==1):
                index=counter_index
                break

                print(index)
    f.seek(0)
    contents=f.readlines()
    contents.insert(index-1,"display: none;")
    contents="".join(contents)
    f.write(contents)
    f.close()"""