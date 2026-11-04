import streamlit as st
import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)
st.title("DeepSeek test")
st.header("DeepSeek test-h1")
st.subheader("DeepSeek test-h2")
st.write("""1. **VSCode / Pycharm 里面读不到**
终端里面 source 生效了，但 IDE 打不开：IDE 是图形程序，不继承终端 zshrc。
  - 方案 A：先从终端里打开 `code .` 启动 vscode，就能读到
  - 方案 B（全局给图形 APP，麻烦一点，一般开发不用）
2. 引号：key 里面没有空格，单引号双引号都可以；不要多加空格""")
st.image('resource/logo.JPG')
st.table({"姓名": ["1","2","3,4,2,3,4,2,3,4,2,3,4"],
           "年龄": ['12', 19,10,2,3,4,2,3,4],
           "年龄2": ['12', 19,10,2,3,4,2,3,4]
}
)
