from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema de Grade Horária iniciado com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)