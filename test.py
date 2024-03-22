import pickle as pk

class testClass:
    
    def __init__(self,nome,testValue) -> None:
        self.testValue = testValue
        self.nome = nome
        
novo = testClass("test3",9)
file = open("./saves/"+novo.nome,"wb")
pk.dump(novo,file)