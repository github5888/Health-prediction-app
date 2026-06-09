from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
import re
from datetime import date
from database import setup_db, get_all, get_one, add_patient, update_patient, delete_patient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "mira123"

# create the table when app starts
setup_db()


def get_ai_remark(glucose, haemoglobin, cholesterol):
    # call groq api to get health prediction based on blood values
    try:
        api_key = os.getenv("GROQ_API_KEY")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "groq/compound",
            "max_tokens": 200,
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a health assistant. Look at these blood test results and give a short health remark (2-3 sentences only). Mention if any value is abnormal and what condition it might indicate.\n\nGlucose: {glucose} mg/dL\nHaemoglobin: {haemoglobin} g/dL\nCholesterol: {cholesterol} mg/dL\n\nGive a simple, clear remark for a patient health record."
                }
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body
        )

        result = response.json()
        remark = result["choices"][0]["message"]["content"]
        return remark

    except Exception as e:
        return "Could not generate AI remark. Please try again."


def check_form(form):
    errors = []

    name = form.get("full_name", "").strip()
    if not name:
        errors.append("Full name is required.")

    dob = form.get("dob", "")
    if not dob:
        errors.append("Date of birth is required.")
    else:
        try:
            dob_parsed = date.fromisoformat(dob)
            if dob_parsed >= date.today():
                errors.append("Date of birth must be in the past.")
        except:
            errors.append("Date of birth format is invalid.")

    email = form.get("email", "")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Please enter a valid email address.")

    for field in ["glucose", "haemoglobin", "cholesterol"]:
        val = form.get(field, "")
        try:
            float(val)
        except:
            errors.append(f"{field.capitalize()} must be a number.")

    return errors


@app.route("/")
def home():
    patients = get_all()
    return render_template("index.html", patients=patients)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        errors = check_form(request.form)

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("form.html", title="Add Patient", action="/add", data=request.form)

        # get values from form
        name       = request.form["full_name"].strip()
        dob        = request.form["dob"]
        email      = request.form["email"].strip()
        glucose    = float(request.form["glucose"])
        haemoglobin = float(request.form["haemoglobin"])
        cholesterol = float(request.form["cholesterol"])

        # get ai remark
        remark = get_ai_remark(glucose, haemoglobin, cholesterol)

        add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remark)
        flash("Patient added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("form.html", title="Add Patient", action="/add", data={})


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    patient = get_one(id)

    if not patient:
        flash("Patient not found.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        errors = check_form(request.form)

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("form.html", title="Edit Patient", action=f"/edit/{id}", data=request.form)

        name        = request.form["full_name"].strip()
        dob         = request.form["dob"]
        email       = request.form["email"].strip()
        glucose     = float(request.form["glucose"])
        haemoglobin = float(request.form["haemoglobin"])
        cholesterol = float(request.form["cholesterol"])

        # regenerate ai remark after edit
        remark = get_ai_remark(glucose, haemoglobin, cholesterol)

        update_patient(id, name, dob, email, glucose, haemoglobin, cholesterol, remark)
        flash("Patient updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("form.html", title="Edit Patient", action=f"/edit/{id}", data=patient)


@app.route("/view/<int:id>")
def view(id):
    patient = get_one(id)
    if not patient:
        flash("Patient not found.", "danger")
        return redirect(url_for("home"))
    return render_template("view.html", p=patient)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    delete_patient(id)
    flash("Patient record deleted.", "warning")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
