from flask import Flask, render_template, request, redirect, url_for
import db

# Inicio servidor Flask
app = Flask(__name__)

@app.route('/')
def home():
    print("Iniciamos con una prueba")
    return render_template("index.html")

if __name__ == '__main__':
    db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)

    db.Base.metadata.create_all(db.engine)

    app.run(debug=True)


