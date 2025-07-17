import os, zipfile
from datetime import datetime
from ftplib import FTP
import time

TARGET_DIR = 'static'  # 백업할 디렉토리
FTP_HOSTIP = '192.168.32.128'  # 테스트 FTP 서버 아이피 사용

# 백업할 디렉토리 생성파일들 압축
def zip_dir(directory):
    date_str = datetime.now().strftime('%Y-%m-%d') # 파일 이름 생성방법
    zip_filename = f"{directory}_{date_str}.zip" # 백업디렉토리-날짜.zip
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)
    return zip_filename

# 압축된 파일 FTP 서버로 전송
def upload_ftp(filename):
    with FTP(FTP_HOSTIP) as ftp:
        ftp.login('msfadmin', 'msfadmin')  # 테스트 FTP 서버 아이디와 패스워드 사용
        filesize = os.path.getsize(filename)
        
        delay = filesize / (10 * 1024 * 1024)  # 딜레이 속도 10MB마다 1초
        time.sleep(delay)
        print(f"파일 크기가 {filesize} bytes이며, 서버로 {delay:.2f}초 만에 전송되었습니다.") #압축파일 크기와 서버로 전송된 속도
        
        with open(filename, 'rb') as file:
            ftp.storbinary(f'STOR {os.path.basename(filename)}', file)

# 프로그램 실행
if __name__ == "__main__":
    zip_file = zip_dir(TARGET_DIR)
    print(f"{zip_file} 파일이 생성되었습니다.")
    upload_ftp(zip_file)
    print("FTP서버에 정상적으로 전송되었습니다.")