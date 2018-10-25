#!/usr/bin/python
#-*- coding: utf8 -*-

import sqlite3 as sqlite
import sys
from PyQt4 import QtGui, QtCore

con = sqlite.connect('network.db')
cur = con.cursor()
cur.execute('create table if not exists network (n int, ip str (255), mask str (255), len int, netadress str (255), Primary key(ip, mask))')
#cur.execute('create table if not exists hosts (n int, host str (255))')
con.commit()
counter = 1
hh = []
del cur


class Window(QtGui.QWidget):

    def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.resize(1350,700)
		self.setWindowTitle(u'Программа')

		self.dbadd = QtGui.QPushButton(u'Рассчитать сеть', self)
		self.showme = QtGui.QPushButton(u'Показать список хостов', self)
		self.dbadd.move(150,110)
		self.dbadd.adjustSize()
		self.showme.adjustSize()
		self.showme.move(300, 600)
		self.line0 = QtGui.QLabel(u'Введите IP-адрес: ', self)
		self.line0.adjustSize()
		self.line1 = QtGui.QLineEdit(self)
		self.line2 = QtGui.QLabel(u'Введите маску: ', self)
		self.line2.adjustSize()
		self.line3 = QtGui.QLineEdit(self)
		self.line0.move(20,40)
		self.line1.move(170,40)
		self.line2.move(20,75)
		self.line3.move(170,75)
		self.line1.adjustSize()
		self.line3.adjustSize()
		self.line1.setFocus()
		self.line = QtGui.QLabel(u'Cписок хостов:', self)
		self.line.move(950,100)
		self.line.adjustSize()

		self.table = QtGui.QTableView()
		self.table.setMaximumSize(500, 400)
		vh = self.table.verticalHeader()
		vh.setVisible(False)

		self.list_of_hosts = QtGui.QListView()
		self.list_of_hosts.setMaximumSize(200, 400)

	#	self.HostsWindow = QtGui.QWidget()

		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.table)
		layout.addWidget(self.list_of_hosts)
		self.setLayout(layout)

    def launchscreen (self):
		global counter
		cur = con.cursor()
		if cur.execute('select * from network').fetchall() == []: counter=1
		else:
			cur_array = []
			cur.execute('select * from network')
			for i in cur:
				cur_array.append(i)
				counter = int(cur_array[len(cur_array)-1][0])+1
			model = MyTable(cur_array)
			self.table.setModel(model)
			self.table.resizeColumnsToContents()
		del cur

#    def show_hosts_init(self, MyTable):
#	self.HostsWindow.setWindowTitle(u'Список хостов')
#	self.HostsWindow.resize(500, 500)
#	self.line = QtGui.QLabel(u'Показать список хостов для сети номер', parent=self.HostsWindow)
#	self.line.move(10,10)
#	self.line.adjustSize()
#	self.line = QtGui.QLineEdit(parent=self.HostsWindow)
#	self.line.move(300,10)
#	self.showok = QtGui.QPushButton('OK', parent=self.HostsWindow)
#	self.showok.move(350,40)
#	self.lines = QtGui.QLabel(parent=self.HostsWindow)
#	self.lines.move(60, 60)
#	self.lines.adjustSize()
#	self.showok.clicked.connect(lambda: self.show_hosts())
#	self.HostsWindow.show()

    def show_hosts(self, MyTable):

	indexes = MyTable.selectedIndexes()
	if not indexes: return
	MyTable.selectRow(indexes[0].row())
	indexes = MyTable.selectedIndexes()
	a = indexes[3].data()
	poolsize = (a.toInt())[0]
	adr = indexes[1].data()
	adr = adr.toString()

        adr = adr.split('.')
	s = [0, 0, 0, 0]
	ss = [0, 0, 0, 0]
	for q in range(4):
	    s[q] = int(adr[q])
	hh = []

	for i in range(4):

		if poolsize == 1:
		    if i == 0:
			for j in range(4):
			    ss[j] = str(s[j])
			hh.append(".".join(ss))
#			cur.execute('update network set netadress=? where n=?', (".".join(ss), counter,))
			break
		    else:
			s[3-i+1]=0
			for j in range(4):
			    ss[j] = str(s[j])
#			cur.execute('update network set netadress=? where n=?', (".".join(ss), counter,))
			for w in range(256):
			    if i>1:
				s[3-i+2]=0
				for e in range(256):
				 if i>2:
				    s[3-i+3]=0
				    for r in range(256):
				      for j in range(4):
				        ss[j] = str(s[j])
				      hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
				      s[3-i+3] += 1
				 else:
				  for j in range(4):
				    ss[j] = str(s[j]) 
				  hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
				 s[3-i+2] += 1
			    else:
			     for j in range(4):
				ss[j] = str(s[j])
			     hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
			    s[3-i+1] += 1
			hh.pop(0)
			hh.pop()
			break

		elif poolsize > 255:
		    poolsize /= 256
		    s[3-i] = 0
		    continue

		elif poolsize > 1 and poolsize < 256:
		    s[3-i]-=s[3-i]%poolsize
		    for j in range(4):
			ss[j] = str(s[j])
#		    cur.execute('update network set netadress=? where n=?', (".".join(ss),counter,))
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
					    hh.append(".".join(ss)) #cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
					  s[3-i+3] += 1
				      else:
					for j in range(4):
					    ss[j] = str(s[j])
					hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
				      s[3-i+2] += 1
				else:
				 for j in range(4):
				    ss[j] = str(s[j])
				 hh.append(".".join(ss)) #cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
				s[3-i+1] += 1
			else:
			 for j in range(4):
			    ss[j] = str(s[j])
			 hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
			s[3-i]+=1
		    hh.pop(0)
		    hh.pop()
		    break

#	hosts = []
#	cur = con.cursor()
#	cur.execute('select host from hosts where n=?', (d[0],))
#	for h in cur:
#	    hosts.append(h)
	model = MyList(hh)
	self.list_of_hosts.setModel(model)
#	del cur

#	self.lines.setText(u'Адреса:\n\t')
#	for i in range (len(hosts)):
#	    self.lines.setText(self.lines.text() + '\n\t %s'%hosts[i])
#	self.lines.adjustSize()

class MyTable(QtCore.QAbstractTableModel):
    def __init__ (self, fromdb, parent=None, *args):
	QtCore.QAbstractTableModel.__init__(self, parent, *args)
	self.array_fromdb = fromdb
	self.colLabels = [u'№', u'IP-адрес', u'Маска', u'Число хостов', u'Адрес сети']
    def rowCount (self, parent):
	return len(self.array_fromdb)
    def columnCount (self, parent):
	return 5
    def data (self, index, role):
	if not index.isValid():
	    return QtCore.QVariant()
	elif role != QtCore.Qt.DisplayRole:
	    return QtCore.QVariant()
	return QtCore.QVariant(QtCore.QString(str(self.array_fromdb[index.row()][index.column()])))
    def headerData(self, section, orientation, role):
	if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
	    return QtCore.QVariant(self.colLabels[section])
	return QtCore.QVariant()

class MyList(QtCore.QAbstractListModel):
    def __init__ (self, fromdb, parent=None, *args):
	QtCore.QAbstractListModel.__init__(self, parent, *args)
	self.hostlist = fromdb
    def rowCount (self, parent):
	return len(self.hostlist)
    def data (self, index, role):
	if not index.isValid():
	    return QtCore.QVariant()
	elif role != QtCore.Qt.DisplayRole:
	    return QtCore.QVariant()
	return QtCore.QVariant(QtCore.QString(str(self.hostlist[index.row()])))


def add_to_database(obj):
    
  global counter
  cur = con.cursor()
  for_table = []
  s = str(obj.line1.text())
  m = str(obj.line3.text())
  try:
    cur.execute('insert into network (n, ip, mask) values (?, ?, ?)', (counter, s, m))
  except Exception:
    print u'Эти данные уже есть в базе'
  else:

    ss=[0, 0, 0, 0]
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
	cur.execute('update network set len=? where n=?', (poolsize,counter,))

	for i in range(4):

		if poolsize == 1:
		    if i == 0:
			for j in range(4):
			    ss[j] = str(s[j])
			cur.execute('update network set netadress=? where n=?', (".".join(ss), counter,))
			break
		    else:
			s[3-i+1]=0
			for j in range(4):
			    ss[j] = str(s[j])
			cur.execute('update network set netadress=? where n=?', (".".join(ss), counter,))
#			for w in range(256):
#			    if i>1:
#				s[3-i+2]=0
#				for e in range(256):
#				 if i>2:
#				    s[3-i+3]=0
#				    for r in range(256):
#				      for j in range(4):
#				        ss[j] = str(s[j])
##				      if r!=0 and r!=255: hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#				      s[3-i+3] += 1
#				 else:
#				  for j in range(4):
#				    ss[j] = str(s[j]) 
##				  if e!=0 and e!=255: hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#				 s[3-i+2] += 1
#			    else:
#			     for j in range(4):
#				ss[j] = str(s[j])
##			     if w!=0 and w!=255: hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#			    s[3-i+1] += 1
			break

		elif poolsize > 255:
		    poolsize /= 256
		    s[3-i] = 0
		    continue

		elif poolsize > 1 and poolsize < 256:
		    s[3-i]-=s[3-i]%poolsize
		    for j in range(4):
			ss[j] = str(s[j])
		    cur.execute('update network set netadress=? where n=?', (".".join(ss),counter,))
#		    for q in range(1,poolsize+1):
#			if i>0:
#			    s[3-i+1]=0
#			    for w in range(256):
#				if i>1:
#				    s[3-i+2]=0
#				    for e in range(256):
#				      if i>2:
#					s[3-i+3]=0
#					for r in range(256):
#					  for j in range(4):
#					    ss[j] = str(s[j])
##					  if r!=0 and r!=255:hh.append(".".join(ss)) #cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#					  s[3-i+3] += 1
#				      else:
#					for j in range(4):
#					    ss[j] = str(s[j])
##					if e!=0 and e!=255: hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#				      s[3-i+2] += 1
#				else:
#				 for j in range(4):
#				    ss[j] = str(s[j])
##				 if w!=0 and w!=255: hh.append(".".join(ss)) #cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#				s[3-i+1] += 1
#			else:
#			 for j in range(4):
#			    ss[j] = str(s[j])
##			 if q!=0 and q!=255: hh.append(".".join(ss))#cur.execute('insert into hosts values(?, ?)', (counter,".".join(ss),))
#			s[3-i]+=1
		    break
	con.commit()
	cur.execute('select * from network')
	for irow in cur:
	    for_table.append(irow)
	model = MyTable(for_table)
	obj.table.setModel(model)
	obj.table.resizeColumnsToContents()
	counter += 1
  finally: del cur




app = QtGui.QApplication(sys.argv)
w = Window()
w.launchscreen()
w.dbadd.clicked.connect(lambda: add_to_database(w))
w.showme.clicked.connect(lambda: w.show_hosts(w.table))
w.show()
sys.exit(app.exec_())