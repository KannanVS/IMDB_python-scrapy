from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect

app = Flask(__name__)
database_file = "sqlite:///IMDBMovies.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app);


class Data(db.Model):

    movie_name = db.Column(db.String(80), nullable=False, unique=True, primary_key=True)
    votes = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Name: {}>".format(self.movie_name)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        movies = Data.query.limit(50).all()
    except:
        print("Error in reading the Names!")
    return render_template("home.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    try:
        if request.form:
            data = Data(movie_name=request.form.get("addname"), votes=85, year=2020, rating=5)
            db.session.add(data)
            db.session.commit()
    except:
        print("Error in adding the Name!")
    return redirect("/")


@app.route("/delete/<movies>", methods=["GET", "POST"])
def delete(movies):
    try:
        movies = Data.query.filter_by(movie_name=movies).first()
        db.session.delete(movies)
        db.session.commit()
    except:
        print("Error in deleting the Name!")
    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.form:
        newname = request.form.get("newtitle")
        oldname = request.form.get("oldtitle")
        movies = Data.query.filter_by(movie_name=oldname).first()
        movies.movie_name = newname
        db.session.commit()
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    try:
        if request.form:
            searchname = request.form.get("searchname")
            movies = Data.query.filter_by(movie_name=searchname).limit(50).all()
    except:
        print("Error in searching the Name!")
    return render_template("home.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)