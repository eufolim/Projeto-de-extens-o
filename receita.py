import os
ingredientes = []
class ingrediente:
    def __init__(self,uni,valor,nome) -> None:
        self.uni = uni
        self.valor = float(valor)
        self.nome = nome
        
    def ajustes(self,valor):
        self.valor = self.valor*float(valor)

def incluir():
    obj = input("Ingrediente: ") 
    obj = ingrediente(input("Unidade: "),input("Quantidade: "),obj)
    return obj
    
def menu(ingredientes):
    os.system("cls")
    ingredientes.append(incluir())
    if input("Comtinuar?(s/n): ") == "s" :
        menu(ingredientes)
    else:
        os.system("cls")
        total = {"Total":input("Total: "),"Unidade":input("Unidade: ")}
        ajustar(ingredientes,total)

def display(ingredientes):
    for x in ingredientes :
        print(x.valor,x.uni+"s" if x.valor >= 2 else x.uni,"de",x.nome)
        
def ajustar(ingredientes,total):
    os.system("cls")
    display(ingredientes)
    print("\nFaz:",total["Total"],total["Unidade"],"\n")
    ajuste = input("Ajuste: ")
    valor = (float(ajuste)/float(total["Total"]))
    for x in ingredientes :
        x.ajustes(valor)
    os.system("cls")
    display(ingredientes)
    total["Total"] = ajuste
    print("\nFaz:",total["Total"],total["Unidade"],"\n")
    
   
menu(ingredientes)
    
