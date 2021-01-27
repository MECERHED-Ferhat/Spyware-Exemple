import pygame,os
from pygame.locals import *

os.chdir(os.path.dirname(__file__))
BLANC=(255,255,255)

def Positionnement(position):
	if position=="Blanc":
		table=[
	  		["nr","nc","nb","nq","nk","nb","nc","nr"],
			["np0","np0","np0","np0","np0","np0","np0","np0"],
			["00","00","00","00","00","00","00","00"],
			["00","00","00","00","00","00","00","00"],
			["00","00","00","00","00","00","00","00"],
			["00","00","00","00","00","00","00","00"],
			["bp0","bp0","bp0","bp0","bp0","bp0","bp0","bp0"],
			["br","bc","bb","bq","bk","bb","bc","br"]
	  	]
	elif position=="Noir":
		table=[
			["br","bc","bb","bk","bq","bb","bc","br"],
			["bp0","bp0","bp0","bp0","bp0","bp0","bp0","bp0"],
			["00","00","00","00","00","00","00","00"],
			["00","00","00","00","00","00","00","00"],
			["00","00","00","00","00","00","00","00"],
			["00","00","00","00","00","00","00","00"],
			["np0","np0","np0","np0","np0","np0","np0","np0"],
			["nr","nc","nb","nk","nq","nb","nc","nr"]
	  	]
	return table

