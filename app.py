from flask import Flask, render_template, request, redirect , session
from database import save_result, save_student, get_results
import json
import random

app = Flask(__name__)
app.secret_key = "reading123"

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/test")
def test():

    level = request.args.get("level", "easy")
    print("Selected Level:", level)
    print(f"Opening file: dataset/{level}.json")

    with open(f"dataset/{level}.json", "r") as file:
        passages = json.load(file)

    passage = random.choice(passages)
    return render_template(
        "test.html",
        passage=passage["text"],
        level=level,
        student_name=session.get("student_name")

    )
@app.route("/login",methods=["GET", "POST"])
def login():
          if request.method =="POST":
               name = request.form["name"]
               code = request.form["code"]


               session["student_name"] = name

               return redirect("/test")
          return render_template("login.html")

@app.route("/save_result",methods=["POST"])
def save_reading_result():
     
     name = request.form["name"]
     level  =  request.form["level"]
     accuracy =  request.form["accuracy"]
     speed =  request.form["speed"]
     time_taken =  request.form["time_taken"]

     print("Before Save")

     print("Name:", name)
     print("Level:", level)
     print("Accuracy:", accuracy)
     print("Speed:", speed)
     print("Time:",time_taken )

     save_result(name, level, accuracy, speed, time_taken)

     print("Saved to  Database")

     print("After Save")

     return "Result Saved Successfully"

@app.route("/progress")
def progress():
    results = get_results(session.get("student_name"))
    return render_template("progress.html", results=results)

@app.route("/admin")
def admin():
     
     results = get_results(session.get("student_name"))
     
     return render_template(
          "admin.html",
          results=results

     )

@app.route("/learning")
def learning():
     with open("phonics/letters.json", "r") as file:
          letters = json.load(file)

          return render_template("learning.html", letters = letters)

@app.route("/letter")
def letter():
     return render_template("letter.html")

@app.route("/letter_b")
def letter_b():
     return render_template("letter_b.html")

@app.route("/letter_c")
def letter_c():
     return render_template("letter_c.html")

@app.route("/letter_d")
def letter_d():
     return render_template("letter_d.html")

@app.route("/letter_e")
def letter_e():
     return render_template("letter_e.html")

@app.route("/letter_f")
def letter_f():
     return render_template("letter_f.html")

@app.route("/letter_g")
def letter_g():
     return render_template("letter_g.html")

@app.route("/letter_h")
def letter_h():
     return render_template("letter_h.html")

@app.route("/letter_i")
def letter_i():
     return render_template("letter_i.html")

@app.route("/letter_j")
def letter_j():
     return render_template("letter_j.html")

@app.route("/letter_k")
def letter_k():
     return render_template("letter_k.html")

@app.route("/letter_l")
def letter_l():
     return render_template("letter_l.html")

@app.route("/letter_m")
def letter_m():
     return render_template("letter_m.html")

@app.route("/letter_n")
def letter_n():
     return render_template("letter_n.html")

@app.route("/letter_o")
def letter_o():
     return render_template("letter_o.html")

@app.route("/letter_p")
def letter_p():
     return render_template("letter_p.html")

@app.route("/letter_q")
def letter_q():
     return render_template("letter_q.html")

@app.route("/letter_r")
def letter_r():
     return render_template("letter_r.html")


@app.route("/letter_s")
def letter_s():
     return render_template("letter_s.html")

@app.route("/letter_t")
def letter_t():
     return render_template("letter_t.html")

@app.route("/letter_u")
def letter_u():
     return render_template("letter_u.html")

@app.route("/letter_v")
def letter_v():
     return render_template("letter_v.html")

@app.route("/letter_w")
def letter_w():
     return render_template("letter_w.html")

@app.route("/letter_x")
def letter_x():
     return render_template("letter_x.html")

@app.route("/letter_y")
def letter_y():
     return render_template("letter_y.html")

@app.route("/letter_z")
def letter_z():
     return render_template("letter_z.html")

@app.route("/blending_intro")
def blending_intro():
    return render_template("blending_intro.html")



@app.route("/blending_a")
def blending_a():
    return render_template("blending_a.html")

@app.route("/blending_e")
def blending_e():
    return render_template("blending_e.html")

@app.route("/blending_i")
def blending_i():
    return render_template("blending_i.html")

@app.route("/blending_o")
def blending_o():
    return render_template("blending_o.html")

@app.route("/blending_u")
def blending_u():
    return render_template("blending_u.html")

@app.route("/blending_bstructure")
def blending_bstructure():
    return render_template("blending_bstructure.html")

@app.route("/blending_words")
def blending_words():
    return render_template("blending_words.html")

@app.route("/blending_words2")
def blending_words2():
    return render_template("blending_words2.html")

@app.route("/sound_test")
def sound_test():
    return render_template("sound_test.html")

@app.route("/phonics")
def phonics():
    return render_template("phonics.html")



if __name__ ==  "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )
