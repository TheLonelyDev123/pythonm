from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from level import map
from kivy.properties import *
from kivy.properties import Clock 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window



class Grass(Image):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.source="grass.png"
		
		
	def change_p(self,po):
		self.pos=po
		
class Stone(Image):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.source="stone.png"
	def change_p(self,po):
		self.pos=po
	
		
		
class Steve(Image):
		def __init__(self,**kwargs):
			super().__init__(**kwargs)
			self.source="steve.png"
			self.size=(80,80)




class Gui(Widget):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.left_bt=Image(source="left.png",size=(200,200),pos=(0,800))
		self.add_widget(self.left_bt)
		self.right_bt=Image(source="right.png",size=(200,200),pos=(0,200))
		self.add_widget(self.right_bt,999)
		self.jump_bt=Image(source="jump.png",size=(200,200),pos=(0,400))
		self.add_widget(self.jump_bt,9990)
		self.health=Image(source='3heart.png',size=(300,100))
		self.add_widget(self.health)
		self.mode=Image(source='grass_mode.png',size=(400,400),pos=(200,200))
		self.add_widget(self.mode)
	def on_touch_down(self,touch):
		if self.left_bt.collide_point(*touch.pos):
			self.parent.g.vx=-1
		if self.right_bt.collide_point(*touch.pos):
			self.parent.g.vx=1
		if self.jump_bt.collide_point(*touch.pos):
			if self.parent.g.allow:
				if self.parent.g.double_jump>0:
					self.parent.g.vy=23
				#	self.parent.ggravity_accel=True
					self.parent.g.allow=False
		if self.mode.collide_point(*touch.pos):
			if self.parent.g.type=='grass':
				self.parent.g.type='stone'
				self.mode.source='stone_mode.png'
			elif self.parent.g.type=='stone':
				self.parent.g.type='grass'
				self.mode.source='grass_mode.png'
			
			
			
			
	def on_touch_up(self,touch):		
		self.parent.g.shift=0
		self.parent.g.speed=9
		if self.left_bt.collide_point(*touch.pos) or self.right_bt.collide_point(*touch.pos):
			self.parent.g.vx=0
		



class Mainrun(Widget):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.gui=Gui()
		self.g=GameMain()
		self.add_widget(self.g)
		self.add_widget(self.gui)
		
	def on_size(self,*args):
		self.gui.left_bt.pos=(0,70)
		self.gui.right_bt.pos=(300,70)
		self.gui.jump_bt.pos=(self.width-200,70)
		self.gui.health.pos=(0,self.height-100)
		self.gui.mode.pos=(self.width-400,self.height-400)
		
		

	
		
				

class GameMain(Widget):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.shift=0
		self.allow=True
		self.gravity_accel=1
		self.gravity=-1
		self.speed=10
		self.vx=0
		self.jump_speed=30
		self.vy=0
		self.dimen=0
		self.shifty=0
		self.ghost=Grass()
		self.ghost.pos=(0,0)
		self.add_widget(self.ghost)
		self.ghost_pos=0
		self.health =3
		self.hit_list=[]
		self.double_jump=2
		self.type='grass'
		self.air=0
		
		Clock.schedule_interval(self.update,1/60)
		self.scrolly=0
		
		for rowi,row in enumerate(map):
			for coli,col in enumerate(row):
					c=15-rowi
					h=33-coli
					x=int(h*100)
					y=int(c*100)
				#print(h,c)
				
					if col==1: 
						self.b=Grass()
					
						self.b.change_p((x,y))
						self.add_widget(self.b)
					elif col==2:
						s=Stone()
						s.change_p((x,y))
						self.add_widget(s)
		
		self.player=Steve()
		self.add_widget(self.player)
		self.player.pos=(500,500)
		for child in self.children:
			if child != self.player:
				pass
	
	def on_size(self,*args):
		self.dimen=self.size
		print(self.dimen)
		self.left_bt.pos=(0,root.height-100)
		self.right_bt.pos=(200,root.height-100)
		self.jump_bt.pos=(root.width-200,root.height-100)
		
		
	
	def on_touch_down(self,touch):			#	self.speed+=3
		
		if abs(touch.x-self.player.x)<=300 and abs(touch.y-self.player.y)<=300:
			offset=self.ghost.x%100
			if touch.y<=260:
				if touch.x>500 and touch.x<self.parent.width-205:
					if self.type=='stone':
						k=Stone()
						print('place')
						print(offset)
						self.add_widget(k,1)
						k.pos=((int(touch.x/100))*100+abs(offset),(int(touch.y/100)*100))
					elif self.type=='grass':
						k=Grass()
						print('place')
						print(offset)
						self.add_widget(k,1)
						k.pos=((int(touch.x/100))*100+abs(offset),(int(touch.y/100)*100))
					
				
			else:	#		if ((int(touch.x/100))*100+abs(offset),(int(touch.y/100)*100)) in self.hit_list:
				if self.type=='stone':
					k=Stone()
					print('place')
					print(offset)
					self.add_widget(k,1)
					k.pos=((int(touch.x/100))*100+abs(offset),(int(touch.y/100)*100))
				elif self.type=='grass':
					k=Grass()
					print('place')
					print(offset)
					self.add_widget(k,1)
					k.pos=((int(touch.x/100))*100+abs(offset),(int(touch.y/100)*100))
		
			
	
			
			
	def hor_move(self):
		self.player.x+=self.vx*self.speed
		for child in self.children:
			if child != self.player:
				if self.player.collide_widget(child):
					if self.vx <0:
						self.player.x=child.x+101
						
					elif self.vx>0:
						self.player.x=child.x-81
						
		
					
	def ver_move(self):
		self.vy+=self.gravity
		self.player.y+=self.vy
		
		for child in self.children:
			if child != self.player:
				if self.player.collide_widget(child):
					if self.vy<0:
						
						self.player.y=child.y+101
						self.vy=0
						self.allow=True
						self.double_jump=2
						if int(self.air)>=10:
							self.health-=1
						self.air=0
					elif self.vy>0:
						self.player.y=child.y-81
						self.vy=0
			else:
				self.air+=0.2
	def shiftw(self):
		
		for child in self.children:
			if child != self.player:
					child.x+=self.shift
					child.y-= self.shifty
		
		
		
		xtem,ystem=self.player.center
		if xtem < self.parent.width/2-40 and self.vx<0:
			self.shift=9
			self.speed=0
		elif xtem > self.parent.width/2+40 and self.vx>0:
			self.shift=-9
			self.speed=0
		else:
			self.shift=0
			self.speed=10
			
	#	if ystem >= self.height-200 and self.vy>1:
#			self.shifty=-10
#			self.vy=0
#		elif ystem <=200 and self.vy<1:
#			self.shifty=-10
#			self.vy=0
#		else:
#			self.shifty=0
#			self.vy=0
#			
	def update(self,dt):
		self.hor_move()
		self.ver_move()
		self.shiftw()	
		print(self.health)
		if self.health==3:
			self.parent.gui.health.source='3heart.png'
		elif self.health==2:
			self.parent.gui.health.source='2hearts.png'
		elif self.health==1:
			self.parent.gui.health.source='1hearts.png'
		
		
	
			
			
#		self.hit_list=[]
#		for child in self.children:
#			if child!=self.player and child!= self.jump_bt:
#				if child!= self.right_bt and child!=self.left_bt:
#					self.hit_list.append(child.pos)
#					print(child.pos)

#		print(self.vy)

class GameApp(App):
	def build(self):
	#	Window.clearcolor=(0,0,0,255)
		game=Mainrun()		
		
		return game		
		
if __name__== '__main__':	
	GameApp().run()