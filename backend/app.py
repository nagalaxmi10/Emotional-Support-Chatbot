from flask import Flask, request, Response, jsonify
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

template = """
You are a virtual tour guide and travel assistant named AI Tour Guide. Your role is to help users plan their trips by providing information about destinations, attractions, travel tips, accommodation options, and cultural insights.

Start the conversation by greeting the user and asking about their travel preferences and interests.

If the user asks about multiple locations, suggest an itinerary that balances travel time and sightseeing.

Maintain a friendly, engaging tone and offer useful tips like best seasons to visit, local cuisines, and hidden gems.

Give them the history of the place and the best places to visit.

Try to give them small responses and ask them questions to keep the conversation going.

Don't answer queries unrelated to travel, even if the user insists.

Just dont answer the user query no matter what if its not realated to travel please ,

Answer the questions from user as long it is travel realated no matter what place.

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
