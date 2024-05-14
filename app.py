from flask import Flask, request, render_template, redirect, url_for
import os
import json

app = Flask(__name__)

# Diretório para salvar os arquivos JSON
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/")
def hello():
    recipes = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                recipe = json.load(f)
                recipes.append(recipe)
    return render_template("menu.html", recipes=recipes)

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/ajuste")
def ajuste():
    recipes = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                recipe = json.load(f)
                recipe['id'] = filename.split('.')[0]  # Usar o nome do arquivo como ID
                recipes.append(recipe)
    return render_template("ajuste.html", recipes=recipes)

@app.route("/adjust_recipe/<recipe_id>", methods=['GET', 'POST'])
def adjust_recipe(recipe_id):
    recipe_path = os.path.join(DATA_DIR, f"{recipe_id}.json")
    if not os.path.exists(recipe_path):
        return "Recipe not found", 404

    with open(recipe_path, 'r') as f:
        recipe = json.load(f)

    if request.method == 'POST':
        new_total = float(request.form.get('new_total'))
        old_total = sum(float(value) for key, value in recipe.items() if key.startswith('quantity-'))
        adjustment_ratio = new_total / old_total

        for key in recipe:
            if key.startswith('quantity-'):
                recipe[key] = round(float(recipe[key]) * adjustment_ratio, 3)  # Arredondar para 3 casas decimais

        with open(recipe_path, 'w') as f:
            json.dump(recipe, f)

        return redirect(url_for('hello'))

    return render_template("adjust_recipe.html", recipe=recipe, recipe_id=recipe_id)

@app.route("/save_recipe", methods=['POST'])
def save_recipe():
    recipe = {}
    recipe_name = request.form.get('recipe_name')
    recipe['name'] = recipe_name

    for key, value in request.form.items():
        if key.startswith('ingredient-') or key.startswith('quantity-'):
            recipe[key] = value
            
    # Salvar receita em um arquivo JSON
    recipe_id = len(os.listdir(DATA_DIR)) + 1
    with open(os.path.join(DATA_DIR, f'recipe_{recipe_id}.json'), 'w') as f:
        json.dump(recipe, f)
    return redirect(url_for('cadastro'))

if __name__ == "__main__":
    app.run(debug=True)
