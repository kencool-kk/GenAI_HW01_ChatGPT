## Ken GenAI HW2

# 離開 deactivate
## streamlit run HW2.py

import streamlit as st
import os
import base64
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# --- 【步驟 1：初始化】 ---
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 【核心功能 1：長期記憶 (LTM) - 模組匯入】
import memory_db as mem 

# 網頁基本設定
st.set_page_config(page_title="Ken's AI Lab", layout="wide")
st.title("🤖 Ken's GenAI 應用開發 HW2")

# --- 輔助函式區域 ---

# --- 【步驟 2：邏輯定義】 ---
# 【核心功能 2：多模態 (Multimodal) - 圖片編碼處理】
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 【核心功能 3：自動路由 (Auto Routing) - 模型選擇邏輯】
def auto_route_model(user_prompt, has_image=False):
    if has_image:
        return "llama-3.2-11b-vision-preview" # 偵測圖片自動轉視覺模型
    if len(user_prompt) > 300:
        return "llama-3.3-70b-versatile"      # 長文自動轉強大模型
    return "llama3-8b-8192"                   # 一般對話用輕量模型

# 【核心功能 4：工具使用 (Tool Use) - 外部環境資訊獲取】
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- 【步驟 3：UI 設定】 ---
with st.sidebar:
    st.header("⚙️ 控制面板")
    
    # [功能 3: 模型與路由切換]
    use_auto_routing = st.toggle("啟動自動路由", value=True)
    if not use_auto_routing:
        model_option = st.selectbox("手動指定模型", ["llama3-8b-8192", "mixtral-8x7b-32768"])
    
    st.markdown("---")
    # 【核心功能 2：多模態 - 檔案上傳 UI】
    uploaded_file = st.file_uploader("🖼️ 上傳圖片內容", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    # 【核心功能 1：長期記憶 - 記憶存儲 UI】
    st.header("💾 長期記憶庫管理")
    f_key = st.text_input("事實標題")
    f_val = st.text_input("事實內容")
    if st.button("📌 存入長期記憶"):
        mem.save_memory({f_key: f_val})
        st.success("記憶已寫入資料庫！")

# --- 【步驟 4：對話狀態管理】 ---
# 【核心功能 5：短期交談記憶 - Session 初始化】
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 【步驟 5：處理輸入與推理】 ---
if prompt := st.chat_input("說點什麼..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 【核心功能 3：執行自動路由】
    current_model = auto_route_model(prompt, (uploaded_file is not None)) if use_auto_routing else model_option

    # 【核心功能 1 & 4：Context 整合 (LTM + Tool Use)】
    ltm_data = mem.get_memory_string() # 抓取長期記憶
    env_time = get_current_time()      # 抓取工具資訊
    
    full_system_instruction = f"人格設定：助手。\n時間工具：{env_time}\n長期記憶：{ltm_data}"

    # 【核心功能 2 & 5：建構多模態與上下文 Payload】
    api_messages = [{"role": "system", "content": full_system_instruction}]
    for m in st.session_state.messages[:-1]: # 注入歷史訊息 (短期記憶)
        api_messages.append({"role": m["role"], "content": m["content"]})
    
    if uploaded_file: # 處理多模態訊息格式
        img_b64 = encode_image(uploaded_file)
        api_messages.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}]
        })
    else:
        api_messages.append({"role": "user", "content": prompt})

    # 【核心功能 6：串流輸出 (Streaming)】
    with st.chat_message("assistant"):
        response_box = st.empty()
        ai_response = ""
        
        # 呼叫 API 並啟動 stream=True
        stream = client.chat.completions.create(model=current_model, messages=api_messages, stream=True)
        
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                ai_response += token
                response_box.markdown(ai_response + "▌") # 實作打字機效果
        
        response_box.markdown(ai_response)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})