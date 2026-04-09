import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
import random

# アプリの設定
st.set_page_config(page_title="2年生国試対策")
st.title("🩺 ２年生国家試験対策")

# --- 1. Googleスプレッドシートへの接続 ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 問題データの読み込み
df_questions = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1ZqpqYB5a3BZ--cjB-KGufhXTH6jPeocC-wPbEXVS_ZQ/edit?usp=sharing")

# --- 2. ログイン画面（学籍番号・氏名入力） ---
with st.container():
    col1, col2 = st.columns(2)
    # keyを設定することで、ログアウト時に確実に消去できるようにします
    student_id = col1.text_input("学籍番号を入力してください", key="s_id")
    student_name = col2.text_input("氏名を入力してください", key="s_name")

# --- 3. メイン処理（ログインしている場合のみ表示） ---
if student_id and student_name:
    st.divider()
    st.success(f"ログイン中: {student_name} さん")

    # 問題をランダムに1つ選んで保持する
    if "target_q_id" not in st.session_state:
        st.session_state.target_q_id = random.choice(df_questions["id"].tolist())

    q_id = st.session_state.target_q_id
    q_data = df_questions[df_questions["id"] == q_id].iloc[0]

    # 問題の表示
    st.write(f"### 今日の挑戦問題：{q_id}")
    st.subheader(f"分野: {q_data['分野']}")
    st.info(q_data["問題文"])

    # 選択肢の表示
    options = [q_data["選択肢1"], q_data["選択肢2"], q_data["選択肢3"], q_data["選択肢4"]]
    answer = st.radio("答えを選んでください", options)
    
    # 振り返り入力
    st.warning("🧐 **なぜその選択肢を選びましたか？（根拠を記入）**")
    reflection = st.text_area("振り返り入力", placeholder="例：〇〇の作用により血管が収縮するため")

    # 送信ボタン
    if st.button("回答を送信する"):
        # GoogleフォームのURL（回答送信専用）
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdlhoQgH7we1JHnb1SEK_3vIBuBteLIfxQcUh1FIvacF82Yyg/formResponse"
        
        # 送信データの組み立て
        params = {
            "entry.366527335": student_id,
            "entry.1974944765": student_name,
            # 必要に応じて問題IDや振り返りのentry IDも追加可能
        }

        try:
            response = requests.post(form_url, data=params)
            if response.status_code == 200:
                st.success(f"送信完了！ 正解は「{q_data['正解']}」でした。")
                st.balloons()
                st.write("履歴は管理者（対策委員）のスプレッドシートに記録されました。")
            else:
                st.error("送信に失敗しました。フォームの設定を確認してください。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

    st.divider()

    # ログアウトボタン
    if st.button("ログアウトしてログイン画面に戻る"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

else:
    # ログインしていない時の表示
    st.info("👆 学籍番号と氏名を入力すると、問題が表示されます。")
