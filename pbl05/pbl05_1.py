import os, requests, smtplib, schedule, time
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import pandas as pd
from openpyxl import load_workbook

# .env 파일 로드
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# SMTP 설정 (네이버 기준)
smtp_name = "smtp.naver.com"
smtp_port = 587

# 타겟 웹사이트
TARGET_URL = "https://www.malware-traffic-analysis.net/2024/index.html"

# 1. 웹 스크래핑 함수
def scrape_data():
    print("웹 스크래핑 시작...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(TARGET_URL, headers=headers, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'html.parser')
        tags = soup.select("#main_content > div.blog_entry > ul > li > a.main_menu")

        titles, links = [], []
        for tag in tags:
            title = tag.text.strip()
            url = f"https://www.malware-traffic-analysis.net/2024/{tag.get('href')}"
            if "2024" in title:
                titles.append(title)
                links.append(url)

        print(f"{len(titles)}개의 보고서 수집 완료.")
        return {'Title': titles, 'Link': links}

    except Exception as e:
        print(f"웹 스크래핑 오류: {e}")
        return {}

# 2. 엑셀 저장 함수 (열 너비 자동 조절)
def save_to_excel(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        time.sleep(1)

        wb = load_workbook(filename)
        ws = wb.active

        # 열 너비 자동 조절
        for column_cells in ws.columns:
            max_length = 0
            column_letter = column_cells[0].column_letter
            for cell in column_cells:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column_letter].width = max_length + 2

        wb.save(filename)
        print(f"엑셀 저장 완료: {filename}")
        return True

    except Exception as e:
        print(f"엑셀 저장 오류: {e}")
        return False

# 3. 이메일 전송 함수
def send_email_report(attach_file_path):
    msg = MIMEMultipart()
    today = datetime.now().strftime('%Y-%m-%d')
    msg['Subject'] = f"보안 보고서 - {today}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    body = f"""
안녕하세요,

{today}자 보안 보고서가 첨부되어 있습니다.
자세한 내용은 첨부파일을 확인해주세요.
"""
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with open(attach_file_path, 'rb') as f:
            part = MIMEApplication(f.read(), _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach_file_path))
            msg.attach(part)

        with smtplib.SMTP(smtp_name, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("이메일 전송 완료.")

    except Exception as e:
        print(f"이메일 전송 오류가 발생했습니다.: {e}")

# 4. 전체 작업 실행 함수
def main():
    now = datetime.now()
    print(f"\n[작업 시작] {now.strftime('%Y-%m-%d %H:%M:%S')}")

    filename = f"malware_reports_{now.strftime('%Y%m%d_%H-%M')}.xlsx"
    data = scrape_data()

    if data and save_to_excel(data, filename):
        send_email_report(filename)
    else:
        print("데이터 수집 실패 또는 엑셀 저장 실패로 이메일 전송 생략")

    print(f"[작업 종료] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# 5. 스케줄링 설정
schedule.every().day.at("17:31").do(main)  # 매일 오후 3시 31분 실행

while True:
    schedule.run_pending()
    time.sleep(1)