from flask import Blueprint, request, jsonify
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Blueprint 객체 생성
chatbot_bp = Blueprint('chatbot', __name__)

# 환경변수 설정
openai_api_key = os.environ.get('OPENAI_API_KEY')

db = SQLDatabase.from_uri("sqlite:///test_database.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=4000)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    # 입력된 메시지 처리
    if user_input:
        # LangChain Agent를 사용하여 응답 생성
        output = agent_executor.invoke(str(user_input) + ", answer in korean")
        result = output['output']
        
        # 답변 추출 및 반환
        final_result = result.split("Invoking:")[0].strip()
        return jsonify({'response': final_result})
    else:
        # 입력이 없는 경우의 처리
        return jsonify({'response': 'No input provided'}), 400