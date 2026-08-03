import streamlit as st
import random
import json
import os
import re
import io
from gtts import gTTS
import base64

# ==========================================
# 🚀 全域系統設定與資源
# ==========================================
APP_VERSION = "v3.0.0 (Cartoon Learning Edition 🎨)"
# 設定頁面基本資訊
st.set_page_config(page_title="阿美族語卡通學習樂園", page_icon="🎉", layout="wide", initial_sidebar_state="collapsed")

# 定義阿美語常見的顏色對應，用於UI裝飾
AMIS_COLORS = {
    "kohecalay": "#FFFFFF", "kohetingay": "#333333", "kahengangay": "#E74C3C",
    "kangdaway": "#2ECC71", "faliyos": "#3498DB", "cidal": "#F1C40F"
}

# ==========================================
# 🎵 核心功能：南島語系動態發音引擎 (TTS)
# ==========================================
def play_tts(text):
    """
    利用印尼語(id)近似南島語系發音規則，進行動態發音。
    """
    # 1. 嘗試抓取「」內的阿美語詞彙 (針對選擇題)
    match = re.search(r'「(.*?)」', text)
    if match:
        target_text = match.group(1)
    else:
        # 2. 若無引號，過濾掉常見中文題幹與中文字，保留阿美語
        target_text = re.sub(r'請問.*?中文意思是什麼|的阿美語是哪一個|聆聽音檔.*?|題目：|阿美語：|中文：.*', '', text)
        target_text = re.sub(r'[\u4e00-\u9fa5]', '', target_text) # 移除所有中文字
        target_text = re.sub(r'^\d+[\.\]\s*', '', target_text) # 移除題號
    
    target_text = target_text.strip()
    if not target_text: target_text = text
        
    try:
        tts = gTTS(text=target_text, lang='id') # 使用印尼語發音近似阿美語
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        # 自動播放音訊
        st.audio(fp.getvalue(), format="audio/mp3")
    except Exception as e:
        st.error("⚠️ 無法生成語音，請檢查網路連線。")

# ==========================================
# 🧠 資料解析引擎 (保留原始結構)
# ==========================================
def load_question_bank():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db = {
        "聽音選詞": [], "對話理解": [], "段落朗讀": [], "情境問答": [],
        "看圖表達": [], "詞彙語意": [], "語言結構": [], "句子聽寫": [], "問答": []
    }
    
    scanned_files = []
    if os.path.exists(base_dir):
        try:
            for f in os.listdir(base_dir):
                if f.lower().endswith(".txt") and f.lower() not in ["app.txt", "requirements.txt", "提示詞.txt"]:
                    scanned_files.append(os.path.join(base_dir, f))
        except: pass

    target_content = ""
    file_loaded = False
    encodings_to_try = ["utf-8", "utf-8-sig", "big5", "cp950"]

    for filepath in set(scanned_files):
        for enc in encodings_to_try:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    text_data = f.read()
                    if "聽音選詞" in text_data and "對話理解" in text_data:
                        target_content = text_data
                        file_loaded = True
                        break
            except: continue
        if file_loaded: break

    if not file_loaded: return db

    current_section = None
    current_question = []

    def save_question():
        if current_section and current_question:
            q_text = " ".join(current_question).strip()
            if re.match(r'^\d+[\.\]]', q_text):
                db[current_section].append(q_text)
            current_question.clear()

    for line in target_content.split("\n"):
        line = line.strip()
        if not line:
            save_question()
            continue
        if "一、選擇題（聽音選詞）" in line: save_question(); current_section = "聽音選詞"
        elif "二、選擇題（對話理解）" in line: save_question(); current_section = "對話理解"
        elif "三、段落朗讀" in line: save_question(); current_section = "段落朗讀"
        elif "四、情境問答" in line: save_question(); current_section = "情境問答"
        elif "五、看圖表達" in line: save_question(); current_section = "看圖表達"
        elif "六、選擇題（詞彙語意）" in line: save_question(); current_section = "詞彙語意"
        elif "七、選擇題（語言結構）" in line: save_question(); current_section = "語言結構"
        elif "八、句子聽寫" in line: save_question(); current_section = "句子聽寫"
        elif "九、問答" in line: save_question(); current_section = "問答"
        elif re.match(r'^\d+[\.\]]', line):
            save_question()
            current_question.append(line)
        else:
            if current_question: current_question.append(line)
    save_question()
    return db

# ==========================================
# 🎨 卡通風格 UI 渲染邏輯
# ==========================================

# 自定義 CSS 樣式，營造活潑、圓潤的卡通感
def apply_custom_css():
    st.markdown("""
    <style>
    /* 全局字體與背景 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans TC', sans-serif;
        background-color: #FFFDE7; /* 淺鵝黃色背景 */
    }
    
    /* 標題樣式 */
    h1, h2, h3 {
        color: #3E2723; /* 深咖啡色標題 */
        font-weight: bold;
        text-shadow: 2px 2px 0px #FFF9C4;
    }

    /* 卡片樣式 - 模擬立體卡通塊 */
    .st-emotion-cache-1r6slon.e1f1d6gn4 {
        background-color: white;
        border: 3px solid #3E2723;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 5px 5px 0px #A1887F; /* 咖啡色陰影 */
        margin-bottom: 20px;
    }
    
    /* 按鈕樣式 - 圓潤、有彈性 */
    div.stButton > button {
        background-color: #FFCC80; /* 亮橘色 */
        color: #3E2723;
        border: 3px solid #3E2723;
        border-radius: 15px;
        font-weight: bold;
        font-size: 16px;
        padding: 10px 24px;
        transition: all 0.2s ease;
        box-shadow: 3px 3px 0px #A1887F;
    }
    div.stButton > button:hover {
        background-color: #FFB74D;
        transform: translate(-1px, -1px);
        box-shadow: 4px 4px 0px #A1887F;
    }
    
    /* Segmented Control 樣式 */
    [data-testid="stSegmentedControl"] {
        background-color: #FFF9C4;
        border-radius: 15px;
        padding: 5px;
        border: 2px solid #3E2723;
    }
    [data-testid="stSegmentedControl"] > div > div > button {
        border-radius: 10px;
        border: none;
        color: #3E2723;
    }
    [data-testid="stSegmentedControl"] > div > div > button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FF9800;
        color: white;
        box-shadow: none;
    }

    /* Radio Button 樣式 */
    [data-testid="stRadio"] label {
        background-color: #FFFDE7;
        border: 2px solid #A1887F;
        border-radius: 10px;
        padding: 8px 15px;
        margin-bottom: 5px;
        transition: all 0.2s;
    }
    [data-testid="stRadio"] label:hover {
        background-color: #FFECB3;
        border-color: #FF9800;
    }

    /* Toggle Switch 樣式 */
    [data-testid="stCheckbox"] {
        background-color: #FFF9C4;
        padding: 5px 10px;
        border-radius: 10px;
    }

    /* 文字區域樣式 */
    textarea {
        border: 2px solid #3E2723 !important;
        border-radius: 10px !important;
        background-color: #FFFDE7 !important;
    }
    
    /* 頁尾樣式 */
    footer {visibility: hidden;}
    .app-footer {
        text-align: center;
        color: #A1887F;
        margin-top: 50px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 裝飾用的標題，帶有可愛圖示
def cartoon_header(icon, text, color="#FF9800"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 4px solid {color};">
        <div style="font-size: 50px; filter: drop-shadow(3px 3px 0px #A1887F);">{icon}</div>
        <h1 style="margin:0; color: {color}; text-shadow: 3px 3px 0px #FFF9C4;">{text}</h1>
    </div>
    """, unsafe_allow_html=True)

# 裝飾用的分隔線
def cartoon_divider():
    st.markdown("""
    <div style="margin: 30px 0; text-align: center; font-size: 30px; color: #A1887F;">
        ✦ ✧ ✦ ✧ ✦ ✧
    </div>
    """, unsafe_allow_html=True)

# 渲染選擇題 (MCQ) - 卡通版
def render_mcq(line, prefix):
    try:
        if "(A)" not in line:
            st.info(line)
            return

        parts = line.split("(A)", 1)
        q_part = parts[0].strip()
        rest = "(A)" + parts[1]
        
        opts_str = rest
        ans_str = ""
        ana_str = ""
        
        if "答案：" in rest:
            ans_parts = rest.split("答案：", 1)
            opts_str = ans_parts[0].strip()
            ans_ana = ans_parts[1]
            if "分析：" in ans_ana:
                final_parts = ans_ana.split("分析：", 1)
                ans_str = final_parts[0].strip("。 ")
                ana_str = final_parts[1].strip()
            else:
                ans_str = ans_ana.strip("。 ")

        is_listening = "聽音選詞" in prefix or "對話理解" in prefix
        
        # 題目區塊
        with st.container():
            st.markdown('<div class="st-emotion-cache-1r6slon.e1f1d6gn4">', unsafe_allow_html=True)
            
            # 🌟 UI 佈局：題目與發音按鈕並列
            col_q, col_btn = st.columns([4, 1.5])
            with col_q:
                if is_listening:
                    st.markdown(f"### 🎧 聽音檔，選出關聯的詞彙：")
                    if st.toggle("👁️ 顯示題目文字 (偷看一下 👀)", key=f"t_show_q_{prefix}"):
                        st.markdown(f"**{q_part}**")
                    else:
                        st.markdown("**[🔊 點擊右方按鈕播放發音]**")
                else:
                    st.markdown(f"### ❓ **{q_part}**")
            with col_btn:
                if st.button("🔊 聽發音", key=f"tts_btn_{prefix}", help="點擊播放模擬發音"):
                    play_tts(q_part)
            
            st.markdown("---")
            
            # 安全切割四個選項
            opts = []
            for tag in ["(A)", "(B)", "(C)", "(D)"]:
                if tag in opts_str:
                    opt_text = opts_str.split(tag, 1)[1]
                    for next_tag in ["(B)", "(C)", "(D)"]:
                        if next_tag > tag and next_tag in opt_text:
                            opt_text = opt_text.split(next_tag, 1)[0]
                    opts.append(opt_text.strip()) # 只要選項內容，標籤用 st.radio 內建的

            user_ans = st.radio("✨ 請選擇正確的答案：", opts, index=None, key=prefix, horizontal=True)
            
            if user_ans:
                # 判斷正誤
                is_correct = False
                if ans_str and ans_str in ["(A)", "(B)", "(C)", "(D)"]:
                    ans_idx = ord(ans_str.strip("()")) - ord('A')
                    if ans_idx < len(opts) and opts[ans_idx] == user_ans:
                        is_correct = True
                elif ans_str == user_ans: # 有時候答案直接給文字
                     is_correct = True

                if st.toggle("💡 顯示解答與分析 (魔法小卡 ✨)", key=f"t_ans_{prefix}"):
                    if ans_str:
                        # 標註正確選項
                        ans_display = ""
                        if ans_str in ["(A)", "(B)", "(C)", "(D)"]:
                             ans_idx = ord(ans_str.strip("()")) - ord('A')
                             if ans_idx < len(opts):
                                 ans_display = f"({ans_str.strip('()')}) {opts[ans_idx]}"
                             else:
                                 ans_display = ans_str # fallback
                        else:
                             ans_display = ans_str

                        msg = f"### ✅ 正確答案：**{ans_display}**"
                        if ana_str: msg += f"\n\n---\n**🔍 分析小撇步：**\n{ana_str}"
                        st.success(
