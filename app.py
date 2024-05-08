from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("menu.html")

@app.route("/cadastro")  
def cadastro():
    return render_template("cadastro.html")  

@app.route("/ajuste")  
def ajuste():
    return render_template("ajuste.html")  

if __name__ == "__main__":
    app.run(debug=True)
