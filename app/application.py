import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.components.retriever import create_qa_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
# لو هتتعامل مع React أو صفحة تانية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # أو ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware for storing chat messages
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))

# Static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Home route - renders index.html
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    messages = request.session.get("messages", [])
    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})


# POST route from form submission (index.html)
@app.post("/", response_class=HTMLResponse)
async def post_index(request: Request, prompt: str = Form(...)):
    messages = request.session.get("messages", [])
    messages.append({"role": "user", "content": prompt})

    try:
        qa_chain = create_qa_chain()
        if qa_chain is None:
            raise Exception("QA chain could not be created (LLM or VectorStore issue)")
        response = qa_chain.invoke({"query": prompt})
        result = response.get("result", "No response")
        messages.append({"role": "assistant", "content": result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "messages": messages,
            "error": f"Error: {str(e)}"
        })

    request.session["messages"] = messages
    return RedirectResponse(url="/", status_code=303)


# API route for JS-based chat in index.html (Fetch API)
@app.post("/api/chat")
async def api_chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    messages = request.session.get("messages", [])
    messages.append({"role": "user", "content": prompt})

    try:
        qa_chain = create_qa_chain()
        if qa_chain is None:
            raise Exception("QA chain could not be created (LLM or VectorStore issue)")
        response = qa_chain.invoke({"query": prompt})
        result = response.get("result", "No response")
        messages.append({"role": "assistant", "content": result})
    except Exception as e:
        result = f"⚠️ Error: {str(e)}"

    request.session["messages"] = messages
    return JSONResponse({"response": result})


# Clear chat history
@app.get("/clear")
async def clear_chat(request: Request):
    request.session.pop("messages", None)
    return RedirectResponse(url="/", status_code=303)
