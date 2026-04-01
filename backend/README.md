⚙️ Backend – FastAPI

🚀 Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

▶️ Run Server
uvicorn app.main:app --reload --port 8001

🔐 Environment Variables (.env)
SECRET_KEY=your_secret_key
ALGORITHM=HS256
GEMINI_API_KEY=your_api_key

📌 API Docs

http://127.0.0.1:8001/docs

🧠 Features
JWT Authentication
Role-based access control
Multi-tenant architecture
Issue management APIs
AI Chatbot integration
AI Study Planner