from flask import Flask, request, render_template, redirect, url_for
import os
import json
import pickle as pk
from PIL import Image as pil

class receita:
    def __init__(self,nome,ingredientes,total,unidade,imagen=None) -> None:
        self.nome = nome
        self.ingredientes = ingredientes
        self.total = float(total)
        self.unidade = unidade
        self.imagen = imagen
        
    def ajustes(self,valor):
        ajuste = float(valor)/float(self.total)
        for x in self.ingredientes :
            x.ajustes(ajuste)
        self.total = float(valor)

class ingrediente:
    def __init__(self,nome,valor,unidade) -> None:
        self.nome = nome
        self.valor = float(valor)
        self.unidade = unidade

    def ajustes(self,valor):
        self.valor = self.valor*valor


# Diretório para salvar os arquivos 
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)

# Rotas do flask ↓

# Menu principal
@app.route("/", defaults={"search":""})
@app.route("/<search>", methods=['GET'])
def hello(search = ""):
    recipes = []
    searched = request.args.get('search')
    for file in os.listdir(DATA_DIR):
        temp = pk.load(open(DATA_DIR+"/"+file,"rb"))
        nome = temp.nome
        if isinstance(searched,str) :
            if nome.find(searched) >= 0 : 
                recipes.append(temp)
        else: 
            recipes.append(temp)  
    return render_template("menu.html", recipes=recipes, searched=searched)

# Tela de cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

# Tela de ajuste
@app.route("/adjust_recipe/<recipe_name>", methods=['GET', 'POST'])
def adjust_recipe(recipe_name):

    recipe = pk.load(open(DATA_DIR+"/"+recipe_name,"rb"))
    
    if request.method == 'POST':
        new_total = float(request.form.get("new_total"))
        recipe.ajustes(new_total)
        
    return render_template("adjust_recipe.html", recipe=recipe)

# Salvar receita
@app.route("/save_recipe", methods=['POST'])
def save_recipe():
    ingredientes = []
    temp = []
    recipe_name = request.form.get('recipe_name')
    for key, value in request.form.items():
        if key.startswith('ingredient-') or key.startswith('quantity-') or key.startswith('unidade-'):
            temp.append(value)
            if len(temp) > 2 :
                ingredientes.append(ingrediente(temp[0],float(temp[1]),temp[2]))
                temp = []
    recipe_total = request.form.get('recipe_total') 
    recipe_unit = request.form.get('recipe_unit') 
    
    # Salvar imagen em pasta
    recipe_image = request.files.get('recipe_image')
    recipe_path = "static/image/"+recipe_name+".jpeg"
    image = pil.open(recipe_image)
    image.save("./"+recipe_path,"JPEG")
    
    # Salvar receita em um arquivo 
    recipe = receita(recipe_name,ingredientes,recipe_total,recipe_unit,recipe_path)
    pk.dump(recipe,open(DATA_DIR+"/"+recipe.nome,"wb"))
    return redirect(url_for('cadastro'))

if __name__ == "__main__":
    app.run(debug=True)