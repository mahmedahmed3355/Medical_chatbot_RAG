import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import Markup

load_dotenv()

app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")
if secret_key:
    app.config["SECRET_KEY"] = secret_key
else:
    app.config["SECRET_KEY"] = os.urandom(32)


def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))


app.jinja_env.filters["nl2br"] = nl2br


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt", "").strip()

        if user_input:
            messages = session["messages"]
            messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )
            session["messages"] = messages

            try:
                from app.components.retriever import create_qa_chain

                qa_chain = create_qa_chain()

                response = qa_chain.invoke(
                    {
                        "query": user_input,
                    }
                )

                result = response.get(
                    "result",
                    "No response",
                )

                messages.append(
                    {
                        "role": "assistant",
                        "content": result,
                    }
                )

                session["messages"] = messages

            except Exception as exc:
                error_msg = f"Error: {exc}"

                return render_template(
                    "index.html",
                    messages=session["messages"],
                    error=error_msg,
                ), 500

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        messages=session.get("messages", []),
    )


@app.get("/clear")
def clear():
    session.pop("messages", None)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
    )
