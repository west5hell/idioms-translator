import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

from utilities import deepseek
from utilities import doubao

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
async def index():
    title = "英语习语翻译"
    heading = "英语习语翻译"
    error_code = ""

    ark_inputs_submitted = session.get("ark_inputs_submitted", False)

    if request.method == "POST":
        if not ark_inputs_submitted:
            ark_api_key = request.form.get("ark_api_key", "")
            ark_endpoint_id = request.form.get("ark_endpoint_id", "")
            print(ark_api_key, ark_endpoint_id)
            session["ark_inputs_submitted"] = True

            return redirect(url_for("index"))

        user_input = request.form.get("user_input", "")
        try:
            # output_text = await deepseek.translate_async(user_input)
            output_text = await doubao.translate_async(user_input)

            session["output_text"] = output_text
            session["user_input"] = user_input

            return redirect(url_for("index"))
        except Exception as e:
            error_code = e.code
            session["user_input"] = user_input

    output_text = session.pop("output_text", "")
    user_input = session.pop("user_input", "")

    return render_template(
        "index.html",
        title=title,
        heading=heading,
        user_input=user_input,
        output_text=output_text,
        error_code=error_code,
        ark_inputs_submitted=ark_inputs_submitted,
    )


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("ark_inputs_submitted", None)
    return redirect(url_for("index"))


# 获取并配置 API Key  https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey
# 获取并推理接入点 Endpoint ID https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
