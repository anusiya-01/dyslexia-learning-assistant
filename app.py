import json
import os
import random
import tempfile
from database import get_results, save_result, save_student, verify_student, update_password, login_or_register
from flask import Flask, redirect, render_template, request, session
import librosa
import numpy as np

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

  try:
    with open(f"dataset/{level}.json", "r") as file:
      passages = json.load(file)
    passage = random.choice(passages)["text"]
  except Exception as e:
    passage = "This is a sample passage for reading assessment test."

  return render_template(
      "test.html",
      passage=passage,
      level=level,
      student_name=session.get("student_name", "Student"),
  )


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    name = request.form["name"]
    code = request.form["code"]

    if not login_or_register(name, code):
      return render_template("login.html", error="Incorrect password", name=name)

    session["student_name"] = name
    return redirect("/test")
  return render_template("login.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
  if request.method == "POST":
    name = request.form["name"]
    new_code = request.form["new_code"]
    if not update_password(name, new_code):
      return render_template("forgot_password.html", name=name, error="Name not found")
      
    session["student_name"] = name
    return redirect("/test")
  return render_template("forgot_password.html", name=request.args.get("name", ""))

@app.route("/save_result", methods=["POST"])
def save_reading_result():
  name = request.form.get("name")
  level = request.form.get("level")
  accuracy = request.form.get("accuracy")
  speed = request.form.get("speed")
  time_taken = request.form.get("time_taken")
  grade = request.form.get("grade")

  print("Before Save")
  print("Name:", name)
  print("Level:", level)
  print("Accuracy:", accuracy)
  print("Speed:", speed)
  print("Time:", time_taken)
  print("Grade:", grade)

  save_result(name, level, accuracy, speed, time_taken, grade)

  print("Saved to Database")
  return "Result Saved Successfully"



@app.route("/progress", methods=["GET", "POST"])
def progress():
  if request.method == "POST":
    name = request.form["name"]
    code = request.form["code"]

    if not verify_student(name, code):
      return render_template("progress_login.html", error="Incorrect password", name=name)

    results = get_results(name)
    return render_template("progress.html", results=results, student_name=name)

  return render_template("progress_login.html")


@app.route("/admin")
def admin():
  results = get_results(session.get("student_name", ""))
  return render_template("admin.html", results=results)


@app.route("/learning")
def learning():
  try:
    with open("phonics/letters.json", "r") as file:
      letters = json.load(file)
  except Exception as e:
    letters = []
  return render_template("learning.html", letters=letters)


# Letter Routes
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


@app.route("/compare_voice", methods=["POST"])
def compare_voice():
  user_file = None
  try:
    if "audio" not in request.files:
      return {"error": "No audio file uploaded"}, 400

    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
      audio_file.save(temp.name)
      user_file = temp.name

    reference_file = os.path.join(
        app.static_folder, "sounds", "a_sound.mp3"
    )

    if not os.path.exists(reference_file):
      return {"error": "Reference sound file not found"}, 404

    reference, sr1 = librosa.load(reference_file, sr=16000, mono=True)
    user_voice, sr2 = librosa.load(user_file, sr=16000, mono=True)

    reference_mfcc = librosa.feature.mfcc(y=reference, sr=sr1, n_mfcc=13)
    user_mfcc = librosa.feature.mfcc(y=user_voice, sr=sr2, n_mfcc=13)

    D, wp = librosa.sequence.dtw(
        X=reference_mfcc, Y=user_mfcc, metric="euclidean"
    )

    distance = D[-1, -1] / len(wp)

    score = 100 * np.exp(-distance / 30)
    score = int(max(0, min(100, score)))

    return {"score": score}

  except Exception as e:
    print("Voice comparison error:", e)
    return {"error": str(e)}, 500

  finally:
    if user_file and os.path.exists(user_file):
      os.remove(user_file)


# Blending & Sound Routes
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


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
