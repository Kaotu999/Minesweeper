from functools import partial
from tkinter import *
import tkinter
from PIL import ImageTk,Image
import random
import sys, os

from numpy import var

#🚩

LVL_info = []
f = open('LVL.txt','r+')
for _i in f.read().split():
    _i = int(_i)
    LVL_info.append(_i)

length = LVL_info[0]
width = LVL_info[1]
mine = LVL_info[2]
background_color = 'white'
num_colors = {0:'white',1:'blue',2:'green',3:'orange',4:'red',5:'purple',6:'purple',7:'purple',8:'purple',9:'purple'}
button_ids = []
button_nums = list(range(1,(width*length)+1))
bombs_spawn = list(range(1,(width*length)+1))
mines = []
broken = []
flagged = []
BTNvals = {}
First = True
Flagging = False

root = Tk()
root.title('MINESWEEPER')
root.iconbitmap('mine.ico')
root.configure(background=background_color)
mine_img_big = Image.open('mine.png').resize((15,15))
mine_img = ImageTk.PhotoImage(mine_img_big)

def restart():
    f.close()
    os.startfile(sys.argv[0])
    sys.exit()

def save(val):
    f.seek(0)
    f.truncate()
    for v in range(len(val)):
        f.write(str(val[v])+' ')
    restart()

def RC_To_num(r, c):
    return (r*length)+c+1

def num_To_RC(num):
    return [((num-1)//length),((num-1)%length)]

def check(now):
    surround = 0
    allaround = []
    row = num_To_RC(now)[0]
    col = num_To_RC(now)[1]
    if now in mines:
        return 'bomb'
    if row!=0: #Top
        allaround.append(RC_To_num(row-1,col))
        if (RC_To_num(row-1,col) in mines):
            surround += 1
    if (row!=0 and col!=0): #Top left
        allaround.append(RC_To_num(row-1,col-1))
        if (RC_To_num(row-1,col-1) in mines):
            surround += 1
    if col!=0 : #Left
        allaround.append(RC_To_num(row,col-1))
        if (RC_To_num(row,col-1) in mines):
            surround += 1
    if (col!=0 and row!=(width-1)): #Bottom left
        allaround.append(RC_To_num(row+1,col-1))
        if (RC_To_num(row+1,col-1) in mines):
            surround += 1
    if row!=(width-1): #Bottom
        allaround.append(RC_To_num(row+1,col))
        if (RC_To_num(row+1,col) in mines):
            surround += 1
    if (row!=(width-1) and col!=(length-1)): #Bottom right
        allaround.append(RC_To_num(row+1,col+1))
        if (RC_To_num(row+1,col+1) in mines):
            surround += 1
    if col!=(length-1): #Right
        allaround.append(RC_To_num(row,col+1))
        if (RC_To_num(row,col+1) in mines):
            surround += 1
    if (row!=0 and col!=(length-1)): #Top right
        allaround.append(RC_To_num(row-1,col+1))
        if (RC_To_num(row-1,col+1) in mines):
            surround += 1
    for y in allaround:
        if y in broken:
            allaround.remove(y)
    return [surround,allaround]

def spawn_mines():
    global mine
    while mine > 0:
        a = random.choice(bombs_spawn)
        if a not in mines:
            mines.append(a)
            mine = mine-1

def create_nums():
    for x in button_nums:
        BTNvals.update({x : (check(x))[0]})

def break_BTN(BTN_num):
    broken.append(BTN_num)
    button_ids[BTN_num-1].destroy()
    Label(text=BTNvals.get(BTN_num),fg=num_colors.get(BTNvals.get(BTN_num)),bg=background_color).grid(row=num_To_RC(BTN_num)[0],column=num_To_RC(BTN_num)[1])

def break_logic(now):
    global broken
    break_BTN(now)
    if BTNvals.get(now)==0:
        CanGo = check(now)[1]
        for _c in button_nums:
            if _c in CanGo:
                if BTNvals.get(_c)==0 and _c not in broken:
                    break_logic(_c)
                else:
                    break_BTN(_c)

def pressed(i):
    global First
    bname = button_ids[i]
    if Flagging:
        if (i+1) in flagged:
            bname.configure(text='')
            flagged.remove(i+1)
        else:
            bname.configure(text='🚩',fg='red')
            flagged.append(i+1)
    else:
        if First:
            A = check(i+1)[1]
            bombs_spawn.remove(i+1)
            for b in A:
                bombs_spawn.remove(b)
            First = False
            spawn_mines()
            create_nums()
            break_logic(i+1)
        else:
            if i+1 in mines:
                bname.configure(bg='red')
                StartBTN.configure(text='😡',bg='orange')
                for n in mines:
                    button_ids[n-1].configure(state=DISABLED)
                    l_img = tkinter.Label(root, image=mine_img)
                    l_img.grid(row=num_To_RC(n)[0],column=num_To_RC(n)[1])
            else:
                break_logic(i+1)
            
def create_BTNs():
    for r in range(width):
        for c in range(length):
            cell = Button(root,width=2,height=1,disabledforeground='red',command=partial(pressed,RC_To_num(r,c)-1))
            cell.grid(row=r,column=c)
            button_ids.append(cell)
    for x1 in range(length):
        Button(bg='black',width=2,height=1,state=DISABLED).grid(row=width,column=x1)
    for x2 in range(width):
        Button(bg='black',width=2,height=1,state=DISABLED).grid(row=x2,column=length)

def Flag():
    global Flagging
    if Flagging:
        for f in flagged:
            button_ids[f-1].configure(state=DISABLED)
        Flagging=False
        stat.configure(text='')
    else:
        for f in flagged:
            button_ids[f-1].configure(state=NORMAL)
        Flagging=True
        stat.configure(text='Flagging')

create_BTNs()

StartBTN = Button(text='😀',bg='yellow',width=2,height=1,command=partial(save,[length,width,mine]))
StartBTN.grid(row=width,column=length)

FlagBTN = Button(text='🚩',width=2,height=1,command=Flag)
FlagBTN.grid(row=width+1,column=0,columnspan=2)
stat = Label(text='',fg='red',bg=background_color)
stat.grid(row=width+1,column=length-2,columnspan=3)

EasyBTN = Button(text='EASY',width=15,command=partial(save,[10,10,10]))
IntermediateBTN = Button(text='INTERMEDIATE',width=15,command=partial(save,[16,16,40]))
HardBTN = Button(text='EXPERT',width=15,command=partial(save,[30,16,99]))
EasyBTN.grid(row=width+1,column=0,columnspan=length)
IntermediateBTN.grid(row=width+2,column=0,columnspan=length)
HardBTN.grid(row=width+3,column=0,columnspan=length)

versionLabel = Label(text='V1.0 ; creator: K40tu',fg='black',bg=background_color)
versionLabel.grid(row=width+5,columnspan=length)

root.mainloop()