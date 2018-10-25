#!/usr/bin/python

import sqlite3 as sqlite
import sys
from PyQt4 import QtGui, QtCore
#addr=[]
#possiblemasks=[]

con = sqlite.connect('network.db')
cur = con.cursor()
cur.execute("drop table if exists network")
cur.execute("drop table if exists hosts")
cur.execute('create table if not exists network (ip str, mask str, len int, netadress str)')
cur.execute('create table if not exists hosts (host str)')
#def create_database(): pass
#def add_to_database(ip, mask, cnt): pass

class Window(QtGui.QWidget):

    def __init__(self, parent=None):
	QtGui.QWidget.__init__(self, parent)
	self.initUI()

    def initUI(self):
	self.setGeometry(500,500,500,200)
	self.setWindowTitle('Programm')

	self.button = QtGui.QPushButton('OK', self)
	self.button.move(150,70)
#	self.connect(self.button, QtCore.SIGNAL('clicked()'), self.dialog)
#	self.setFocus()
	self.line0 = QtGui.QLabel('Enter IP-adress: ', self)
	self.line1 = QtGui.QLineEdit(self)
	self.line0.move(20,40)
	self.line1.move(130,40)

#	self.dialog()
#    def dialog(self):
#	text, ok = QtGui.QInputDialog.getText(self, 'Programm', 'Enter IP-adress: ')
#	if ok:
#	    self.label.setText(unicode(text))

def pushed(q):
cur.execute('insert into network (ip, mask) values (?, ?)', (s, m))
    
    print (q.line1.text())

app = QtGui.QApplication(sys.argv)
w = Window()
w.button.clicked.connect(lambda: pushed(w))
w.show()

ss=[0, 0, 0, 0]
#s=raw_input("Enter IP-adress: ")
#m=raw_input("Enter mask: ")
#cur.execute('insert into network (ip, mask) values (?, ?)', (s, m))
#print cur.execute('select * from network').fetchall()
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
	cur.execute('update network set len=?', (poolsize,))
	print cur.execute('select * from network').fetchall()
	
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
#							  addr.append(".".join(ss))
							  cur.execute('insert into hosts values(?)', (".".join(ss),))
							  s[3-i+3] += 1
						 else:
						  for j in range(4):
						    ss[j] = str(s[j]) 
						  print ".".join(ss)
#						  addr.append(".".join(ss))
						 s[3-i+2] += 1
					else:
					 for j in range(4):
					    ss[j] = str(s[j])
					 print ".".join(ss)
#					 addr.append(".".join(ss))
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
			y = ".".join(ss)
			print "Netadress: ", ".".join(ss)				#ss[0],'.',ss[1],'.',ss[2],'.',ss[3]	
			cur.execute('update network set netadress=?', (".".join(ss),))
			for q in range(1,poolsize+1):
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
#								  addr.append(".".join(ss))
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
					 cur.execute('insert into hosts values(?)', (".".join(ss),))
				s[3-i]+=1
			#print addr
			print '///', ".".join(ss)
			break
	print cur.execute('select ip from network').fetchall()
	print cur.execute('select * from hosts').fetchall()
	con.commit()

sys.exit(app.exec_())
# add_to_datebase(...)