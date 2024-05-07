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
    
def reset(newWindow):
    global cursorY, cursorX, window
    cursorY = 0
    cursorX = 0
    window = newWindow

def enter(receitas):
    global cursorY, cursorX, window
    try: window == int(window) 
    except:pass
    else:
        if cursorX == 0:
            cursorX = 0
            keyboard.wait("enter",True,True)
            unHook()
            #ajustar(receitas[cursorY])
        elif cursorX == 1:
            pass
        elif cursorX ==2:
            cursorX = 0
            window = "menu"
            keyboard.wait("enter",True,True)
            unHook()
            menu(receitas)
    if window == "menu":
        if len(receitas) == 0:
            if cursorX == 0:
                reset("incluir")
                keyboard.wait("enter",True,True)
                unHook()
                incluir(receitas)
            if cursorX == 1:
                exit()
        elif cursorY == (len(receitas) or -1):
            if cursorX == 0:
                reset("incluir")
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
    #elif window == "deletar":
        #if cursorY == len(receitas):
            #reset("menu")
            #menu(receitas)
        #else:
            #pass
    
            
        
        
def key(value):
    global cursorY, cursorX, receitas
    try: window == int(window)
    except: pass
    else:
        if value.name == "left" and cursorX > 0 :
            cursorX -= 1
        if value.name == "right" and cursorX < 2 :
            cursorX += 1
        display(receitas,cursorY,cursorX,window)
    if window == "menu":
        if value.name == "up" and cursorY > 0 :
            cursorY -= 1
        if value.name == "down" and cursorY < len(receitas) :
            cursorY += 1
        if value.name == "right" and cursorY == len(receitas):
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
    global window, cursorY, cursorX
    print("Receitas:\n")
    hook()
    display(receitas,cursorY,cursorX,window)
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

def display(receitas,cursorY,cursorX,window,):
    os.system("cls")
    if window == "menu" or window == int(window):
        #if cursorY == -1 :
            #if cursorX == 0:
                #print("[Nova]"," Buscar "," Sair ")
            #elif cursorX == 1:
                #print(" Nova ","[Buscar]"," Sair ")
            #else :
                #print(" Nova "," Buscar ","[Sair]")
        #else:
            #print(" Nova "," Buscar ", " Sair")
        print("\nReceitas:\n")
        size = 3
        if cursorY == len(receitas) or cursorY == 0:
            test = size
        else:
            test = size-2
        count = 0
        for x in range(0,len(receitas)) :
            if count < size:
                if x in range(cursorY-test,cursorY+test+1):
                    count += 1
                    if x == window :
                        print("> "+receitas[x].nome)
                        if cursorX == 0:
                            print("    [Alterar]"," Deletar "," Voltar ")
                        elif  cursorX == 1:
                            print("     Alterar ","[Deletar]"," Voltar ")
                        elif cursorX ==2:
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
    elif window == "ajustar" :
        pass
    else:
        if receitas == [] :
            print("- Nenhuma receita cadastrada -\n") 
            if cursorY == len(receitas) :
                if cursorX == 0:
                    print("[Nova]"," Sair ")
                else :
                    print(" Nova ","[Sair]")
        

def alterar(receita) :
    print(receita.nome,"\n")
    for x in receita.ingredientes :
        print(x.quant,x.uni+"s" if x.quant >= 2 else x.uni,"de",x.nome)
       
def ajustar(receita):
    os.system("cls")
    alterar(receita)
    print("\nFaz:",receita.resultato,"\n")
    ajuste = input("Ajuste: ")
    valor = (float(ajuste)/float(receita.resultado))
    for x in receita.ingredientes :
        x.ajustes(valor)
    os.system("cls")
    alterar(receita)
    receita.resultado = ajuste
    print("\nFaz:",receita.resultado,"\n")
    
menu(search())

    
receitas.index 