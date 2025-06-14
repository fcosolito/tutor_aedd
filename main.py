from service.llm_service import LLMService
from repository.environment import Environment
from repository.mongo_user_repository import MongoUserRepository
from service.code_service import CodeService
from service.memory_service import MemoryService
from service.chunk_service import ChunkService
from model.message import Message
from model.conversation import Conversation
from model.user import User
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
env = Environment()
code_service = CodeService(env)
user_repository = MongoUserRepository(env)
memory_service = MemoryService(user_repository)
chunk_service = ChunkService()
llm_service = LLMService(env, memory_service, chunk_service)

# Create a default user for the web interface
default_user = User("web_user", [])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = llm_service.conversation_prompt(default_user, 1, user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


#message = Message("alumno", "Explicame punteros")
#conv = Conversation(1, [message])
#user = User("franco", [conv])
#memory_service.save_user(user)


#success, comp_output = code_service.compile_cpp("tmp/compilation_test.cpp")
#response = llm_service.simple_prompt(
    #comp_output,
    #"Explicame por que falla mi codigo"
#)
#print(response)