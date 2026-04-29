# Ken's ChatGPT - GenAI HW01 & HW02

這是一個基於 Streamlit 與 Groq API 開發的進階 AI 助理應用。本專案從基礎的對話機器人（HW01）演進為具備環境感知、跨對話記憶與多模態分析能力的 AI 工作站（HW02）。

## 核心功能亮點

### 🚀 HW02 新增進階功能
1. **長期記憶 (Long-term Memory)**：
   - 整合 `memory_db` 模組，支援手動儲存與自動檢索使用者事實（如姓名、偏好）。
   - 實現跨 Session 的資訊持久化，AI 即使在重新對話後也能記住重要細節。
2. **多模態支援 (Multimodal)**：
   - 支援圖片上傳（JPG/PNG）與分析。
   - 透過 Base64 編碼處理影像，並結合 Groq 視覺模型進行圖像理解。
3. **自動路由 (Auto Routing)**：
   - 內建智能路由邏輯，根據輸入任務自動選擇最佳模型：
     - **視覺任務**：`llama-3.2-11b-vision-preview`
     - **複雜任務/長文**：`llama-3.3-70b-versatile`
     - **一般對話**：`llama3-8b-8192`
4. **工具使用與環境感知 (Tool Use / MCP)**：
   - 實作外部工具注入（如當前系統時間），模擬模型上下文協議 (MCP) 精神，讓 AI 具備即時資訊感知能力。

### 🛠️ HW01 基礎功能
- **人格自訂**：可自由編輯 System Prompt 定義 AI 角色。
- **參數動態調整**：支援 Temperature 與 Max Tokens 即時調教。
- **短期交談記憶**：利用 Session State 維持流暢的上下文對話。
- **串流輸出 (Streaming)**：提供逐字生成的打字機互動體驗。

## 技術棧
- **Frontend**: Streamlit
- **LLM Engine**: Groq API (Llama 3.3, Llama 3.2 Vision, Mixtral)
- **Language**: Python 3.x
- **Environment**: python-dotenv, base64, custom memory module

## 快速開始

1. **複製專案並安裝套件**：
   ```bash
   git clone [你的專案網址]
   pip install -r requirements.txt
