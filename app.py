import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

from utilities import deepseek
from utilities import doubao

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# @app.route("/", methods=["GET", "POST"])
# def index():
#     title = "英语习语翻译"
#     heading = "英语习语翻译"
#     user_input = ""
#     output_text = ""

#     if request.method == "POST":
#         user_input = request.form.get("user_input", "")
#         output_text = deepseek.translate(user_input)

#     return render_template(
#         "index.html",
#         title=title,
#         heading=heading,
#         user_input=user_input,
#         output_text=output_text,
#     )


@app.route("/", methods=["GET", "POST"])
async def index():
    title = "英语习语翻译"
    heading = "英语习语翻译"
    # user_input = ""
    # output_text = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        # output_text = await deepseek.translate_async(user_input)
        output_text = await doubao.translate_async(user_input)

        session["output_text"] = output_text
        session["user_input"] = user_input

        return redirect(url_for("index"))

    output_text = session.pop("output_text", "")
    user_input = session.pop("user_input", "")

    return render_template(
        "index.html",
        title=title,
        heading=heading,
        user_input=user_input,
        output_text=output_text,
    )
