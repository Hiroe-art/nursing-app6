import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="国試対策プロトタイプ")

# --- Googleスプレッドシートへの接続 ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 問題データの読み込み
df_questions = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1ZqpqYB5a3BZ--cjB-KGufhXTH6jPeocC-wPbEXVS_ZQ/edit?usp=sharing")

st.title("🩺 看護師国試 対策プロトタイプ")

# 1. ログイン（学籍番号・氏名入力）
with st.container():
    col1, col2 = st.columns(2)
    student_id = col1.text_input("学籍番号を入力してください")
    student_name = col2.text_input("氏名を入力してください")

if student_id and student_name:
    st.divider()
    
    # 2. 問題の表示（今回は試作として3問からランダムまたは選択）
    q_id = st.selectbox("解く問題を選択してください", df_questions["id"])
    q_data = df_questions[df_questions["id"] == q_id].iloc[0]

    st.subheader(f"分野: {q_data['分野']}")
    st.info(q_data["問題文"])
    
    options = [q_data["選択肢1"], q_data["選択肢2"], q_data["選択肢3"], q_data["選択肢4"]]
    answer = st.radio("答えを選んでください", options)
    
    # 「なぜ？」の入力欄
    st.warning("🧐 **なぜその選択肢を選びましたか？（根拠を記入）**")
    reflection = st.text_area("振り返り入力", placeholder="例：〇〇の作用により血管が収縮するため")

    if st.button("回答を送信する"):
        # 正誤判定
        is_correct = "○" if answer == q_data["正解"] else "×"
        
        # 保存するデータの作成
        new_answer = pd.DataFrame([{
            "日時": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "学籍番号": student_id,
            "氏名": student_name,
            "問題ID": q_id,
            "結果": is_correct,
            "振り返り（なぜ？）": reflection
        }])
        
        # スプレッドシートの「answers」シートに追記
        # ※実際の運用時は conn.create(worksheet="answers", data=...) 等を使用

        # --- ここから追加 ---
        # 既存の回答を読み込んで、新しい回答をくっつける
        existing_answers = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1ZqpqYB5a3BZ--cjB-KGufhXTH6jPeocC-wPbEXVS_ZQ/edit#gid=sharing", worksheet="answers")
        updated_answers = pd.concat([existing_answers, new_answer], ignore_index=True)
        
        # スプレッドシートを更新（書き込み）
        conn.update(worksheet="answers", data=updated_answers)
        # --- ここまで追加 ---

        st.success(f"送信完了！ 正解は「{q_data['正解']}」でした。")
        st.balloons()
        
        # ここで自分の正答率を表示するロジックを将来的に追加
        st.write("履歴は管理者（対策委員）のスプレッドシートに記録されました。")
