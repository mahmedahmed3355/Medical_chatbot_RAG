# 🧠 AI Medical Chatbot – RAG Based (FastAPI + LangChain + HuggingFace + FAISS)

This project is an AI-powered **Medical Chatbot** built using **Retrieval-Augmented Generation (RAG)**, combining:

- ✅ FastAPI for the web backend  
- ✅ LangChain for LLM chaining and RAG  
- ✅ FAISS for fast semantic search  
- ✅ HuggingFace for embeddings and LLM  
- ✅ GROQ for accelerated model inference  
- ✅ Frontend with HTML/CSS + JavaScript  
- ✅ Optional voice reply using `SpeechSynthesis` API

> 💬 Ask medical questions in natural language, and get intelligent, contextual answers powered by LLMs and document search!

---

## 🚀 Features

- 🔍 Ask medical questions via a friendly chatbot UI
- 📄 RAG-enabled: context comes from your own PDF data
- ⚡ Powered by `mistralai/Mistral-7B-Instruct-v0.3` via HuggingFace or GROQ
- 🔊 Built-in text-to-speech reply
- 🧠 FAISS-based local vector store
- ☁️ Ready for deployment on Vercel or Render
- 🐳 Docker-ready setup (optional)

---

## 🏗️ Project Structure



Medical_chatbot_RAG/
│
├── app/
│ ├── application.py # FastAPI backend app
│ ├── components/ # Core logic: RAG, embeddings, retriever, etc.
│ └── templates/
│ └── index.html # Interactive frontend chatbot UI
│
├── data/ # Your own medical PDFs (converted to vector store)
├── vectorstore/db_faiss/ # FAISS vector index
├── .env # API keys and config
├── requirements.txt
├── README.md
└── ...
