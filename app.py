import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import requests 
import random  

st.set_page_config(page_title="2年生国試対策")

# --- Googleスプレッドシートへの接続 ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 問題データの読み込み
df_questions = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1ZqpqYB5a3BZ--cjB-KGufhXTH6jPeocC-wPbEXVS_ZQ/edit?usp=sharing")

st.title("🩺 ２年生国家試験対策")

# 1. ログイン（学籍番号・氏名入力）
with st.container():
    col1, col2 = st.columns(2)
    student_id = col1.text_input("学籍番号を入力してください")
    student_name = col2.text_input("氏名を入力してください")

if student_id and student_name:
    st.divider()
    
    # 2. 問題の表示（今回は試作として3問からランダムまたは選択）
    if "target_q_id" not in st.session_state:
    # まだ問題が選ばれていない場合、リストからランダムに1つ選んで保持する
        st.session_state.target_q_id = random.choice(df_questions["問題ID"].tolist())

q_id = st.session_state.target_q_id
st.write(f"### 今日の挑戦問題：{q_id}")
    q_data = df_questions[df_questions["id"] == q_id].iloc[0]

    st.subheader(f"分野: {q_data['分野']}")
    st.info(q_data["問題文"])
    
    options = [q_data["選択肢1"], q_data["選択肢2"], q_data["選択肢3"], q_data["選択肢4"]]
    answer = st.radio("答えを選んでください", options)
    
    # 「なぜ？」の入力欄
    st.warning("🧐 **なぜその選択肢を選びましたか？（根拠を記入）**")
    reflection = st.text_area("振り返り入力", placeholder="例：〇〇の作用により血管が収縮するため")

   # --- 50行目付近にあるはずの送信ボタン ---
if st.button("回答を送信する"):
    # 1. 正誤判定（これは今のコードにあるはずです）
    is_correct = "○" if answer == q_data["正解"] else "×"
    
    # 2. Googleフォームの「回答送信専用URL」
    # ★ここから新しく追加・置き換え！
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdlhoQgH7we1JHnb1SEK_3vIBuBteLIfxQcUh1FIvacF82Yyg/formResponse"
    
    # 3. 送信するデータの組み立て（先ほど特定したID）
    params = {
        "entry.366527335": student_id,    # 学籍番号
        "entry.1974944765": student_name,  # 氏名
        # 「問題ID」や「振り返り」をフォームに追加した場合は、ここも増やします
    }
    
    # 4. 裏側で送信！
    try:
        requests.post(form_url, data=params) # これがスプレッドシートへの記録の代わりです
        st.success(f"送信完了！ 正解は「{q_data['正解']}」でした。")
        st.balloons()
    except Exception as e:
        st.error(f"送信時にエラーが発生しました: {e}")

    # 元々あった conn.read や conn.update の古いコードは削除してください

        # --- ここから追加 ---
        # 既存の回答を読み込んで、新しい回答をくっつける
        # --- 58行目から62行目あたりをこれ1行に書き換える ---
        conn.create(spreadsheet="https://docs.google.com/spreadsheets/d/1ZqpqYB5a3BZ--cjB-KGufhXTH6jPeocC-wPbEXVS_ZQ/edit?usp=sharing", worksheet="answers", data=new_answer)
        # --- ここまで追加 ---

        st.success(f"送信完了！ 正解は「{q_data['正解']}」でした。")
        st.balloons()
        
        # ここで自分の正答率を表示するロジックを将来的に追加
        st.write("履歴は管理者（対策委員）のスプレッドシートに記録されました。")
