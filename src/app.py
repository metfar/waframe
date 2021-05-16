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
	
def getUniq(val=None):
	if (val==None):
		val=uuid.uuid4().int;
	else:
		if(len(Component.Ids)>0):
			val=(uuid.uuid1(node=max(Component.Ids)).int)%2207 +3;
		else:
			val=(uuid.uuid1(node=22).int)% 2207+1;
	while(val in baseData.Ids):
		val=uuid.uuid4().int;
	return(val);

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
	
	def getIndex(self,val):
		try:
			return(self.ndx.index(val));
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
		
		
	def title(self,val=None):
		if(val!=None):
			self.prop[self.getIndex("Description")].setValue(val);
		else:
			return(self.prop[self.getIndex("Description")].getValue());
	
	def set(self,name=None,val=None):
		if(name==None):
			name="description";
		name=filterName(name);
		if(val!=None):
			self.prop[self.getIndex(name)].setValue(val);
		
		return(self.prop[self.getIndex(name)].getValue());
	
	def getProps(self):
		out="";
		for f in self.prop:
			out+=str(f)+BR;
		return(out);
	
def listComponents():
	for f in Component.Components:
		print(f.title());

def main(args):
	Main=Component(Name="Principal",title="No sé",width=320,height=200);
	Main.title("Algo");
	Main.set("description","Agenda");
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
