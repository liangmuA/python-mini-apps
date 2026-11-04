# 本文件运行方式：直接右键运行
import logging
from datetime import datetime
import os.path
from fastapi import FastAPI
import json
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO, # 设置日志最低级别为INFO，记录所有INFO及以上级别的日志，灵活控制
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

app = FastAPI()

# 挂载静态文件目录，用于提供前端静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 系统提示词 - 适配DeepSeek V4
SYSTEM_PROMPT = """
你是一个专门玩猜字谜的AI小助手，只进行字谜互动，不闲聊无关内容，全程纯文本交互。
请严格遵守以下规则：

一、出题规则
1. 开场先友好打招呼，并随机出一道常见、简单、适合大众的字谜，不生僻、不低俗、不使用网络烂梗。
2. 题目格式：“谜面”（打一字）。
3. 每次出题必须完全随机，禁止重复使用相同题目；你需要在对话上下文中主动记录已使用过的谜语，确保同一会话内绝对不重复。
4. 避免使用高频重复的经典老谜语，尽量选择多样化的中等常见谜语。

二、【判题规则（最重要！）】
1. 判题时，只看用户输入中的核心汉字，忽略无关内容：
- 比如用户输入“江字”“江”“jiang”，都视为答案是「江」；
- 用户输入“是江吗？”“应该是江”，也视为答案是「江」。
2. 核心字与正确答案完全一致 → 判为正确，回复：“太棒了！答对了！就是‘XX’字！要不要再来一题？”
3. 核心字与正确答案不一致 → 判为错误，回复：“不对哦，再想想~ 给你个小提示：[简短线索，不泄露答案]”
4. 用户说“不知道”“公布答案”：先揭晓谜底和解释，再问“要不要再来一题？”

三、互动流程
1. 用户答对：夸奖 + 确认正确 + 询问“要不要再来一题？”
2. 用户答错：告知不对 + 简单提示 + 鼓励继续猜
3. 用户说“提示一下”：给出简短线索，不公布答案

四、其他要求
1. 语气轻松有趣、简洁明快，不啰嗦。
2. 全程只围绕字谜，不回答其他问题、不聊无关话题。
3. 不使用多余表情符号，保持简洁。
4. 若用户答案与正确答案仅差一字或笔画，请仔细核对是否正确。

请严格按以上规则回复，优先保证谜语的随机性和多样性。
"""


@app.get("/")
def root():
    logging.info("访问首页")
    return FileResponse("static/index.html") # 返回首页，使用starlette库的FileResponse

# 存储会话数据的目录
if not os.path.exists("sessions"):
    os.makedirs("sessions")

# 获取会话id
def generate_session_id():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_session_file(session_id):
    return f"sessions/{session_id}.json"

# 定义返回数据模型
class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any

# 定义请求数据模型
class ChatRequest(BaseModel):
    session_id: str
    message: str

# 创建对话
@app.post("/api/sessions")
def create_session() -> ApiResponse:
    logging.info("创建对话")
    session_id = generate_session_id()

    session_data = {
        "current_session": session_id,
        "messages": []
    }

    with open(f"sessions/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    return ApiResponse(code=200, message="创建对话成功", data=session_id)

# 获取会话列表
@app.get("/api/sessions")
def get_sessions() -> ApiResponse:
    logging.info("获取会话列表")
    sessions = os.listdir("sessions")
    sessions = [session for session in sessions if session.endswith(".json")]
    sessions = [session.replace(".json", "") for session in sessions]
    sessions.sort(reverse=True)
    return ApiResponse(code=200, message="获取会话列表成功", data=sessions)

# 获取指定会话
@app.get("/api/sessions/{session_id}") # 路径参数用{}通配
def get_session(session_id: str) -> ApiResponse:
    logging.info("获取指定会话")
    session_file = get_session_file(session_id)
    with open(session_file, "r", encoding="utf-8") as f:
        session_data = json.load(f)
    return ApiResponse(code=200, message="获取会话成功", data=session_data)

# 删除指定会话
@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str) -> ApiResponse:
    logging.info("删除指定会话")
    session_file = get_session_file(session_id)
    if not os.path.exists(session_file):
        return ApiResponse(code=404, message="会话不存在", data=None)
    os.remove(session_file)
    return ApiResponse(code=200, message="删除会话成功", data=None)

# 创建与大模型交互的客户端对象
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

# 与ai交互
@app.post("/api/chat")
def chat(request: ChatRequest) -> ApiResponse:
    # 与AI大模型交互
    # 1.加载json中的会话数据
    session_file = get_session_file(request.session_id)
    with open(session_file, "r", encoding="utf-8") as f:
        session_data = json.load(f)

    # 2.构建与大模型交互的消息数据
    messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT
    }]
    for msg in session_data["messages"]:
        messages.append(msg)
    messages.append({
        "role": "user",
        "content": request.message
    })

    # 3.调用deepseek大模型
    # 调用ai大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False,
        temperature=1.5 # 温度参数，控制生成文本的随机性
    )

    # 4.获取模型响应数据
    ai_response = response.choices[0].message.content
    logging.info(f"获取模型响应数据{ai_response}")

    # 5.更新消息队列
    messages.pop(0) # 滚雪球时，不需要连带系统提示词
    messages.append({
        "role": "assistant",
        "content": ai_response
    })
    session_data["messages"] = messages
    # 6.保存到json中
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    # 7.返回结果
    return ApiResponse(code=200, message="与ai交互成功", data=ai_response)

@app.exception_handler(Exception)
def handle_exception(request: Request, exc: Exception):
    logging.error(f"捕获到 {request.url} 的异常，请求路径：{request.url}")
    return JSONResponse(content={"code": 500, "message": "服务器错误，请稍后再试", "data": None})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
