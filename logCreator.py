import Tkinter
import pickle
import tkMessageBox

top = Tkinter.Tk()

C = Tkinter.Canvas(top, bg="blue", height=250, width=300)

coord = 10, 50, 240, 210
arc = C.create_arc(coord, start=0, extent=150, fill="red")
f=open("log.txt",mode="wb")
arcP=pickle.dump(arc,f)
f.close()
f=open("log.txt",mode="r")
arcUP=pickle.load(f)
print C.itemcget(arcUP,"fill")
arcUPO=C.create_arc(C.coords(arcUP),fill="green")

C.pack()
top.mainloop()