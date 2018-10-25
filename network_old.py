#!/usr/bin/python
#addr=[]
#possiblemasks=[]

import sys
from PyQt4 import QtCore, QtGui

class Window(QtGui.QDialog):

    def __init__(self):
	QtGui.QDialog.__init__(self)
	self.initUI()

    def initUI(self):
	btn = QtGui.QPushButton('OK', self)
	btn.setGeometry(100,100,100,20)
	self.connect(btn, QtCore.SIGNAL('clicked()'), quit)
	self.setGeometry(300,300,300,200)
	self.setWindowTitle('Programm')

app = QtGui.QApplication(sys.argv)
w = Window()
w.show()


ss=[0, 0, 0, 0]
s=raw_input("Enter IP-adress: ")
m=raw_input("Enter mask: ")
m = m.split('.')
s = s.split('.')
for j in range(4):
    m[j] = int(m[j])
    s[j] = int(s[j])
if any([i>255 or i<0 for i in m]):
	print ValueError("Invalid mask")
if any([i>255 or i<0 for i in s]):
	print ValueError("Invalid IP")
else:
	poolsize = (256 - m[0]) * (256 - m[1]) * (256 - m[2]) * (256 - m[3])
	
	for i in range(4):
		if poolsize == 1:
			if i == 0:
				for j in range(4):
				    ss[j] = str(s[j])
#				addr.append(".".join(ss))
				print ".".join(ss)				#ss[0],'.',ss[1],'.',ss[2],'.',ss[3]	
				break
			else:
				s[3-i+1]=0
				for w in range(255):
						#s[3-i+1]=0
						if i>1:
							s[3-i+2]=0
							for e in range(255):
							 if i>2:
								s[3-i+3]=0
								for r in range(255):
							   	  for j in range(4):
								    ss[j] = str(s[j])
								  print ".".join(ss)
#								  addr.append(".".join(ss))
								  s[3-i+3] += 1
							 else:
							  for j in range(4):
							    ss[j] = str(s[j])
                                                          
							  print ".".join(ss)
#							  addr.append(".".join(ss))
							 s[3-i+2] += 1
						else:
						 for j in range(4):
						    ss[j] = str(s[j])
						 print ".".join(ss)
#						 addr.append(".".join(ss))
						s[3-i+1] += 1
				#print(addr)
				break
		elif poolsize > 255:
			poolsize /= 256
			s[3-i] = 0
			continue
		elif poolsize > 1 and poolsize < 256:
			s[3-i]-=s[3-i]%poolsize
			for j in range(4):
			    ss[j] = str(s[j])
#			addr.append(".".join(ss))
			print "Netadress: ", ".".join(ss)				#ss[0],'.',ss[1],'.',ss[2],'.',ss[3]	
			for q in range(1,poolsize):
				if i>0:
					s[3-i+1]=0
					for w in range(256):
						if i>1:
							s[3-i+2]=0
							for e in range(256):
							  if i>2:
								s[3-i+3]=0
								for r in range(256):
								  for j in range(4):
								    ss[j] = str(s[j])
								  print '1++', ".".join(ss)
								  addr.append(".".join(ss))
								  s[3-i+3] += 1
							  else:
							   for j in range(4):
							    ss[j] = str(s[j])
                                                          
							   print ".".join(ss)
#							   addr.append(".".join(ss))
							  s[3-i+2] += 1
						else:
						 for j in range(4):
						    ss[j] = str(s[j])
						 print ".".join(ss)
#						 addr.append(".".join(ss))
						s[3-i+1] += 1
				else:
					 for j in range(4):
					    ss[j] = str(s[j])
					 print ".".join(ss)
#					 addr.append(".".join(ss))
				s[3-i]+=1
			#print addr
			print '///', ".".join(ss)
			break

sys.exit(app.exec_())