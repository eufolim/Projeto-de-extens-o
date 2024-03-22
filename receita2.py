import os, sys
import keyboard
import pandas as pd
import pickle as pk
from quantulum3 import parser
from deep_translator import GoogleTranslator as gt

receitas = []
cursorY = 0
cursorX = 0
window = "menu"

class receita:
    def __init__(self,nome,ingredientes,resultado) -> None:
        self.nome = nome
        self.ingredientes = ingredientes
        self.resultado = resultado

class ingrediente:
    def __init__(self,quant,string) -> None:
        self.string = string
        self.quant = quant
        
    #def ajustes(self,valor):
        #self.valor = self.valor*float(valor)

def hook():
    keyboard.on_press_key("up",key,True)
    keyboard.on_press_key("down",key,True)
    keyboard.on_press_key("right",key,True)
    keyboard.on_press_key("left",key,True)
    
def unHook():
    keyboard.unhook("up")
    keyboard.unhook("down")
    keyboard.unhook("left")
    keyboard.unhook("right")
    
def reset(newWindow):
    global cursorY, cursorX, window
    cursorY = 0
    cursorX = 0
    window = newWindow

def enter(receitas):
    global cursorY, cursorX, window
    if window == "menu":
        if len(receitas) == 0:
            if cursorX == 0:
                reset("incluir")
                keyboard.wait("enter",True,True)
                unHook()
                incluir(receitas)
            if cursorX == 1:
                exit()
        elif cursorY == len(receitas):
            if cursorX == 0:
                reset("incluir")
                keyboard.wait("enter",True,True)
                unHook()
                incluir(receitas)
            if cursorX == 1:
                reset("deletar")
                deletar(receitas)
            if cursorX == 2:
                exit()
        else:
            pass
    elif window == "deletar":
        if cursorY == len(receitas):
            reset("menu")
            menu(receitas)
        else:
            pass
    
            
        
        
def key(value):
    global cursorY, cursorX, receitas
    if window == "menu":
        if value.name == "up" and cursorY > 0 :
            cursorY -= 1
        if value.name == "down" and cursorY < len(receitas) :
            cursorY += 1
        if value.name == "right" and cursorY == len(receitas) :
            if len(receitas) == 0 and cursorX < 1:
                cursorX += 1
            elif cursorX < 2:
                cursorX += 1
        if value.name == "left" and cursorY == len(receitas) and cursorX > 0:
            cursorX -= 1
        display(receitas,cursorY,cursorX,window)
    if window == "deletar":
        if value.name == "up" and cursorY > 0 :
            cursorY -= 1
        if value.name == "down" and cursorY < len(receitas) :
            cursorY += 1
        display(receitas,cursorY,cursorX,window)
    
def incluir(receitas):
    os.system("cls")
    nomeReceita = str(input("Nome da receita\n-> "))
    print("")
    ingredientes = []
    count = 0
    while True :
        count += 1
        item = input(str(count)+") ")
        quant = parser.parse(
            gt(source="auto",target="en").translate(
            item))
        if quant == [] :
            print("\033[F\033[K")
            break
        ingredientes.append(ingrediente(quant,item))
    texto = str(input("Quantidade resultante: "))
    valor = parser.parse(texto)
    resultado = {"texto":texto,"valor":valor}
    salvar = receita(nomeReceita,ingredientes,resultado)
    pk.dump(salvar,open("saves/"+salvar.nome,"wb"))
    reset("menu")
    hook()
    menu(search())

def search():
    global receitas
    receitas = []
    files = os.listdir("saves/")
    for x in files:
        receitas.append(pk.load(open("saves/"+x,"rb")))
    return receitas

#def start():
#    menu(search(receitas))

def menu(receitas):
    global window
    print("Receitas:\n")
    hook()
    display(receitas,0,0,window)
    keyboard.wait("enter",True)
    enter(receitas)
    
def deletar(receitas):
    global window, cursorY
    print("Receitas:\n")
    display(receitas,0,0,window)
    keyboard.wait("enter",True)
    enter(receitas)
    if cursorY < len(receitas) :
        os.remove("saves/"+receitas[cursorY].nome)
    menu(search())

def display(receitas,cursorY,cursorX,window):
    os.system("cls")
    if window == "menu" :
        if receitas == [] :
            print("- Nenhuma receita cadastrada -\n") 
            if cursorY == len(receitas) :
                if cursorX == 0:
                    print("[Nova]"," Sair ")
                else :
                    print(" Nova ","[Sair]")
        else:
            print("Receitas:\n")
            for x in range(0,len(receitas)) :
                print("> "+receitas[x].nome if x == cursorY else "  "+receitas[x].nome)
            print("")
            if cursorY == len(receitas) :
                if cursorX == 0:
                    print("[Nova]"," Deletar "," Sair ")
                elif cursorX == 1:
                    print(" Nova ","[Deletar]"," Sair ")
                else :
                    print(" Nova "," Deletar ","[Sair]")
            else:
                print(" Nova "," Deletar ", " Sair")
    elif window == "deletar" :
        print("Receitas:\n")
        for x in range(0,len(receitas)) :
            print("> "+receitas[x].nome if x == cursorY else "  "+receitas[x].nome)
        print("")
        if cursorY == len(receitas):
            print("[Voltar]")
        else:
            print(" Voltar ")
    elif window == "ajustar" :
        pass
       
def ajustar(ingredientes,total):
    pass
    
menu(search())

    
receitas.index 