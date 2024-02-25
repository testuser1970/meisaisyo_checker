import streamlit as st
import time

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import io
from googleapiclient.http import MediaIoBaseDownload

import csv

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import hashlib

# 単純な認証チェック関数
def check_password(input_hash, correct_hash):
    return input_hash == correct_hash

# パスワードをハッシュ化する関数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")

def main():

    # Streamlitセッションステートを初期化
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # ページのレイアウト
    menu = ["Login", "Home"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        # セッションステートを確認して、ログイン状態でなければ警告を表示
        if st.session_state.logged_in:
            st.subheader("Home")
            # ここにHomeページのコンテンツを追加します

            st.title("椿特許事務所～知財管理ページ")

            st.write("""
            - このページは、知財管理のためのものです。
            - [椿特許事務所](https://tsubakipat.jp): このWEBページの制作
            """)


            SCOPES = ['https://www.googleapis.com/auth/drive']

            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'nodal-triumph-399812-fee6c800d8ef.json', SCOPES
            )
            http_auth = credentials.authorize(Http())

            drive_service = build('drive', 'v3', http=http_auth)


            results = drive_service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    ## 拡張子がある時（ファイルの時）
                    if "." in item['name']:
                        print(u'{0} ({1})'.format(item['name'], item['id']))

                        request = drive_service.files().get_media(fileId=item['id'])
                        fh = io.FileIO(item['name'], "wb")
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()

            #csvfile = open('/content/drive/My Drive/番号付新規ユーザー定義エクスポートファイル.csv', 'r', encoding='utf-8')

            #csvfile = open('番号付新規ユーザー定義エクスポートファイル.csv', 'r', encoding='CP932')
            #reader = csv.DictReader(csvfile)

            df = pd.read_csv('新規ユーザー定義エクスポートファイル.csv', encoding='CP932')
            #df
            #df = pd.read_csv(csvfile)


            search_characters = st.text_input('検索文字列・数字等', placeholder='2020-012345 101234JP01', max_chars=20, help='願番、整理番号、貴社番号などなんでも入力可能です')


            #df[df['当方整理番号'].str.contains(search_characters)]

            found_rows = df[df.applymap(lambda x: search_characters in str(x)).any(axis=1)]
            found_rows

            st.write("""
            """)




        else:
            st.warning("You need to login first.")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')

        # ここではハードコードしていますが、本番環境では推奨されません。
        hardcoded_username = "etsuran"
        hardcoded_password_hash = hash_password("KsBh86#") # パスワードのハッシュ

        if st.button("Login"):
            if username == hardcoded_username and check_password(hash_password(password), hardcoded_password_hash):
                st.success("Logged In Successfully メニューからHomeを選んで下さい。")
                st.session_state.logged_in = True # セッションステートにログイン状態を保存
            else:
                st.warning("Incorrect Username/Password")






if __name__ == "__main__":
    main()
