import os
import time
import re
from datetime import datetime

dir_path = "new_file" 

all_files = os.listdir(dir_path)
pre_file = set(all_files)

while True:
    now = datetime.now()
    day = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H:%M:%S")

    current_file = set(os.listdir(dir_path))
    result_diff = current_file - pre_file

    for file_name in result_diff:
        print(f"새로운 파일 탐지 : {file_name}")

        file_path = os.path.join(dir_path, file_name)

        with open(f"{day}_탐지 보고서.txt", "a", encoding="UTF-8") as report_file:
            report_file.write(f"작성자 : 유연송\n")
            report_file.write(f"주요 내용 : 신규파일 탐지 및 내용 분석\n")
            report_file.write(f"{hour}에 '{file_name}' 신규파일이 탐지되었습니다.\n")

            if file_name.endswith(".txt"):
                comment_detections = []
                email_detections = [] 

                with open(file_path, 'r', encoding='utf-8') as content_file:
                    lines = content_file.readlines()

                    for index, line in enumerate(lines):
                        
                        if line.startswith("#") or line.startswith(("//")):
                            comment_detections.append(f"  - 주석 탐지: {file_name} {index+1}라인: {line.strip()}")
                            print(f"  - 주석 탐지: {file_name} {index+1}라인: {line.strip()}")
                        
                        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', line):
                            email_detections.append(f"  - 이메일 탐지: {file_name} {index+1}라인: {line.strip()}")
                            print(f"  - 이메일 탐지: {file_name} {index+1}라인: {line.strip()}")
                        

                if comment_detections:

                    for detection in comment_detections:
                        report_file.write(f"{detection}\n")
                
                if email_detections:
                    for detection in email_detections:
                        report_file.write(f"{detection}\n")

            report_file.write("="*50)
    pre_file = set(os.listdir(dir_path))

    print("모니터링 중")
    time.sleep(1)
