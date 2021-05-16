#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  app.py
#  
#  Copyright 2021 William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys;
import uuid;
from walsoc import *;
import time;


def val(num=None,dbg=False):
	out=0.0;#output
	sg=1;	#sign
	flg=0;	#flag (number started)
	fp=0;	#flag (decimal point position negative)
	
	for f in str(num):
		if(f=="-"):
			sg*=-1;
		else:
			if(not flg):
				if(('0'<=f	and
					f<='9') or
					f=="."):
						flg=1;
						if(f=="."):
							fp=1;
						else:
							if(fp):
								out+=int(f)*(10**(-fp));
								if(dbg):
									print("D:",out,"\t",int(f),"x10^",(-fp));
								fp+=1;
							else:
								out=out*10+int(f);
								if(dbg):
									print("E:",out);
			else:
				if(('0'<=f	and
					f<='9') or
					f=="."):
					
					flg=1;
					if(f=="."):
						fp=1;
					else:
						if(fp):
							out+=int(f)*(10**(-fp));
							if(dbg):
								print("D:",out,"\t",int(f),"x10^",(-fp));
							fp+=1;
							
						else:
							out=out*10+int(f);
							if(dbg):
								print("E:",out);
				else:
					break;
	if(fp>0):
		out=int(out*(10**(fp-1)));
		out=float(sg*out*(10**(-fp+1)));
	else:
		out=out*sg;
		
	return(out);

BR="\n";

def timer():
	return(time.time());

def iconify():
	pygame.display.iconify();
	
def pause(n=0,msg=None):
	
	if (n==0):
		if(msg==None):
			msg="Press a key to continue...";
		print(msg);
		return(getkey());
	else:
		p=timer();
		while(timer()<(p+n)):
			pass;
		#return(inkey());
	
class Property:
	default="property";
	nr=0;
	def __init__(self,name=None,value=None):
		if(name==None):
			nr+=1;
			name=default+("%09d"%nr);
		
		self.name=name;
		self.value=value;
		
		
	def setValue(self,value=None):
		self.value=value;
	
	def getValue(self):
		return(self.value);
	
	def getName(self):
		return(self.name);
	
	def __repr__(self):
		return(str(self.name)+":"+str(self.value));


class baseData:
	Ids=[];
	Names=[];
	
def getUniq(valor=None):
	if (valor==None):
		valor=uuid.uuid4().int;
	else:
		if(len(Component.Ids)>0):
			valor=(uuid.uuid1(node=max(Component.Ids)).int)%2207 +3;
		else:
			valor=(uuid.uuid1(node=22).int)% 2207+1;
	while(valor in baseData.Ids):
		valor=uuid.uuid4().int;
	return(valor);

def inList(what,where):
	try:
		out=where.index(what);
	except:
		out=-1;
	return(out);

def filterName(st):
	s=str(st).capitalize();
	s=s.split(":");
	out="_".join(s);
	return(out);
	
class Component(baseData):
	Components=[];
	Required=	"name,id";
	Properties=	"name,description,id,bgcolor,bgimage,bglayout,"+\
	"class,cursor,enabled,font,forecolor,help,icon,"+\
	"maximize,minimize,opacity,padding,"+\
	"righttoleft,showicon,showintaskbar,"+\
	"value,height,width,minheight,minwidth,maxheight,maxwidth,x,y";
	Defaults=[	None,"Untitled",None,"#000",None,None,
				"standard","default",True,
				"consolan.ttf","#eee",None,None,
				False,False,1.0,[0,0,0,0],
				False,True,True,
				None,640,480,640,480,16384,16384,0,0 ];
	def get(self,what):
		out=None;
		try:
			name=filterName(what);
			for f in self.prop:
				if(f.getName()==name):
					out=f.getValue();
		except:
			pass;
		return(out);
		
	def getDefault(self,name):
		nm=str(name).lower();
		if(inList(nm,Component.Properties.split(","))>=0):
			return(Component.Defaults[inList(nm,Component.Properties.split(","))]);
		else:
			return(None);
	
	def getIndex(self,valor):
		try:
			return(self.ndx.index(valor));
		except:
			return(0);
		
	def __init__(self,**kwargs):
		self.prop=[Property(filterName(f),self.getDefault(f)) for f in Component.Properties.split(",")];
		self.ndx=[f.getName() for f in self.prop];
		
		#print(self.prop);
		for f in kwargs:
			name=filterName(f);
			if(name=="Title"):
				name="Description";
			if(name in self.ndx):
				self.prop[self.getIndex(name)].setValue(kwargs[f]);
			else:
				self.prop.append(Property(name,kwargs[f]));
				self.ndx.append(name);
				
			#print(f,"=",kwargs[f]);
		for f in Component.Required.split(","):
			if(self.prop[self.getIndex(name)].getValue()==None):
				self.prop[self.getIndex(name)].setValue(getUniq());
			
		if(not (self in Component.Components)):
			Component.Components.append(self);
		
		
	def title(self,valor=None):
		if(valor!=None):
			self.prop[self.getIndex("Description")].setValue(valor);
		else:
			return(self.prop[self.getIndex("Description")].getValue());
	
	def set(self,name=None,valor=None):
		if(name==None):
			name="description";
		name=filterName(name);
		if(valor!=None):
			self.prop[self.getIndex(name)].setValue(valor);
		
		return(self.prop[self.getIndex(name)].getValue());
	
	def getProps(self):
		out="";
		for f in self.prop:
			out+=str(f)+BR;
		return(out);
	
	def setPosition(self,x=None,y=None):
		if(x!=None):
			x=val(x);
			self.prop[getIndex("x")].setValue(x);
		if(y!=None):
			y=val(y);
			self.prop[getIndex("y")].setValue(y);
	
	
	def setPos(self,vect=[None,None]):
		try:
			x=vect[0];
			y=vect[1];
			self.setPosition(x,y);
		except:
			pass;
	
def listComponents():
	for f in Component.Components:
		print(f.title());

def main(args):
	Main=Component(Name="Principal",title="No sé",width=320,height=200);
	Main.title("Algo");
	Main.set("description","WhatAnAgenda");
	gotoxy(1,1);
	listComponents();
	print(Main.getProps());
	
	for f in range(5):
		gotoxy(5+f,5);
		color(0,f);
		print(".");
		pause(1);
	pause(0);
	color(7,0);
	clrscr();
	

if __name__ == '__main__':
	iconify();
	clrscr();
	Exit(main(["World"]+list(sys.argv)));
