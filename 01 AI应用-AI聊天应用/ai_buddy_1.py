# 本文件运行方式：控制台输入：streamlit run ai_buddy_1.py
import datetime
import json
import streamlit as st
import os
from openai import OpenAI
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="AI智能搭子",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)
st.title("AI智能搭子")
st.logo("resource/logo.gif")

# 系统提示词
system_prompt = """ 你叫 %s，是用户的学习搭子，请完全代入角色。
规则：
1. 每次只回1条消息
2. 禁止任何场景或状态描述性文字
3. 匹配用户的语言
4. 回复简短，像微信聊天一样
5. 有需要的话可以用🖤✨等emoji表情
6. 用符合搭子性格的方式对话
7. 回复的内容，要充分体现搭子的性格特征
搭子性格：
- %s。"""

# 用户提示词
prompt = st.chat_input("请输出你的问题")


# 生成会话名称
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 消息管理
if 'messages' not in st.session_state:
    st.session_state.messages = []
# ai角色管理
if 'ai_role' not in st.session_state:
    st.session_state.ai_role = {"name": '知予', "nature": '聪明温柔耐心，善于分析和讲解问题的学习搭子'}
# 会话管理
if 'current_session' not in st.session_state:
    st.session_state.current_session = generate_session_name()

# 保存会话功能
def save_session():
    if not st.session_state.messages:
        return

    dict1 = {
        "messages": st.session_state.messages,
        "ai_role": st.session_state.ai_role,
        "session_id": st.session_state.current_session
    }
    if not os.path.exists("session"):
        os.makedirs("session")
    with open(f"session/{st.session_state.current_session}.json", "w") as f:
        json.dump(dict1, f, ensure_ascii=False, indent=2)

# 加载会话列表
def load_session_list():
    session_list = []
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for file in file_list:
            if file.endswith(".json"):
                session_list.append(file[:-5])
    session_list.sort(reverse=True) # 返回None
    return session_list

# 加载指定会话
def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            with open(f"session/{session_name}.json", "r") as f:
                dict1 = json.load(f)
            st.session_state.messages = dict1["messages"]
            st.session_state.ai_role = dict1["ai_role"]
            st.session_state.current_session = dict1["session_id"]
            st.rerun()
    except Exception as error:
        st.error("加载会话失败！")

# 删除会话
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            if st.session_state.current_session == session_name:
                st.session_state.current_session = generate_session_name()
                st.session_state.messages = []
        st.rerun()
    except Exception:
        st.error("删除会话失败！")

# 左侧-侧边栏
with st.sidebar:
    # 会话管理
    st.subheader("会话管理")
    if st.button("新建会话", width='stretch', icon="🖌️"):
        """
        被点击就会返回true
        Streamlit 每次交互都会从头到尾重新执行整个脚本
        """

        # 保存当前会话
        save_session()
        # 新建会话
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        save_session()
        st.rerun()
    # 展示历史会话
    st.text('历史会话')
    session_list = load_session_list()
    for session in session_list:
        co1, col2 = st.columns([4, 1])
        with co1:
            if st.button(session, width='stretch', icon="📁", key=f"load_{session}", type="primary" if st.session_state.current_session == session else "secondary"):
                load_session(session)
        with col2:
            if st.button("", width='stretch', icon="❌️", key=session):
                delete_session(session)
    st.divider()
    # 角色管理
    st.subheader("AI角色配置")
    name = st.text_input("昵称", value=st.session_state.ai_role["name"], placeholder="请输入AI角色名称")
    if name:
        st.session_state.ai_role['name'] = name
    nature = st.text_area("性格", value=st.session_state.ai_role["nature"], placeholder="请输入AI角色性格")
    if nature:
        st.session_state.ai_role['nature'] = nature

# 展示历史信息
def show_history():
    for message in st.session_state.messages:
        if "role" in message:
            st.chat_message(message["role"]).write(message["content"])
st.text(f"当前会话: {st.session_state.current_session}")
show_history()

# 创建与大模型交互的客户端对象
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

if prompt:
    st.chat_message('user').write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用ai大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.ai_role['name'], st.session_state.ai_role['nature'])},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )

    # 输出大模型结果-非流式输出
    # st.chat_message('assistant').write(response.choices[0].message.content)
    # print(response.choices[0].message.content)

    # 输出大模型结果-流式输出
    response_message = st.empty()
    response_content = ''
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            response_content += chunk.choices[0].delta.content
            response_message.chat_message('assistant').write(response_content)

    # 保存大模型结果
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    save_session()
