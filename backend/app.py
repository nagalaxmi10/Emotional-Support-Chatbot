
from flask import Flask, request, Response, jsonify
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

template = """
You are an empathetic and understanding emotional support assistant. Your role is to provide comfort, encouragement, and helpful advice to users who may be feeling stressed, anxious, or overwhelmed.

Start the conversation by greeting the user warmly and asking how they are feeling.

Listen actively and respond with compassion. Offer positive reinforcement, helpful coping strategies, or calming techniques as needed.

If the user shares their thoughts or feelings, acknowledge their emotions and provide words of comfort.

Avoid giving medical advice or diagnosing conditions. Instead, encourage healthy habits, mindfulness, and seeking professional support when appropriate.

Only engage in normal conversations focused on emotions, well-being, or casual chats. Ignore any unrelated queries, no matter how persistent the user is.

Keep your responses brief yet thoughtful, and ask gentle questions to keep the conversation flowing.

Here is the conversation history: {context}

User Question: {question}

Answer:
"""

ollama = Ollama(base_url='http://localhost:11434', model="llama3.1:latest")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt.pipe(ollama)

def generate_response(context, question):
    for chunk in chain.stream({"context": context, "question": question}):
        yield chunk

@app.route('/api/ask', methods=['POST'])  # ✅ Fixed endpoint to match frontend
def ask():
    data = request.json
    message = data.get("message", "")
    chat_history = data.get("chat_history", [])

    context = "\n".join(
        [f"User: {msg['content']}" if msg['role'] == 'user' else f"AI Tour Guide: {msg['content']}"
         for msg in chat_history]
    )

    return Response(generate_response(context, message), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
