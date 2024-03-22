import os
import pickle as pk

class testClass:
    
    def __init__(self,nome,testValue) -> None:
        self.testValue = testValue
        self.nome = nome

files = os.listdir("saves/")
openFile = []
lista = {}
for x in files:
    openFile.append(pk.load(open("saves/"+x,"rb")))
for x in openFile:
    lista[x.nome] = x
print(lista["test"].testValue)