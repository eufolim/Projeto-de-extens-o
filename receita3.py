import os, sys
import keyboard
import pandas as pd
import pickle as pk
from quantulum3 import parser
from deep_translator import GoogleTranslator as gt

areceita = ""
receitas=[]
cursorY = -1
cursorX = 0
window = "menu"

class receita:
    def __init__(self,nome,ingredientes,resultado) -> None:
        self.nome = nome
        self.ingredientes = ingredientes
        self.resultado = resultado
    
    def ajustes(self,valor):
        ajuste = float(valor)/float(self.resultado["valor"])
        for x in self.ingredientes :
            x.ajustes(ajuste)

class ingrediente:
    def __init__(self,uni,valor,nome) -> None:
        self.uni = uni
        self.valor = valor
        self.nome = nome
        
    def ajustes(self,valor):
        self.valor = self.valor*float(valor)
     
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
        
def enter(receitas):
    global cursorY, cursorX, window, areceita
    if window == int:
        if cursorX == 0:
            cursorX = 0
            window = "ajustar"
            areceita = receitas[cursorY]
            keyboard.wait("enter",True,True)
            ajustar(window)
        elif cursorX == 1:
            cursorX = 0
            cursorY = 0
            keyboard.wait("enter",True,True)
            deletar(receitas[cursorY])
            menu(search())
        elif cursorX ==2:
            cursorX = 0
            window = "menu"
            keyboard.wait("enter",True,True)
            unHook()
            menu(receitas)
    if window == "menu":
        if len(receitas) == 0:
            if cursorX == 0:
                window = "incluir"
                keyboard.wait("enter",True,True)
                unHook()
                incluir(receitas)
            if cursorX == 1:
                exit()
        elif cursorY == len(receitas) or cursorY == -1:
            if cursorX == 0:
                window = "incluir"
                keyboard.wait("enter",True,True)
                unHook()
                incluir(receitas)
            if cursorX == 1:
                pass
                #reset("deletar")
                #deletar(receitas)
            if cursorX == 2:
                exit()
        else:
            window = int(cursorY)
            keyboard.wait("enter",True,True)
            unHook()
            menu(receitas)   
    elif window == "ajustar" :
        if cursorX == 0 :
            cursorX = 0
            window = "ajuste"
            unHook()
            ajustar(window)
        elif cursorX == 1 :
            cursorX = 0
            window = "menu"
            unHook()
            menu(receitas)

def key(value):
    global cursorY, cursorX, receitas, areceita
    try: window == int(window)
    except: pass
    else:
        if value.name == "left" and cursorX > 0 :
            cursorX -= 1
        if value.name == "right" and cursorX < 2 :
            cursorX += 1
        display(receitas,cursorY,cursorX,window)
    if window == "menu":
        if value.name == "up" and cursorY > -1 :
            cursorY -= 1
        if value.name == "down" and cursorY < len(receitas) :
            cursorY += 1
        if value.name == "right" and (cursorY == len(receitas) or cursorY == -1) :
            if len(receitas) == 0 and cursorX < 1:
                cursorX += 1
            elif cursorX < 2:
                cursorX += 1
        if value.name == "left" and (cursorY == len(receitas) or cursorY == -1 )and cursorX > 0:
            cursorX -= 1
        display(receitas,cursorY,cursorX,window)
    if window == "ajustar":
        if value.name == "left" and cursorX > 0 :
            cursorX -= 1
        if value.name == "right" and cursorX < 1 :
            cursorX += 1
        adisplay(areceita,cursorX,window)
        
def search():
    global receitas
    receitas = []
    files = os.listdir("saves2/")
    for x in files:
        receitas.append(pk.load(open("saves2/"+x,"rb")))
    return receitas
        
def incluir(receitas):
    os.system("cls")
    nomeReceita = str(input("Nome da receita\n-> "))
    print("")
    ingredientes = []
    count = 0
    while True :
        count += 1
        item = input(" "+str(count)+") Item: ")
        if item == "" :
            print("\033[F\033[K")
            break
        print("\033[F",str(count)+") Item:",item,end="")
        valor = int(input("  Valor: "))
        print("\033[F",str(count)+") Item:",item,"  Valor:",valor,end="")
        uni = input("  Unidade: ")
        ingredientes.append(ingrediente(uni,valor,item))
    texto = str(input("Quantidade resultante: "))
    value = parser.parse(texto)
    resultado = {"texto":texto,"valor":value[0].value}
    salvar = receita(nomeReceita,ingredientes,resultado)
    pk.dump(salvar,open("saves2/"+salvar.nome,"wb"))
    receitas.append(salvar)
    hook()
    menu(receitas)
    
def menu(receitas):
    global window, cursorY, cursorX
    hook()
    display(receitas,cursorY,cursorX,window)
    keyboard.wait("enter",True)
    enter(receitas)
    
def display(receitas,cursorY,cursorX,window):
    os.system("cls")
    if receitas == [] :
        print("- Nenhuma receita cadastrada -\n") 
        if cursorY == -1 :
            if cursorX == 0:
                print("[Nova]"," Sair ")
            else :
                print(" Nova ","[Sair]")
    elif window == "menu" or window == int:
        if cursorY == -1 :
            if cursorX == 0:
                print("[Nova]"," Buscar "," Sair ")
            elif cursorX == 1:
                print(" Nova ","[Buscar]"," Sair ")
            else :
                print(" Nova "," Buscar ","[Sair]")
        else:
            print(" Nova "," Buscar ", " Sair")
        print("\nReceitas:\n")
        #size = 3
        #if cursorY == len(receitas) or cursorY == 0:
            #test = size
        #else:
            #test = size-2
        #count = 0
        for x in range(0,len(receitas)) :
            #if count < size:
                #if x in range(cursorY-test,cursorY+test+1):
                    #count += 1
                    if x == window :
                        print("> "+receitas[x].nome)
                        if cursorX == 0:
                            print("    [Alterar]"," Deletar "," Voltar ")
                        elif  cursorX == 1:
                            print("     Alterar ","[Deletar]"," Voltar ")
                        elif cursorX == 2:
                            print("     Alterar "," Deletar ","[Voltar]")
                    else:
                        print("> "+receitas[x].nome if x == cursorY else "  "+receitas[x].nome)
        print("")
        if cursorY == len(receitas) :
            if cursorX == 0:
                print("[Nova]"," Buscar "," Sair ")
            elif cursorX == 1:
                print(" Nova ","[Buscar]"," Sair ")
            else :
                print(" Nova "," Buscar ","[Sair]")
        else:
            print(" Nova "," Buscar ", " Sair")

def adisplay(receita,cursorX,window):
    os.system("cls")
    print(receita.nome,"\n")
    for x in receita.ingredientes :
        print(x.valor,x.uni,x.nome)
    print("\nFaz:",receita.resultado["texto"],"\n")
    if window == "ajustar" :
        if cursorX == 0:
            print("[Ajustar]"," Voltar ")
        else:
            print(" Ajustar ","[Voltar]")


def ajustar(window):
    global areceita, receitas, cursorX
    adisplay(areceita,cursorX,window)
    if window == "ajuste":
        ajuste = input("Ajuste: ")
        areceita.ajustes(ajuste)
        window = "ajustar"
        ajustar(window)
    keyboard.wait("enter",True,True)
    enter(receitas)
    ajustar(window)
              
def deletar(receita):
    os.remove("saves/"+receita.nome)

                    
menu(search())