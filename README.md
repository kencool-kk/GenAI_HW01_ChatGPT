# Ken's ChatGPT - GenAI HW01

這是一個基於 Streamlit 與 Groq API 開發的專屬 ChatGPT 網頁應用。

## 功能特點
1. [cite_start]**多模型切換**：支援 Llama 3.3 等多種 LLM 模型 [cite: 954]。
2. [cite_start]**人格自訂**：可自由設定 System Prompt 定義 AI 角色 [cite: 955]。
3. [cite_start]**參數調整**：支援 Temperature 與 Max Tokens 動態調整 [cite: 956]。
4. [cite_start]**串流輸出**：實作 Streaming 功能，提供流暢的對話體驗 [cite: 957]。
5. [cite_start]**短期記憶**：具備交談短期記憶功能 [cite: 958]。

## 如何執行
1. 安裝套件：`pip install -r requirements.txt`
2. 設定 `.env` 檔案並填入 `GROQ_API_KEY`。
3. 執行指令：`streamlit run HW1.py`
