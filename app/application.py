import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, Response, g, redirect, render_template, request, session, url_for
from markupsafe import Markup
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import ValidationError

from app.common.structured_logger import logger
from app.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY
from app.schemas.prompt import PromptRequest

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


@app.before_request
def start_request_observability():
    """Create a request identifier and start request timing."""
    g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    g.request_start_time = time.perf_counter()


@app.after_request
def record_request_observability(response):
    """Record request metrics and attach the request identifier."""
    endpoint = request.endpoint or "unknown"
    start_time = getattr(g, "request_start_time", None)

    if start_time is not None:
        duration = time.perf_counter() - start_time

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code,
    ).inc()

    response.headers["X-Request-ID"] = g.request_id

    logger.info(
        "http_request_completed",
        extra={"request_id": g.request_id},
    )

    return response


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        raw_prompt = request.form.get("prompt", "")

        try:
            prompt_request = PromptRequest(prompt=raw_prompt)
            user_input = prompt_request.prompt
        except ValidationError as exc:
            return render_template(
                "index.html",
                messages=session.get("messages", []),
                error=exc.errors()[0]["msg"],
            ), 400

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
