from flask import Flask, request, render_template
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)

# OneDrive에서 변환된 다운로드 링크 (여기에 올바른 링크를 넣어야 해!)
onedrive_url = "https://jj63e-my.sharepoint.com/personal/mestory83_jj63e_onmicrosoft_com/_layouts/15/download.aspx?share=EewDhk00vM5BoTVZIxTOpwEBeguO_q1HT4Tk-ULJl7ZJsw"

def load_excel_from_onedrive():
    response = requests.get(onedrive_url)
    
    if response.status_code == 200:
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        return df
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    student_info = None
    message = ""
    df = load_excel_from_onedrive()  # 최신 데이터 불러오기

    if df is None:
        message = "데이터를 불러올 수 없습니다."
        return render_template('index.html', message=message)
    
    if request.method == 'POST':  # 사용자가 폼을 제출했을 때 실행
        name = request.form['name']
        birth = request.form['birth']

        # 입력한 값과 엑셀 데이터 비교
        student_info = df[(df['이름'] == name) & (df['주민번호 앞자리'] == int(birth))]

        if student_info.empty:
            message = "일치하는 학생이 없습니다."

    return render_template('index.html', student_info=student_info, message=message)

if __name__ == '__main__':
    app.run(debug=True)
