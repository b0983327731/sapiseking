import streamlit as st
import random
import json
import os
import re
import io
from gtts import gTTS

# 🚀 全域系統版本號
APP_VERSION = "v3.1.0 (Super Cartoon Edition 🎈)"

# 設定頁面基本資訊 (使用 wide 讓排版更可愛、寬敞)
st.set_page_config(page_title="阿美族語卡通學習樂園", page_icon="🎈", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 🎨 自定義卡通風格 CSS 樣式 (不省略任何細節)
# ==========================================
def apply_cartoon_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Noto+Sans+TC:wght@400;700&display=swap');

    /* 全局背景與字體 */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans TC', sans-serif;
        background-color: #FFFDE7; /* 溫暖的淺鵝黃色背景 */
    }

    /* 頂部導覽列及標題風格 */
    h1 {
        font-family: 'Fredoka', 'Noto Sans TC', sans-serif;
        color: #FF6F00;
        text-shadow: 3px 3px 0px #FFE082;
        font-weight: 700;
    }
    h2, h3 {
        color: #E65100;
        font-weight: 700;
    }

    /* 彈跳立體卡通卡片風格 */
    .quiz-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 24px;
        border: 4px solid #FFB300;
        box-shadow: 6px 6px 0px #FF8F00;
        margin-top: 20px;
        margin-bottom: 30px;
        transition: all 0.2s ease-in-out;
        color: #3E2723;
    }
    .quiz-card:hover {
        transform: translateY(-2px);
        box-shadow: 8px 8px 0px #FF8F00;
    }

    /* 圓潤可愛按鈕 */
    div.stButton > button {
        background-color: #FF7043;
        color: white;
        border: 3px solid #E64A19;
        border-radius: 20px;
        font-weight: bold;
        font-size: 16px;
        padding: 10px 24px;
        box-shadow: 4px 4px 0px #BF360C;
        transition: all 0.1s ease;
    }
    div.stButton > button:hover {
        background-color: #FF5722;
        transform: translate(-1px, -1px);
        box-shadow: 5px 5px 0px #BF360C;
    }
    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #BF360C;
    }

    /* Segmented Control 導覽風格 */
    [data-testid="stSegmentedControl"] {
        background-color: #FFE082;
        border-radius: 20px;
        padding: 8px;
        border: 3px solid #FFB300;
    }
    [data-testid="stSegmentedControl"] button {
        border-radius: 15px !important;
        font-weight: bold !important;
        color: #5D4037 !important;
    }

    /* 訊息外框與輸入框卡通化 */
    .stTextInput input, textarea {
        border: 3px solid #FFB300 !important;
        border-radius: 15px !important;
        background-color: #FFF8E1 !important;
    }
    
    hr {
        border-top: 3px dashed #FFB300;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🛡️ 防腐層：保留指定的原始結構與函數
# ==========================================
VOCABULARY = []
SENTENCES = []

def init_quiz(): 
    pass

def play_audio(): 
    pass

def show_learning_mode(): 
    pass

def show_quiz_mode(): 
    pass

def show_debug_info(): 
    pass

# 原始聽力題庫 (15題標準數據庫，完全保留)
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["hadhad", "hakhak", "hawan", "hafay"], "correct_text": "hafay"},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["tefo'", "'okoy", "tafokod", "tafolod"], "correct_text": "tafokod"},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["fakar", "tayhi", "pitaw", "tarakar"], "correct_text": "pitaw"},
    {"id": 6, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-06.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sariri'", "riri'", "siri", "riyar"], "correct_text": "siri"},
    {"id": 7, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-07.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["koleto", "lokot", "kewaw", "kakorot"], "correct_text": "koleto"},
    {"id": 8, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-08.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["siwoy", "kodasing", "konga", "damay"], "correct_text": "konga"},
    {"id": 9, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-09.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["mali'", "tikami", "tilifi", "pawli"], "correct_text": "tilifi"},
    {"id": 10, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-10.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["picakay", "pitangtang", "picaliw", "pafeli'"], "correct_text": "picakay"},
    {"id": 11, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-11.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["'olaw", "'alo", "fao", "tao"], "correct_text": "tao"},
    {"id": 12, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-12.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["rorang", "kolong", "lotong", "ekong"], "correct_text": "lotong"},
    {"id": 13, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-13.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["Halitamako", "Haliradiw", "Haliepah", "Hali'ecaw"], "correct_text": "Haliepah"},
    {"id": 14, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-14.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["dafak", "a'ayad", "dadaya", "kamaya"], "correct_text": "dadaya"},
    {"id": 15, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-15.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sioy", "simal", "sinafel", "simico"], "correct_text": "sinafel"}
]

# ==========================================
# 🎵 南島語系動態發音引擎 (TTS)
# ==========================================
def play_tts(text):
    """
    在上傳實體聲音檔之前，利用印尼語(id)近似南島語系發音規則，
    自動萃取題幹中的阿美語並進行動態發音。
    """
    match = re.search(r'「(.*?)」', text)
    if match:
        target_text = match.group(1)
    else:
        target_text = re.sub(r'請問.*?中文意思是什麼|的阿美語是哪一個|聆聽音檔.*?|題目：|阿美語：|中文：.*', '', text)
        target_text = re.sub(r'[\u4e00-\u9fa5]', '', target_text) 
        target_text = re.sub(r'^\d+[\.、]\s*', '', target_text) 
    
    target_text = target_text.strip()
    if not target_text:
        target_text = text 
        
    try:
        tts = gTTS(text=target_text, lang='id')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp.getvalue(), format="audio/mp3")
    except Exception as e:
        st.error("⚠️ 無法生成語音，請確認環境是否支援 gTTS 或檢查網路連線。")

# ==========================================
# 🧠 動態解析引擎：跨行讀取與穩定分割版
# ==========================================
def load_question_bank():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd_dir = os.getcwd()

    db = {
        "聽音選詞": [], "對話理解": [], "段落朗讀": [], "情境問答": [],
        "看圖表達": [], "詞彙語意": [], "語言結構": [], "句子聽寫": [], "問答": []
    }
    
    scanned_files = []
    for d in [base_dir, cwd_dir]:
        if not os.path.exists(d): continue
        try:
            for f in os.listdir(d):
                if f.lower().endswith(".txt") and f.lower() not in ["app.txt", "requirements.txt", "提示詞.txt"]:
                    scanned_files.append(os.path.join(d, f))
        except:
            pass

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
            except:
                continue
        if file_loaded:
            break

    if not file_loaded:
        return db

    current_section = None
    current_question = []

    def save_question():
        if current_section and current_question:
            q_text = " ".join(current_question).strip()
            if re.match(r'^\d+[\.、]', q_text):
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
        elif re.match(r'^\d+[\.、]', line):
            save_question()
            current_question.append(line)
        else:
            if current_question:
                current_question.append(line)
                
    save_question()
    return db

# ==========================================
# 🎨 卡通風格 UI 渲染邏輯 (結合動態 TTS 發音)
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題 (卡通風格)"""
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
        col_q, col_btn = st.columns([4, 1.5])
        
        with col_q:
            if is_listening:
                if st.toggle("👁️ 顯示題目文字", key=f"t_show_q_{prefix}"):
                    st.markdown(f"**🌟 {q_part}**")
                else:
                    st.markdown("**🎈 [文字隱藏中，請點擊右方播放卡通發音]**")
            else:
                st.markdown(f"**🌟 {q_part}**")
                
        with col_btn:
            if st.button("🎵 播放語音", key=f"tts_btn_{prefix}"):
                play_tts(q_part)
        
        opts = []
        for tag in ["(A)", "(B)", "(C)", "(D)"]:
            if tag in opts_str:
                opt_text = opts_str.split(tag, 1)[1]
                for next_tag in ["(B)", "(C)", "(D)"]:
                    if next_tag > tag and next_tag in opt_text:
                        opt_text = opt_text.split(next_tag, 1)[0]
                opts.append(tag + " " + opt_text.strip())

        user_ans = st.radio("✨ 請選擇您的答案：", opts, index=None, key=prefix)
        
        if st.toggle("💡 顯示解題魔法盒", key=f"t_ans_{prefix}"):
            if ans_str:
                msg = f"🎉 **正確答案：** {ans_str}"
                if ana_str: msg += f"\n\n🔍 **解析：** {ana_str}"
                st.success(msg)
            else:
                st.warning("無標準答案。")
        elif user_ans and ans_str:
            if ans_str in user_ans:
                st.success(f"🥳 太棒了！答對囉！" + (f" 解析：{ana_str}" if ana_str else ""))
            else:
                st.error(f"❌ 哎呀答錯囉！正確答案是：{ans_str}。" + (f" 解析：{ana_str}" if ana_str else ""))
    except Exception as e:
        st.info(line) 

def render_reading(line, prefix):
    """渲染段落朗讀 (卡通風格)"""
    try:
        q_part = line
        ch_part = ""
        if "(中文：" in line:
            parts = line.split("(中文：", 1)
            q_part = parts[0].strip()
            ch_part = parts[1].strip(")")
        elif "(中文大意：" in line:
            parts = line.split("(中文大意：", 1)
            q_part = parts[0].strip()
            ch_part = parts[1].strip(")")
        
        col_q, col_btn = st.columns([4, 1.5])
        with col_q:
            st.markdown(f"📖 **{q_part}**")
        with col_btn:
            if st.button("🎵 朗讀音檔", key=f"tts_btn_{prefix}"):
                play_tts(q_part)
                
        if ch_part:
            if st.toggle("💡 顯示中文翻譯", key=f"t_{prefix}"):
                st.success(f"📌 中文對照：{ch_part}")
    except:
        st.info(line)

def render_qa(line, prefix):
    """渲染問答與情境問答 (卡通風格)"""
    try:
        text = line
        q_am = text
        ch_hint = ""
        ans = ""
        ana = ""
        
        if "中文：" in text:
            parts = text.split("中文：", 1)
            q_am = parts[0].strip()
            text = parts[1]
            
        if "參考回答：" in text:
            parts = text.split("參考回答：", 1)
            ch_hint = parts[0].strip()
            text = parts[1]
        elif "作答參考：" in text:
            parts = text.split("作答參考：", 1)
            ch_hint = parts[0].strip()
            text = parts[1]
            
        if "分析：" in text:
            parts = text.split("分析：", 1)
            ans = parts[0].strip()
            ana = parts[1].strip()
        else:
            if not ans: 
                ans = text.strip()
        
        q_am = q_am.replace("題目：", " 題目：")
        
        col_q, col_btn = st.columns([4, 1.5])
        with col_q:
            is_situational = "情境問答" in prefix
            if is_situational:
                if st.toggle("👁️ 顯示題目與提示", key=f"t_show_q_{prefix}"):
                    st.markdown(f"🗣️ **{q_am}**")
                    if ch_hint:
                        st.caption(f"💡 中文提示：{ch_hint}")
                else:
                    st.markdown("**🎈 [提示文字隱藏中]**")
            else:
                st.markdown(f"🗣️ **{q_am}**")
                if ch_hint:
                    st.caption(f"💡 中文提示：{ch_hint}")
                    
        with col_btn:
            if st.button("🎵 聽取問句", key=f"tts_btn_{prefix}"):
                play_tts(q_am)
            
        if ans or ana:
            if st.toggle("💡 顯示參考解答", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"✨ 參考解答：{ans}"
                if ana: msg += f"\n\n🔍 分析：{ana}"
                st.success(msg)
                if ans:
                    if st.button("🎵 發音參考解答", key=f"tts_ans_{prefix}"):
                        play_tts(ans)
    except:
        st.info(line)

def render_picture(line, prefix):
    """渲染看圖表達 (卡通風格)"""
    try:
        text = line
        pic = text
        hint = ""
        ans = ""
        ana = ""
        
        if "圖片情境：" in text:
            parts = text.split("圖片情境：", 1)
            pic = parts[1]
            
        if "中文提示：" in pic:
            parts = pic.split("中文提示：", 1)
            pic = parts[0].strip()
            hint_part = parts[1]
            
            if "作答參考：" in hint_part:
                h_parts = hint_part.split("作答參考：", 1)
                hint = h_parts[0].strip()
                ans_part = h_parts[1]
                
                if "重點分析：" in ans_part:
                    a_parts = ans_part.split("重點分析：", 1)
                    ans = a_parts[0].strip()
                    ana = a_parts[1].strip()
                elif "重點：" in ans_part:
                    a_parts = ans_part.split("重點：", 1)
                    ans = a_parts[0].strip()
                    ana = a_parts[1].strip()
                else:
                    ans = ans_part.strip()
            else:
                hint = hint_part.strip()
        
        try:
            idx = int(prefix.split('_')[-1]) + 1
            img_path_jpg = f"assets/images/picture_{idx}.jpg"
            img_path_png = f"assets/images/picture_{idx}.png"
            
            if os.path.exists(img_path_jpg):
                st.image(img_path_jpg, use_container_width=True)
            elif os.path.exists(img_path_png):
                st.image(img_path_png, use_container_width=True)
            else:
                st.info(f"🖼️ 溫馨小提示：若要顯示圖片，請將圖片命名為 `picture_{idx}.jpg` 或 `.png` 並放在 `assets/images/` 資料夾中！")
        except:
            pass

        st.markdown(f"🎨 **圖片情境：** {pic}")
        
        if hint:
            st.caption(f"💡 中文提示：{hint}")
            
        st.text_area("✍️ 請在此輸入您的口說草稿：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="可以在此輸入您的口說草稿...")
            
        if ans or ana:
            if st.toggle("💡 顯示作答參考", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"✨ 作答參考：{ans}"
                if ana: msg += f"\n\n🔍 重點：{ana}"
                st.success(msg)
                if ans:
                    if st.button("🎵 發音作答參考", key=f"tts_ans_{prefix}"):
                        play_tts(ans)
    except:
        st.info(line)

def render_dictation(line, prefix):
    """渲染句子聽寫 (卡通風格)"""
    try:
        text = line
        am = text
        ch = ""
        ana = ""
        
        if "中文：" in text:
            parts = text.split("中文：", 1)
            am = parts[0].replace("阿美語：", "").strip()
            text = parts[1]
            
            if "分析：" in text:
                sub_parts = text.split("分析：", 1)
                ch = sub_parts[0].strip()
                ana = sub_parts[1].strip()
            else:
                ch = text.strip()
        
        st.text_area("✍️ 請在此輸入您的聽寫句子：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="請在此輸入您聽寫的句子...")
        
        col_q, col_btn = st.columns([4, 1.5])
        
        with col_q:
            if st.toggle("👁️ 顯示聽寫原文", key=f"t_show_dict_{prefix}"):
                st.markdown(f"✍️ **{am}**")
            else:
                st.markdown("**🎈 [原文隱藏中，請點擊右側按鈕進行聽寫測試]**")
                
        with col_btn:
            if st.button("🎵 播放語音", key=f"tts_btn_{prefix}"):
                play_tts(am)
            
        if ch or ana:
            if st.toggle("💡 顯示翻譯與分析", key=f"t_{prefix}"):
                msg = ""
                if ch: msg += f"📌 中文：{ch}"
                if ana: msg += f"\n\n🔍 分析：{ana}"
                st.success(msg)
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器 (卡通外框)"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"⚠️ 系統找不到【{section_name}】的資料，請檢查題庫檔案！")
        return

    for i, line in enumerate(questions):
        with st.container():
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            if "聽音選詞" in section_name or "對話理解" in section_name or section_name in ["詞彙語意", "語言結構"]:
                render_mcq(line, f"{section_name}_{i}")
            elif section_name == "段落朗讀":
                render_reading(line, f"{section_name}_{i}")
            elif section_name in ["情境問答", "問答"]:
                render_qa(line, f"{section_name}_{i}")
            elif section_name == "看圖表達":
                render_picture(line, f"{section_name}_{i}")
            elif section_name == "句子聽寫":
                render_dictation(line, f"{section_name}_{i}")
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🚀 應用程式主邏輯 (Main)
# ==========================================
def main():
    apply_cartoon_theme()

    st.title("🌟 阿美族語卡通學習樂園 🎈")
    st.caption("✨ 歡迎來到趣味滿點的族語檢定闖關世界！選擇下方導覽開始冒險吧！")

    main_options = ["📋 認證考試說明", "🎧 聽力闖關", "🗣️ 口說練習", "📖 閱讀天地", "✍️ 寫作挑戰"]
    current_tab = st.segmented_control("主選單導覽", main_options, default=None, label_visibility="collapsed")

    if "previous_tab" not in st.session_state:
        st.session_state.previous_tab = None

    if st.session_state.previous_tab != current_tab:
        st.session_state.submitted = False
        st.session_state.audio_triggered = False
        if "writing_submitted" in st.session_state:
            st.session_state.writing_submitted = False
        st.session_state.previous_tab = current_tab

    db = load_question_bank()

    if current_tab == "📋 認證考試說明":
        st.subheader("📋 [認證考試說明與指南](https://lokahsu.ilrdf.org.tw/web_lokahsu/Files/Guide/1_20251211_162558.pdf)")
        st.divider()
        st.info("💡 貼心提醒：請透過上方導覽列選擇您要進行的測驗項目。系統將自動從資料庫載入完整題庫，並附帶可愛的南島語系模擬發音按鈕，陪您輕鬆學習！")

    elif current_tab == "🎧 聽力闖關":
        st.subheader("🎧 聽力測驗 (pitengil) - 聽音辨位大冒險")
        st.divider()
        listening_sub = st.radio("🎯 選擇聽力題型：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True)
        if listening_sub == "選擇題-聽音選詞":
            render_section("聽音選詞", db)
        elif listening_sub == "選擇題-對話理解":
            render_section("對話理解", db)

    elif current_tab == "🗣️ 口說練習":
        st.subheader("🗣️ 口說測驗 (pisowal) - 開口說族語")
        st.divider()
        speaking_sub = st.radio("🎯 選擇口說題型：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
        if speaking_sub == "段落朗讀":
            render_section("段落朗讀", db)
        elif speaking_sub == "情境問答":
            render_section("情境問答", db)
        elif speaking_sub == "看圖表達":
            render_section("看圖表達", db)

    elif current_tab == "📖 閱讀天地":
        st.subheader("📖 閱讀測驗 (piasip) - 智慧大考驗")
        st.divider()
        reading_sub = st.radio("🎯 選擇閱讀題型：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True)
        if reading_sub == "選擇題-詞彙語意":
            render_section("詞彙語意", db)
        elif reading_sub == "選擇題-語言結構":
            render_section("語言結構", db)

    elif current_tab == "✍️ 寫作挑戰":
        st.subheader("✍️ 寫作測驗 (pitilid) - 魔法文字書寫")
        st.divider()
        writing_sub = st.radio("🎯 選擇寫作題型：", ["句子聽寫", "問答"], horizontal=True)
        if writing_sub == "句子聽寫":
            render_section("句子聽寫", db)
        elif writing_sub == "問答":
            render_section("問答", db)

    st.write("---")
    st.markdown(f"""
    <div style="text-align: center; color: #A1887F; margin-top: 50px; font-size: 14px;">
        🎉 2026 中高級認證 App 三一開發團隊 ｜ 系統版本： <b>{APP_VERSION}</b> 🎈
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
