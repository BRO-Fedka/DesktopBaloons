
import tkinter as tk
import random
import keyboard
import datetime
from pygame import mixer
from PIL import Image,ImageTk
ANIMATIONS = [
[0,1,2,1],
[3,4],
[5,6]
]
COLORS = [
[(255,0,0),(200,0,0)],
[(255,255,0),(200,200,0)],
[(0,255,0),(0,200,0)],
[(0,255,255),(0,200,200)],
[(0,0,255),(0,0,200)],
[(255,0,255),(200,0,200)],
]
BALOONFRAMES =[
Image.open('./img/baloon0.png'),
Image.open('./img/baloon1.png'),
Image.open('./img/baloon2.png'),
Image.open('./img/baloon3.png'),
Image.open('./img/baloon4.png'),
Image.open('./img/baloon5.png'),
Image.open('./img/baloon6.png')
]
COLOREDBALOONS = []
class Baloon():
	def __init__(self):
		self.status = 'FLYING'
		self.x = random.randint(50,WIDTH-50)
		self.color = random.randint(0,len(COLOREDBALOONS)-1)
		self.animation = 0
		self.y = HEIGHT+50
		self.frame = 0
		self.timer = 0
		self.dead = False
		self.speed = 1 + random.random()*1
		self.canvitem = CANVAS.create_image(self.x,self.y,image =COLOREDBALOONS[self.color][ANIMATIONS[self.animation][self.frame]])
		
		CANVAS.tag_bind(self.canvitem,'<Button-1>',self.Pop)

	def Pop(self,e = None):
		self.status = 'POP'
		self.frame = 0
		self.animation = 1
		POPSND.play()
	def Update( self):
		global MISSEDBALOONS
		global LASTBALOON
		if self.y > HEIGHT+60:
			self.dead = True
		elif self.y < -60:
			LASTBALOON = datetime.datetime.now()
			MISSEDBALOONS +=1
			self.dead = True
		if self.status == 'FLYING':
			if ANIMATIONS[self.animation][self.frame] == 0:
				self.y -= 1*self.speed
			elif ANIMATIONS[self.animation][self.frame] == 2:
				self.y -= 3*self.speed
			else:self.y -= 2*self.speed
			if self.timer == 0:
				self.frame = (self.frame+1 )%len(ANIMATIONS[self.animation])
				if ANIMATIONS[self.animation][self.frame]==2:self.timer = random.randint(8,16)
				else:
					self.timer = 3
			self.timer -=1
			CANVAS.coords(self.canvitem,self.x,self.y)
			CANVAS.itemconfig(self.canvitem, image = COLOREDBALOONS[self.color][ANIMATIONS[self.animation][self.frame]])
		elif self.status == 'POP':
			CANVAS.itemconfig(self.canvitem, image = COLOREDBALOONS[self.color][ANIMATIONS[self.animation][self.frame]])
			self.frame +=1
			if self.frame ==2:
				self.status = 'FALLING'
				self.animation = 2
				self.frame = 0
		elif self.status == 'FALLING':
			self.y += 12*self.speed
			if self.timer == 0:
				self.frame = (self.frame+1 )%len(ANIMATIONS[self.animation])
				self.timer = 2
			self.timer -=1
			CANVAS.coords(self.canvitem,self.x,self.y)
			CANVAS.itemconfig(self.canvitem, image = COLOREDBALOONS[self.color][ANIMATIONS[self.animation][self.frame]])
FORM = tk.Tk()
FPS = 30
WIDTH = FORM.winfo_screenwidth()
HEIGHT = FORM.winfo_screenheight()
CANVAS = tk.Canvas(FORM,bg = '#000',bd = 0,highlightthickness = 0, cursor = 'hand2')
CANVAS.place(x=0,y=0,width = WIDTH,height = HEIGHT)
mixer.init()
POPSND = mixer.Sound('./snd/pop.wav')
BEEPSND = mixer.Sound('./snd/beep.wav')
for color in range(0,len(COLORS)):
		COLOREDBALOONS.append([])
		for frame in range(0,len(BALOONFRAMES)):
			copyimg = BALOONFRAMES[frame].copy()
			pixels = copyimg.load()
			for i in range(copyimg.size[0]): 
			    for j in range(copyimg.size[1]):
			        if pixels[i,j] == (255, 0, 0,255):
			            pixels[i,j] = COLORS[color][0]
			        elif pixels[i,j] == (200, 0, 0,255):
			            pixels[i,j] = COLORS[color][1]
			COLOREDBALOONS[color].append(ImageTk.PhotoImage(copyimg))
BALOONS = []
LASTBALOON = None
MISSEDBALOONS= 0
LOCKSCREEN = CANVAS.create_rectangle(-1,-1,WIDTH,HEIGHT, fill = '#010101',state = 'hidden')
TITLE = CANVAS.create_text(WIDTH//2, HEIGHT//2, text="",justify=tk.CENTER, font="Fixedsys 32",fill = '#fff')
def empty(e=None):pass
def Update(e = None):
		global MISSEDBALOONS
		
		if not LASTBALOON is None and  (datetime.datetime.now()-LASTBALOON).seconds < 60*MISSEDBALOONS:
			CANVAS.itemconfig(LOCKSCREEN,state = 'normal')
			CANVAS.itemconfig(TITLE,state = 'normal',text = 'Your PC will be unlocked soon\n'+str((60*MISSEDBALOONS-(datetime.datetime.now()-LASTBALOON).seconds)//60) + ':' +str((60*MISSEDBALOONS-(datetime.datetime.now()-LASTBALOON).seconds)%60))
			CANVAS.config(cursor='none')
		else:
			CANVAS.itemconfig(LOCKSCREEN,state = 'hidden')
			CANVAS.itemconfig(TITLE,state = 'hidden')
			MISSEDBALOONS = 0
			CANVAS.config(cursor='hand2')
			if random.randint(0,FPS*5) == 0 and len(BALOONS)==0:
				BEEPSND.play()
				
				for _ in range(0,random.randint(7,14)):

					BALOONS.append(Baloon())
		_ = 0
		while _ < len(BALOONS):
			BALOONS[_].Update()
			if BALOONS[_].dead:
				BALOONS.pop(_)
				_-=1
			_+=1
		FORM.after(int(1000/FPS),Update) 
FORM.protocol('WM_WINDOW_DELETE',  empty)
keyboard.block_key('f4')
FORM.overrideredirect(True)
FORM.state('zoomed')
FORM.wm_attributes("-topmost", True)
FORM.wm_attributes("-transparentcolor", "#000")
FORM.after(int(1000/FPS),Update) 
FORM.mainloop()