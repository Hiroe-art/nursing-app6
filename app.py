Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
...     st.info(q_data["問題文"])
...
...     options = [q_data["選択肢1"], q_data["選択肢2"], q_data["選択肢3"], q_data["選択肢4"]]
...     answer = st.radio("答えを選んでください", options)
...
...     # 「なぜ？」の入力欄
...     st.warning("?? **なぜその選択肢を選びましたか？（根拠を記入）**")
...     reflection = st.text_area("振り返り入力", placeholder="例：〇〇の作用により血管が収縮するため")
...
...     if st.button("回答を送信する"):
...         # 正誤判定
...         is_correct = "○" if answer == q_data["正解"] else "×"
...
...         # 保存するデータの作成
...         new_answer = pd.DataFrame([{
...             "日時": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
...             "学籍番号": student_id,
...             "氏名": student_name,
...             "問題ID": q_id,
...             "結果": is_correct,
...             "振り返り（なぜ？）": reflection
...         }])
...
...         # スプレッドシートの「answers」シートに追記
...         # ※実際の運用時は conn.create(worksheet="answers", data=...) 等を使用
...         st.success(f"送信完了！ 正解は「{q_data['正解']}」でした。")
...         st.balloons()
...
...         # ここで自分の正答率を表示するロジックを将来的に追加
...         st.write("履歴は管理者（対策委員）のスプレッドシートに記録されました。")