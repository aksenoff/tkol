# coding: utf-8
from itertools import imap, repeat, chain
from time import sleep
from xmlrpclib import Server
from ubigraph import Ubigraph

U = Ubigraph()
G = U.server.ubigraph
pauses = True
sleepTime = 0.005
sizeDivide = 10
bin = False
nolabels = False

class Node(object):
  def __init__(self, data, vertex):
    self.selfCount, self.leftCount, self.left, self.right, self.next, self.prev = 1, 0, [0], [0], [0], [0]
    self.data, self.vertex = data, vertex
    self.inEdge = None
    
  def printTree(self, k, totalCount):
    rightCount = totalCount - self.selfCount - self.leftCount
    print self.data, ", s=", self.selfCount, ", l=", self.leftCount, ", r=", rightCount
    if self.right[0]:
      for i in xrange(0, k-1): print "|        ",
      self.right[0].printTree(k+1, rightCount)
    else:
      for i in xrange(0, k-1): print "|        ",
      print "--"
    if self.left[0]:
      for i in xrange(0, k-1): print "|        ",
      self.left[0].printTree(k+1, self.leftCount)
    else:
      for i in xrange(0, k-1): print "|        ",
      print "--"

  def LeftRotate(self, tRoot, parentVertex):
      if self.inEdge: self.inEdge.destroy()
      self.right[0].inEdge.destroy()
      if self.right[0].left[0]:  self.right[0].left[0].inEdge.destroy()
      self.inEdge = U.newEdge(self.right[0].vertex, self.vertex, oriented=True)
      if parentVertex: self.right[0].inEdge = U.newEdge(parentVertex, self.right[0].vertex, oriented=True)
      if self.right[0].left[0]: self.right[0].left[0].inEdge = U.newEdge(self.vertex, self.right[0].left[0].vertex, oriented=True)
      buf1, buf2 = self.right[0], self.right[0].left[0]
      self.right[0].leftCount += (self.leftCount + self.selfCount)
      self.right[0].left[0] = self
      self.right[0] = buf2
      tRoot[0] = buf1

  def RightRotate(self, tRoot, parentVertex):
      if self.inEdge: self.inEdge.destroy()
      self.left[0].inEdge.destroy()
      if self.left[0].right[0]:  self.left[0].right[0].inEdge.destroy()
      self.inEdge = U.newEdge(self.left[0].vertex, self.vertex, oriented=True)
      if parentVertex: self.left[0].inEdge = U.newEdge(parentVertex, self.left[0].vertex, oriented=True)
      if self.left[0].right[0]: self.left[0].right[0].inEdge = U.newEdge(self.vertex, self.left[0].right[0].vertex, oriented=True)
      buf1, buf2 = self.left[0], self.left[0].right[0]
      self.leftCount -= self.left[0].leftCount + self.left[0].selfCount
      self.left[0].right[0] = self
      self.left[0] = buf2
      tRoot[0] = buf1

  def addRotateNode(self, data, totalCount, tRoot, parentVertex, difSym, sumTr, rotateCount):
    rightCount = totalCount - self.selfCount - self.leftCount
    print u"В текущем узле", self.data
    self.vertex.set(color="#ff0000")
    if self.data == data:
      print u"Узел найден, увеличиваем"
      self.vertex.set(color="#00ff00")
      sleep(sleepTime) if pauses else raw_input(u"->")
      self.selfCount += 1
      self.vertex.set(size=self.selfCount/sizeDivide)
      self.vertex.set(color="#ffff00")
      if self.left[0] != 0:
        nLeftCount = self.leftCount
        rLeftCount = self.left[0].leftCount
        rRightCount = totalCount - self.left[0].leftCount - self.left[0].selfCount
        if(abs(rightCount - nLeftCount)>abs(rRightCount - rLeftCount)):
          print u"Выполняем правое вращение"
          sleep(sleepTime) if pauses else raw_input(u"->")
          self.RightRotate(tRoot, parentVertex)
          rotateCount[0] += 1
      if self.right[0] != 0:
        nLeftCount = self.leftCount
        rLeftCount = totalCount - rightCount + self.right[0].leftCount
        rRightCount = rightCount - self.right[0].leftCount - self.right[0].selfCount
        if(abs(nLeftCount-rightCount)>abs(rLeftCount - rRightCount)):
          print u"Выполняем левое вращение"
          sleep(sleepTime) if pauses else raw_input(u"->")
          self.LeftRotate(tRoot, parentVertex)
          rotateCount[0] += 1
    elif self.data > data:
      self.leftCount += 1
      if self.left[0] != 0:
        print u"Идем влево"
        sleep(sleepTime) if pauses else raw_input(u"->")
        self.left[0].addRotateNode(data, self.leftCount, self.left, self.vertex, difSym, sumTr, rotateCount)
        self.vertex.set(color="#ffff00")
        sumTr[0] += 1
        nLeftCount = self.leftCount
        rLeftCount = self.left[0].leftCount
        rRightCount = totalCount - self.left[0].leftCount - self.left[0].selfCount
        if(abs(rightCount - nLeftCount)>abs(rRightCount - rLeftCount)):
          print u"Выполняем правое вращение"
          sleep(sleepTime) if pauses else raw_input(u"->")
          self.RightRotate(tRoot, parentVertex)
          rotateCount[0] += 1
      else:
        print u"Создаем левый дочерний узел"
        sleep(sleepTime) if pauses else raw_input(u"->")
        if nolabels: self.left[0] = Node(data, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide))
        else:
          if bin: self.left[0] = Node(data, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide, label=str(data)))
          else: self.left[0] = Node(data, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide, label=chr(data)))
        self.left[0].inEdge = U.newEdge(self.vertex, self.left[0].vertex, oriented=True)
        difSym[0] += 1
        nLeftCount = self.leftCount
        rLeftCount = self.left[0].leftCount
        rRightCount = totalCount - self.left[0].leftCount - self.left[0].selfCount
        if(abs(rightCount - nLeftCount)>abs(rRightCount - rLeftCount)):
          print u"Выполняем правое вращение"
          sleep(sleepTime) if pauses else raw_input(u"->")
          self.RightRotate(tRoot, parentVertex)
          rotateCount[0] += 1
    elif self.right[0] != 0: # self.data < data
      print u"Идем вправо"
      sleep(sleepTime) if pauses else raw_input(u"->")
      self.right[0].addRotateNode(data, rightCount, self.right, self.vertex, difSym, sumTr, rotateCount)
      self.vertex.set(color="#ffff00")
      sumTr[0] += 1
      nLeftCount = self.leftCount
      rLeftCount = totalCount - rightCount + self.right[0].leftCount
      rRightCount = rightCount - self.right[0].leftCount - self.right[0].selfCount
      if(abs(nLeftCount-rightCount)>abs(rLeftCount - rRightCount)):
        print u"Выполняем левое вращение!"
        print self.data
        sleep(sleepTime) if pauses else raw_input(u"->")
        self.LeftRotate(tRoot, parentVertex)
        rotateCount[0] += 1
    else:
      print u"Создаем правый дочерний узел"
      sleep(sleepTime) if pauses else raw_input(u"->")
      if nolabels: self.right[0] = Node(data, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide))
      else:
        if bin: self.right[0] = Node(data, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide, label=str(data)))
        else: self.right[0] = Node(data, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide, label=chr(data)))
      self.right[0].inEdge = U.newEdge(self.vertex, self.right[0].vertex, oriented=True)
      difSym[0] += 1
      nLeftCount = self.leftCount
      rLeftCount = totalCount - rightCount + self.right[0].leftCount
      rRightCount = rightCount - self.right[0].leftCount - self.right[0].selfCount
      if(abs(nLeftCount-rightCount)>abs(rLeftCount - rRightCount)):
        print u"Выполняем левое вращение!!"
        sleep(sleepTime) if pauses else raw_input(u"->")
        self.LeftRotate(tRoot, parentVertex)
        rotateCount[0] += 1
    self.vertex.set(color="#ffff00")

  def AWD(self, data, awd):
    awd[0] += self.selfCount * data
    data += 1
    if self.right[0]: self.right[0].AWD(data, awd)
    if self.left[0]: self.left[0].AWD(data, awd)

def main():
  U.clear()
  if bin: f = file("binary.bin", "rb")
  else: f = file("text.txt", "r")
  print u"Открыт файл"
  sleep(sleepTime) if pauses else raw_input(u"->")
  totalCount, difSym2, sumTr2, awd2, rotateCount2, root2 = 0, [0], [0], [0], [0], [0]
  char = f.read(1)
  c = ord(char)
  #print "Creating root", c, char
  if nolabels: root2[0] = Node(c, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide))
  else:
    if bin: root2[0] = Node(c, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide, label=str(c)))
    else: root2[0] = Node(c, U.newVertex(shape="sphere", color="#ffff00", size=1/sizeDivide, label=chr(c)))
  totalCount += 1
  difSym2[0] += 1
  print u"Корень", c, u"(", char, u") создан"
  for char in chain(iter(imap(f.read, repeat(1)).next, ''),[-1]):
    if char == -1: break
    if bin and (ord(char) == 0 or ord(char) == 85): continue
    totalCount += 1
    c = ord(char)
    print u"Вставляем", c, "(", char, ")"
    sleep(sleepTime) if pauses else raw_input(u"->")
    root2[0].addRotateNode(c, totalCount, root2, None, difSym2, sumTr2, rotateCount2)
  root2[0].printTree(1, totalCount)
  root2[0].AWD(0, awd2)
  print "TotalCount: ", totalCount
  print "Dif Symbols", difSym2[0]
  print "Sum time", sumTr2[0]
  print "AWD", awd2[0]
  print "Rotate Count", rotateCount2[0]
  raw_input(u"Press any key...")

if __name__ == '__main__':
  main()
