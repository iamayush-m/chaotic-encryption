#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import Tkinter
import tkFileDialog
from PIL import Image, ImageTk
from numpy import *
from decimal import Decimal
from scipy.integrate import odeint
import scipy
from math import *
from shutil import copy2

def dec2bin(i):
	s=str(bin(i))[2:]
	length=len(s)
	ans=[]
	for x in range(0,8-length):
		ans.append(0)
	for x in range(0,length):
		ans.append(int(s[x]))
	return ans


def bin2dec(x):
	num=0
	for i in range(0,8):
		num+=x[i]*(2**(8-1-i))
	return num

def lorenz_int(initial, t): 
   
  x = initial[0]
  y = initial[1]
  z = initial[2]
  sigma = 10
  rho = 28
  beta = 8.0/3
  x_dot = sigma * (y - x)
  y_dot = x * (rho -z) - y
  z_dot = x * y - beta* z
  return [x_dot, y_dot, z_dot]

def saveFun(cn):
	f = tkFileDialog.asksaveasfile(mode='w', defaultextension="."+cn.split('.').pop())
	if f is None:
		return
	copy2(cn, f.name)

def encryption(f,xx,yy,zz):
	global myvar22
	global savebutton
	global flag2
	global msg
	global bs
	sm=False
	if flag2==True:
		myvar22.destroy()
		savebutton.destroy()
		msg.destroy()
	flag2=True
	img = Image.open(f.name)
	if f.name.split('.').pop()=='jpg':
		sm=True
		img.save('FotoTemp.png')
		img = Image.open('FotoTemp.png')
	print "image read"
	# img = img.convert('1')
	arr = array(img)
	#print arr
	a,b=img.size
	print a  , b
	##############################################

	


	########################################STEP 1

	  #initial conditions.
	initial = [float(xx),float(yy),float(zz)]            
	t = scipy.arange(10.00001, 10.00301, 0.000001)   
	DataOut = odeint(lorenz_int, initial, t)
	

	###################################STEP 2
	initial[0]= DataOut[3000,0]
	initial[1]= DataOut[3000,1]
	initial[2]= DataOut[3000,2]
	t8=scipy.arange(0,1.6,0.2)
	for l in range(0,b) :
	  for br in range(0,a):
	   
	    lorenz_sol = odeint(lorenz_int, initial, t8)
	    # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	    # print lorenz_sol
	    # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	    x = [i[0] for i in lorenz_sol]
	    y = [i[1] for i in lorenz_sol]
	    z = [i[2] for i in lorenz_sol]



	    mx=max(x)
	    my=max(y)
	    mix=min(x)
	    miy=min(y)
	    dx=mx-mix
	    dy=my-miy
	    keyx=[]
	    keyy=[]
	    for i in range(0,8):
	      if ((x[i]-mix)/dx)>=0.5:
	        keyx.append(1)
	      else:
	        keyx.append(0)
	      if ((y[i]-miy)/dy)>=0.5:
	        keyy.append(1)
	      else:
	        keyy.append(0)
	    Wi=0
	    Wj=0
	    """for i in range(0,8):   ## WHAT IS THIS?!
	      Wi+=keyx[i]*(2**i)
	      Wj+=keyy[i]*(2**i)"""
	    Wi=bin2dec(keyx)
	    Wj=bin2dec(keyy)
	    D=170
	    initial[0]=x[7]
	    initial[1]=y[7]
	    initial[2]=z[7]
	    # print initial[0]
	    # print initial[1]
	    # print initial[2]


	      ###################################################STEP 3
	    W1=[]
	    W2=[] 
	    C=[]
	    Wd1=[]
	    Wd2=[]
	    Theta=[]
	    for i in range(0,8):
	      if keyx[i]==1:
	        W1.append(1)
	        C.append(-0.5)
	        Wd1.append(1)
	      else:
	        W1.append(-1)
	        C.append(0.5)
	        Wd1.append(0)
	      if keyy[i]==1:
	        W2.append(1)
	        Wd2.append(1)
	      else:
	        W2.append(-1)
	        Wd2.append(0)
	      Theta.append(Wd1[i]^Wd2[i])
	    for rgb in xrange(0,3):
	     
		    im= dec2bin(arr[l,br,rgb])
		    for k in range(0,8):
		      if W1[k]==1:
		        if (W1[k]*im[k] + W2[k]*C[k] - Theta[k]) >=0 :
		          im[k]=1
		        else :
		          im[k]=0
		      else :
		        if (W1[k]*im[k] - W2[k]*C[k] + Theta[k]) >=0 :
		          im[k]=1
		        else :
		          im[k]=0
		    temp=bin2dec(im)
		    """temp=0
		    for i in range(0,8):   ## WHAT IS THIS?!
		      temp+=im[i]*(2**i)"""
		    arr[l,br,rgb]=temp
		    
	img = Image.fromarray(arr)
	if sm==False:
		exten=f.name.split('.').pop()
	else:
		exten="png"
	img.save("cache."+exten)
	print "image cached : "+"cache."+exten
	#msg2.destroy()
	msg=Tkinter.Label(frame3,text="Encryption/Decrypted Image ", font=("Helvetica",14))
	msg.configure(background=BGCOLOR)
	msg.pack()
	IMG = Image.open("cache."+exten)
	tkimage = ImageTk.PhotoImage(IMG)
	myvar22=Tkinter.Label(frame3,image = tkimage)
	myvar22.image = tkimage
	myvar22.pack()
	bs=Tkinter.Label(frame3,text="9555226464",font=("Ubuntu",8))
	bs.configure(background=BGCOLOR,foreground=BGCOLOR)
	bs.pack()
	savebutton=Tkinter.Button(frame3,text='Save', command=lambda:saveFun("cache."+exten))
	savebutton.configure(background="black",foreground="white")
	savebutton.pack()

flag=False
flag2=False
#BGCOLOR="dark slate gray"
BGCOLOR="orange2"
fileName=""
prev=None
root = Tkinter.Tk()

root.configure(background=BGCOLOR)
frame1=Tkinter.Frame(root)
frame1.configure(background=BGCOLOR)
frame1.pack()
root.geometry("600x550")
heading=Tkinter.Label(frame1, text="Image Encryption and Decryption", font=("Ubuntu",20))
heading.configure(background=BGCOLOR)
heading.pack()
def openFile():
	global fileName
	global enB
	global flag
	global myvar
	global blankSpace
	if flag==True:
		myvar.destroy()
		blankSpace.destroy()
	fileName = tkFileDialog.askopenfile(parent=frame1,initialdir='/home/',title='Select your file', filetypes=[('png files', '.png'),('JPEG files', '.jpg'),('BMP files', '.bmp'),('All Files','.*')])
	blankSpace=Tkinter.Label(frame1,text="iambatman",font=("Ubuntu",8))
	blankSpace.configure(background=BGCOLOR,foreground=BGCOLOR)
	blankSpace.pack()
	if fileName is not None:
		im = Image.open(fileName)
		tkimage = ImageTk.PhotoImage(im)
		myvar=Tkinter.Label(frame1,image = tkimage)
		myvar.image = tkimage
		myvar.pack()
		enB.pack()
		flag=True
	else:
		blankSpace.destroy()
		return
b3=Tkinter.Button(frame1, text = 'Select image to Encrypt/Decrypt', fg = 'black', command= openFile)  #font=("TkDefaultFont",8,"bold")
b3.configure(background="black",foreground="white")
b3.pack()
frame2=Tkinter.Frame(root)
frame2.configure(background=BGCOLOR)
frame2.pack()
t1=Tkinter.Label(frame2, text="X : ")
t1.configure(background=BGCOLOR)
t1.grid(row=0,column=0, pady=7)
x = Tkinter.Entry(frame2, width=5)
x.delete(0, Tkinter.END)
x.insert(0, "5")
x.grid(row=0,column=1)   #s=e.get()
t2=Tkinter.Label(frame2, text="  Y : ")
t2.configure(background=BGCOLOR)
t2.grid(row=0,column=3)
y = Tkinter.Entry(frame2, width=5)
y.delete(0, Tkinter.END)
y.insert(0, "5")
y.grid(row=0,column=4) 
t3=Tkinter.Label(frame2, text="  Z : ")
t3.configure(background=BGCOLOR)
t3.grid(row=0,column=6)
z = Tkinter.Entry(frame2, width=5)
z.delete(0, Tkinter.END)
z.insert(0, "5")
z.grid(row=0,column=7) 
frame3=Tkinter.Frame(root)
frame3.configure(background=BGCOLOR)
frame3.pack()
enB=Tkinter.Button(frame3, text = 'Submit !', fg = 'black',command = lambda: encryption(fileName,x.get(),y.get(),z.get()))
enB.configure(background="black",foreground="white")

nm=Tkinter.Label(root,text=" Ayush Mehra", font=("Tibetan Machine Uni",10,"italic"))
nm.configure(background=BGCOLOR)
nm.pack( side = Tkinter.BOTTOM)
root.mainloop()