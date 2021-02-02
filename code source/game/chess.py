import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
FPS = 50

import pygame
from pygame.locals import *
from game.placement import positionnement

def lunch_game():

	os.chdir(os.path.dirname(__file__))

	pygame.init()
	BLANC=(255,255,255)
	mouse_pos=old_mouse_pos=[-1,-1]
	points=[]
	points_unpassun={"b":[],"n":[]}
	castling=[]

	class KingsInstance():
		def __init__(self,color,posx,posy):
			self.color=color
			self.posx=posx
			self.posy=posy
			self.check=False
			self.CheckMate=False
			self.moved=False
			self.K_rook=False
			self.Q_rook=False
			self.K_castle=False
			self.Q_castle=False
			
		def CheckInstance(self,kposx=None,kposy=None):
			Etat=False
			if kposx==None:
				kposx=self.posx
			if kposy==None:
				kposy=self.posy
				#Echec avec reine,fou,tour
			for i in [[-1,-1,"nw","b"],[0,-1,"n0","r"],[1,-1,"ne","b"],[-1,0,"w0","r"],[1,0,"e0","r"],[-1,1,"sw","b"],[0,1,"s0","r"],[1,1,"se","b"]]:
				obool=True
				while obool:
					if 8>(kposy+i[1])>=0 and 8>(kposx+i[0])>=0 :
						if table[kposy+i[1]][kposx+i[0]]!="00":
							if table[kposy+i[1]][kposx+i[0]][0]!=self.color:
								if table[kposy+i[1]][kposx+i[0]][1]=="q":
									Etat=True
									obool=False
								elif table[kposy+i[1]][kposx+i[0]][1]==i[3]:
									Etat=True
									obool=False
								else:
									obool=False
							else:
								obool=False
					else:
						obool=False
					if i[2][0]=="n":
							i[1]-=1
					elif i[2][0]=="e":
							i[0]+=1
					elif i[2][0]=="s":
							i[1]+=1
					elif i[2][0]=="w":
							i[0]-=1
					if i[2][1]=="w":
							i[0]-=1
					elif i[2][1]=="e":
							i[0]+=1
				#Echec avec cavalier
			if not Etat :
				for i in ((-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1)):
					if 8>(kposy+i[1])>=0 and 8>(kposx+i[0])>=0 :
						if table[kposy+i[1]][kposx+i[0]]!="00":
							if table[kposy+i[1]][kposx+i[0]][0]!=self.color:
								if table[kposy+i[1]][kposx+i[0]][1]=="c":
									Etat=True
									break
				#Echec avec pion
			if not Etat :
				for i in ((-1,jeu[self.color]),(1,jeu[self.color])):
					if 8>(kposy+i[1])>=0 and 8>(kposx+i[0])>=0 :
						if table[kposy+i[1]][kposx+i[0]]!="00":
							if table[kposy+i[1]][kposx+i[0]][0]!=self.color:
								if table[kposy+i[1]][kposx+i[0]][1]=="p":
									Etat=True
									break
			return Etat
		
		def CheckMateInstance(self,points):
			x=y=7
			obool=True
			while y>=0 and obool:
				if table[y][x]!="00" and table[y][x][0]==self.color:
					points=CréationDesPoints(points,[x,y])
					i=len(points)-1
					while i>=0:
						mémoire1=table[points[i][1]][points[i][0]]
						table[points[i][1]][points[i][0]]=table[y][x]
						table[y][x]="00"
						if table[points[i][1]][points[i][0]][1]=="k":
							mémoire2=Kings[jeu["joueur"]].CheckInstance(points[i][0],points[i][1])
						else:
							mémoire2=Kings[jeu["joueur"]].CheckInstance()
						table[y][x]=table[points[i][1]][points[i][0]]
						table[points[i][1]][points[i][0]]=mémoire1
						
						if mémoire2 :
							del points[i]
						i-=1
					if points==[]:
						x-=1
						if x<0:
							x=7
							y-=1
					else:
						obool=False
				else:
					x-=1
					if x<0:
						x=7
						y-=1
			return obool

		def Castle(self):
			if not self.check:
				if not self.K_rook:
					if table[self.posy][self.posx-(1*jeu["b"])]=="00" and table[self.posy][self.posx-(2*jeu["b"])]=="00":
						if not self.CheckInstance(self.posx-(1*jeu["b"])) and not self.CheckInstance(self.posx-(2*jeu["b"])):
							self.K_castle=True
						else:
							self.K_castle=False
					else:
						self.K_castle=False
				if not self.Q_rook:
					if table[self.posy][self.posx+(1*jeu["b"])]=="00" and table[self.posy][self.posx+(2*jeu["b"])]=="00":
						if not self.CheckInstance(self.posx+(1*jeu["b"])) and not self.CheckInstance(self.posx+(2*jeu["b"])):
							self.Q_castle=True
						else:
							self.Q_castle=False
					else:
						self.Q_castle=False
				


	def CréationDesPoints(points,pos):
		points=[]
		if table[pos[1]][pos[0]][1]=="k":
			points=AfficheurPoints(((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)),False,points,pos)
		if table[pos[1]][pos[0]][1]=="q":
			points=AfficheurPoints([[-1,-1,"nw"],[0,-1,"n0"],[1,-1,"ne"],[-1,0,"w0"],[1,0,"e0"],[-1,1,"sw"],[0,1,"s0"],[1,1,"se"]],True,points,pos)	
		if table[pos[1]][pos[0]][1]=="r":
			points=AfficheurPoints([[-1,0,"w0"],[0,-1,"n0"],[1,0,"e0"],[0,1,"s0"]],True,points,pos)			
		if table[pos[1]][pos[0]][1]=="b":
			points=AfficheurPoints([[-1,-1,"nw"],[1,-1,"ne"],[1,1,"se"],[-1,1,"sw"]],True,points,pos)
		if table[pos[1]][pos[0]][1]=="c":
			points=AfficheurPoints(((-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1)),False,points,pos)
		if table[pos[1]][pos[0]][1]=="p":
			if table[pos[1]+jeu[table[pos[1]][pos[0]][0]]][pos[0]]=="00":
				points.append([pos[0],pos[1]+jeu[table[pos[1]][pos[0]][0]]])
				if table[pos[1]][pos[0]][2]=="0":
					if table[pos[1]+2*jeu[table[pos[1]][pos[0]][0]]][pos[0]]=="00":
						points.append([pos[0],pos[1]+2*jeu[table[pos[1]][pos[0]][0]]])
			if pos[0]!=0:
				if table[pos[1]+jeu[table[pos[1]][pos[0]][0]]][pos[0]-1]!="00" and table[pos[1]+jeu[table[pos[1]][pos[0]][0]]][pos[0]-1][0]!=table[pos[1]][pos[0]][0]:
					points.append([pos[0]-1,pos[1]+jeu[table[pos[1]][pos[0]][0]]])
				else:
					if table[pos[1]][pos[0]][0]=="n" and [pos[0]-1,pos[1]+jeu[table[pos[1]][pos[0]][0]]] in points_unpassun["b"]:
						points.append([pos[0]-1,pos[1]+jeu[table[pos[1]][pos[0]][0]]])
					elif table[pos[1]][pos[0]][0]=="b" and [pos[0]-1,pos[1]+jeu[table[pos[1]][pos[0]][0]]] in points_unpassun["n"]:
						points.append([pos[0]-1,pos[1]+jeu[table[pos[1]][pos[0]][0]]])
			if pos[0]!=7:
				if table[pos[1]+jeu[table[pos[1]][pos[0]][0]]][pos[0]+1]!="00" and table[pos[1]+jeu[table[pos[1]][pos[0]][0]]][pos[0]+1][0]!=table[pos[1]][pos[0]][0]:
					points.append([pos[0]+1,pos[1]+jeu[table[pos[1]][pos[0]][0]]])
				else:
					if table[pos[1]][pos[0]][0]=="n" and [pos[0]+1,pos[1]+jeu[table[pos[1]][pos[0]][0]]] in points_unpassun["b"]:
						points.append([pos[0]+1,pos[1]+jeu[table[pos[1]][pos[0]][0]]])
					elif table[pos[1]][pos[0]][0]=="b" and [pos[0]+1,pos[1]+jeu[table[pos[1]][pos[0]][0]]] in points_unpassun["n"]:
						points.append([pos[0]+1,pos[1]+jeu[table[pos[1]][pos[0]][0]]])	
		return points

	def AfficheurPoints(Emplacement,DéplacementLong,points,case):
		if DéplacementLong:
			for i in Emplacement:
				obool=True
				while obool:
					if 8>(case[1]+i[1])>=0 and 8>(case[0]+i[0])>=0 :
						if table[case[1]+i[1]][case[0]+i[0]]=="00":
							points.append([case[0]+i[0],case[1]+i[1]])
						else:
							if table[case[1]][case[0]][0]!=table[case[1]+i[1]][case[0]+i[0]][0]:
								points.append([case[0]+i[0],case[1]+i[1]])
							obool=False
					else:
						obool=False
					if i[2][0]=="n":
							i[1]-=1
					elif i[2][0]=="e":
							i[0]+=1
					elif i[2][0]=="s":
							i[1]+=1
					elif i[2][0]=="w":
							i[0]-=1
					if i[2][1]=="w":
							i[0]-=1
					elif i[2][1]=="e":
							i[0]+=1
		else:
			for i in Emplacement:
				if 8>(case[1]+i[1])>=0 and 8>(case[0]+i[0])>=0 :
					if table[case[1]+i[1]][case[0]+i[0]]=="00":
						points.append([case[0]+i[0],case[1]+i[1]])
					elif table[case[1]][case[0]][0]!=table[case[1]+i[1]][case[0]+i[0]][0]:
						points.append([case[0]+i[0],case[1]+i[1]])
		return points

	def KingScan(table,couleur):
		i=j=7
		x_king=[-1,-1]
		while x_king==[-1,-1]:
			if table[j][i]==couleur+"k":
				x_king=[i,j]
			else:
				i-=1
				if i<0:
					i=7
					j-=1
		return x_king

	def AffichagePromotion(clique):
		obool=True
		clique_pos=[-1,-1]
		if clique[0]==8:
			clique[0]-=2
		if clique[1]==0:
			screen.blit(promotion[jeu["joueur"]+"0"],(clique[0]*60,0))
		else:
			screen.blit(promotion[jeu["joueur"]+"7"],(clique[0]*60,240))
		while obool:
			for event in pygame.event.get():
				if event.type==QUIT:
					obool=False
					partie=False
					end=False
				if event.type==MOUSEBUTTONUP:
					clique_pos[0]=pygame.mouse.get_pos()[0]//60
					clique_pos[1]=pygame.mouse.get_pos()[1]//60
					if clique[0]!=clique_pos[0] or not (0<=abs(clique[1]-clique_pos[1])<4):
						clique_pos=[-1,-1]
			if clique_pos!=[-1,-1]:
				if abs(clique[1]-clique_pos[1])==0:
					return jeu["joueur"]+"q"
				elif abs(clique[1]-clique_pos[1])==1:
					return jeu["joueur"]+"r"
				elif abs(clique[1]-clique_pos[1])==2:
					return jeu["joueur"]+"b"
				else:
					return jeu["joueur"]+"c"
			pygame.display.flip()

	screen=pygame.display.set_mode((480,480))
	echiquier=pygame.image.load("image/echiquier.png").convert()
	menu=pygame.image.load("image/menu.png").convert()
	point=pygame.image.load("image/point.png").convert()			#60X60
	point.set_colorkey(BLANC)
	marque=pygame.image.load("image/marque.png").convert()
	marque.set_colorkey(BLANC)
	point_castle=pygame.image.load("image/point_castle.png").convert()
	point_castle.set_colorkey(BLANC)
	marque_check=pygame.image.load("image/marque_check.png").convert()
	marque_check.set_colorkey(BLANC)
	b_checkmate=pygame.image.load("image/b_panneau_checkmate.png").convert()
	n_checkmate=pygame.image.load("image/n_panneau_checkmate.png").convert()
	promotion_b7=pygame.image.load("image/promotion_b7.png").convert()
	promotion_b0=pygame.image.load("image/promotion_b0.png").convert()
	promotion_n7=pygame.image.load("image/promotion_n7.png").convert()
	promotion_n0=pygame.image.load("image/promotion_n0.png").convert()
	b_pion=pygame.image.load("image/b_pion.png").convert()		#60X60
	b_pion.set_colorkey(BLANC)
	n_pion=pygame.image.load("image/n_pion.png").convert()
	n_pion.set_colorkey(BLANC)
	b_cavalier=pygame.image.load("image/b_cavalier.png").convert()
	b_cavalier.set_colorkey(BLANC)
	n_cavalier=pygame.image.load("image/n_cavalier.png").convert()
	n_cavalier.set_colorkey(BLANC)
	b_fou=pygame.image.load("image/b_fou.png").convert()
	b_fou.set_colorkey(BLANC)
	n_fou=pygame.image.load("image/n_fou.png").convert()
	n_fou.set_colorkey(BLANC)
	b_tour=pygame.image.load("image/b_tour.png").convert()
	b_tour.set_colorkey(BLANC)
	n_tour=pygame.image.load("image/n_tour.png").convert()
	n_tour.set_colorkey(BLANC)
	b_reine=pygame.image.load("image/b_reine.png").convert()
	b_reine.set_colorkey(BLANC)
	n_reine=pygame.image.load("image/n_reine.png").convert()
	n_reine.set_colorkey(BLANC)
	b_roi=pygame.image.load("image/b_roi.png").convert()
	b_roi.set_colorkey(BLANC)
	n_roi=pygame.image.load("image/n_roi.png").convert()
	n_roi.set_colorkey(BLANC)
	blanc={"p":b_pion,"c":b_cavalier,"b":b_fou,"r":b_tour,"q":b_reine,"k":b_roi}
	noir={"p":n_pion,"c":n_cavalier,"b":n_fou,"r":n_tour,"q":n_reine,"k":n_roi}
	panneau_checkmate={"n":b_checkmate,"b":n_checkmate}		#200X200
	promotion={"b7":promotion_b7,"b0":promotion_b0,"n7":promotion_n7,"n0":promotion_n0}		#60X300

	menu_principale=True
	partie=True
	end=True
				#Menu Principale
	while menu_principale:
		for event in pygame.event.get():
			if event.type==QUIT:
				menu_principale=False
				partie=False
				end=False
			if event.type==MOUSEBUTTONUP:			
				if pygame.mouse.get_pos()[0]<240:
					table=Positionnement("Blanc")
					pos_king=KingScan(table,"b")
					bk=KingsInstance("b",pos_king[0],pos_king[1])
					if pos_king!=(4,7):
						bk.moved=True
					pos_king=KingScan(table,"n")
					nk=KingsInstance("n",pos_king[0],pos_king[1])
					if pos_king!=(4,0):
						nk.moved=True
					jeu={"b":-1,"n":1,"joueur":"b"} 
				else:
					table=Positionnement("Noir")
					pos_king=KingScan(table,"b")
					bk=KingsInstance("b",pos_king[0],pos_king[1])
					if pos_king!=(3,0):
						bk.moved=True
					pos_king=KingScan(table,"n")
					nk=KingsInstance("n",pos_king[0],pos_king[1])
					if pos_king!=(3,7):
						nk.moved=True
					jeu={"b":1,"n":-1,"joueur":"b"}
				Kings={"b":bk,"n":nk}
				menu_principale=False
		screen.blit(menu,(0,0))
		pygame.display.flip()

				#Partie en cours
	while partie:
		pygame.time.wait(FPS)
		if mouse_pos!=[-1,-1]:
			old_mouse_pos=mouse_pos
		mouse_pos=[-1,-1]
		for event in pygame.event.get():
			if event.type==QUIT:
				partie=False
				end=False
			if event.type==MOUSEBUTTONDOWN:
				mouse_pos[0]=pygame.mouse.get_pos()[0]
				mouse_pos[1]=pygame.mouse.get_pos()[1]
			if event.type==KEYDOWN:
				if event.key==K_ESCAPE:
					mouse_pos=old_mouse_pos=[-1,-1]
					points=[]

				#Traitement des cliques
		if mouse_pos!=[-1,-1]:
			mouse_pos=[mouse_pos[0]//60,mouse_pos[1]//60]
				#Traitement déplacement
			if mouse_pos in points:
				if table[old_mouse_pos[1]][old_mouse_pos[0]][1]=="p":
					if table[mouse_pos[1]][mouse_pos[0]]=="00" and abs(mouse_pos[0]-old_mouse_pos[0])==1:
						table[mouse_pos[1]-jeu[jeu["joueur"]]][mouse_pos[0]]="00"
					table[mouse_pos[1]][mouse_pos[0]]=table[old_mouse_pos[1]][old_mouse_pos[0]][0]+"p1"
					if abs(mouse_pos[1]-old_mouse_pos[1])==2:
						points_unpassun[jeu["joueur"]].append([old_mouse_pos[0],old_mouse_pos[1]+jeu[jeu["joueur"]]])
					elif mouse_pos[1]==3.5*(1+jeu[jeu["joueur"]]):
						points=[]
						table[mouse_pos[1]][mouse_pos[0]]=AffichagePromotion([mouse_pos[0]+1,mouse_pos[1]])
				else:
					if table[old_mouse_pos[1]][old_mouse_pos[0]][1]=="k":
						Kings[table[old_mouse_pos[1]][old_mouse_pos[0]][0]].posx=mouse_pos[0]
						Kings[table[old_mouse_pos[1]][old_mouse_pos[0]][0]].posy=mouse_pos[1]
						Kings[jeu["joueur"]].moved=True
					if table[old_mouse_pos[1]][old_mouse_pos[0]][1]=="r" and not Kings[jeu["joueur"]].moved:
						if abs(Kings[jeu["joueur"]].posx-old_mouse_pos[0])==3:
							Kings[jeu["joueur"]].K_rook=True
						else:
							Kings[jeu["joueur"]].Q_rook=True
					table[mouse_pos[1]][mouse_pos[0]]=table[old_mouse_pos[1]][old_mouse_pos[0]]

				table[old_mouse_pos[1]][old_mouse_pos[0]]="00"
				mouse_pos=old_mouse_pos=[-1,-1]
				points=[]
				Kings[jeu["joueur"]].K_castle=False
				Kings[jeu["joueur"]].Q_castle=False
				#Bascule de joueur
				if jeu["joueur"]=="b":
					jeu["joueur"]="n"
				else:
					jeu["joueur"]="b"
				#Nettoyage de UnPassUn
				points_unpassun[jeu["joueur"]]=[]
				#Recherche de "check"
				Kings["b"].check=Kings["b"].CheckInstance()
				Kings["n"].check=Kings["n"].CheckInstance()
				#Recherche de "CheckMate"
				if Kings[jeu["joueur"]].check:
					Kings[jeu["joueur"]].CheckMate=Kings[jeu["joueur"]].CheckMateInstance(points)
			elif mouse_pos==old_mouse_pos:
				mouse_pos=old_mouse_pos=[-1,-1]
				points=[]
				Kings[jeu["joueur"]].K_castle=False
				Kings[jeu["joueur"]].Q_castle=False
			elif table[mouse_pos[1]][mouse_pos[0]][0]==jeu["joueur"] :
				Kings[jeu["joueur"]].K_castle=False
				Kings[jeu["joueur"]].Q_castle=False
				#Création des points
				points=CréationDesPoints(points,mouse_pos)
				#Traitement des points
				i=len(points)-1
				while i>=0:
					mémoire1=table[points[i][1]][points[i][0]]
					table[points[i][1]][points[i][0]]=table[mouse_pos[1]][mouse_pos[0]]
					table[mouse_pos[1]][mouse_pos[0]]="00"
					if table[points[i][1]][points[i][0]][1]=="k":
						mémoire2=Kings[jeu["joueur"]].CheckInstance(points[i][0],points[i][1])
					else:
						mémoire2=Kings[jeu["joueur"]].CheckInstance()
					table[mouse_pos[1]][mouse_pos[0]]=table[points[i][1]][points[i][0]]
					table[points[i][1]][points[i][0]]=mémoire1
					if mémoire2 :
						del points[i]
					i-=1
				#Traitement castling
				if table[mouse_pos[1]][mouse_pos[0]][1]=="k":
					if not Kings[jeu["joueur"]].moved and (not Kings[jeu["joueur"]].K_rook or not Kings[jeu["joueur"]].Q_rook):
						Kings[jeu["joueur"]].Castle()
			elif table[old_mouse_pos[1]][old_mouse_pos[0]][1]=="k" and not Kings[jeu["joueur"]].moved: 
				if (mouse_pos[0],mouse_pos[1])==(Kings[jeu["joueur"]].posx-(2*jeu["b"]),Kings[jeu["joueur"]].posy) and Kings[jeu["joueur"]].K_castle:
					table[mouse_pos[1]][mouse_pos[0]]=table[old_mouse_pos[1]][old_mouse_pos[0]]
					Kings[jeu["joueur"]].posx=mouse_pos[0]
					Kings[jeu["joueur"]].posy=mouse_pos[1]
					table[old_mouse_pos[1]][old_mouse_pos[0]]="00"
					table[Kings[jeu["joueur"]].posy][Kings[jeu["joueur"]].posx+jeu["b"]]=table[Kings[jeu["joueur"]].posy][Kings[jeu["joueur"]].posx-jeu["b"]]
					table[Kings[jeu["joueur"]].posy][Kings[jeu["joueur"]].posx-jeu["b"]]="00"
					Kings[jeu["joueur"]].K_castle=False
					Kings[jeu["joueur"]].Q_castle=False
					Kings[jeu["joueur"]].moved=True
					mouse_pos=old_mouse_pos=[-1,-1]
					points=[]
					#Bascule de joueur
					if jeu["joueur"]=="b":
						jeu["joueur"]="n"
					else:
						jeu["joueur"]="b"
				elif (mouse_pos[0],mouse_pos[1])==(Kings[jeu["joueur"]].posx+(2*jeu["b"]),Kings[jeu["joueur"]].posy) and Kings[jeu["joueur"]].Q_castle:
					table[mouse_pos[1]][mouse_pos[0]]=table[old_mouse_pos[1]][old_mouse_pos[0]]
					Kings[jeu["joueur"]].posx=mouse_pos[0]
					Kings[jeu["joueur"]].posy=mouse_pos[1]
					table[old_mouse_pos[1]][old_mouse_pos[0]]="00"
					table[Kings[jeu["joueur"]].posy][Kings[jeu["joueur"]].posx-jeu["b"]]=table[Kings[jeu["joueur"]].posy][Kings[jeu["joueur"]].posx+(jeu["b"]*2)]
					table[Kings[jeu["joueur"]].posy][Kings[jeu["joueur"]].posx+(jeu["b"]*2)]="00"
					Kings[jeu["joueur"]].K_castle=False
					Kings[jeu["joueur"]].Q_castle=False
					Kings[jeu["joueur"]].moved=True
					mouse_pos=old_mouse_pos=[-1,-1]
					points=[]
					#Bascule de joueur
					if jeu["joueur"]=="b":
						jeu["joueur"]="n"
					else:
						jeu["joueur"]="b"
				else:
					Kings[jeu["joueur"]].K_castle=False
					Kings[jeu["joueur"]].Q_castle=False
					mouse_pos=old_mouse_pos=[-1,-1]
					points=[]
			else:
				Kings[jeu["joueur"]].K_castle=False
				Kings[jeu["joueur"]].Q_castle=False
				mouse_pos=old_mouse_pos=[-1,-1]
				points=[]
		
		screen.blit(echiquier,(0,0))
				#Affichage des pièces
		for i in range(8):
			for j in range(8):
				if table[i][j][0]=="b":
					screen.blit(blanc[table[i][j][1]],(j*60,i*60))
				elif table[i][j][0]=="n":
					screen.blit(noir[table[i][j][1]],(j*60,i*60))

				#Affichage des points
		for i in points:
			if table[i[1]][i[0]]=="00":
				screen.blit(point,(i[0]*60,i[1]*60))
			else:
				screen.blit(marque,(i[0]*60,i[1]*60))

				#Affichage des "Castle"
		if Kings[jeu["joueur"]].K_castle:
			screen.blit(point_castle,((Kings[jeu["joueur"]].posx-(2*jeu["b"]))*60,(Kings[jeu["joueur"]].posy)*60))
		if Kings[jeu["joueur"]].Q_castle:
			screen.blit(point_castle,((Kings[jeu["joueur"]].posx+(2*jeu["b"]))*60,(Kings[jeu["joueur"]].posy)*60))
			
				#Affichage des "check"
		if Kings[jeu["joueur"]].check:
			screen.blit(marque_check,(Kings[jeu["joueur"]].posx*60,Kings[jeu["joueur"]].posy*60))
		if Kings[jeu["joueur"]].CheckMate:
			screen.blit(panneau_checkmate[jeu["joueur"]],(140,140))
			partie=False
		pygame.display.flip()
				#Fin de partie
	while end:
		for event in pygame.event.get():
			if event.type==QUIT or event.type==KEYDOWN or event.type==MOUSEBUTTONDOWN:
				end=False

if __name__ == "__main__":
	lunch_game()