import os
import sys
import mysql.connector
import datetime
import requests
import xml.etree.ElementTree as elemTree


def main():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'admin',
        passwd = '1234',
        database = 'db_server_b',
    )

    insert_subject(db)
    insert_detailed_subject(db)

    db.close()
    


def insert_subject(db):
    SUBJECTS = (
        (71073, '컴퓨터개론'),
        (70001, '프로그래밍입문'), # 교과번호 모르겠음
        (71002, 'C언어및실습'),
        (30000, '창의공학기초설계'),
        (71078, '논리회로및실습'),
        (71008, '이산수학'),
        (71006, '객체지향프로그래밍및실습'),
        (71055, '멀티미디어응용'),
        (71007, '선형대수'),
        (71042, '확률과통계'),
        (71074, '자료구조'),
        (71016, '데이터통신'),
        (71051, '수리모형과미분방정식'),
        (71067, '유닉스프로그래밍'),
        (71011, '인터넷프로그래밍및실습'),
        (71005, '프로그래밍언어론'),
        (71015, '운영체제'),
        (71068, '윈도우즈프로그래밍'),
        (71079, '컴퓨터구조론'),
        (71028, '컴퓨터보안'),
        (71039, '컴퓨터알고리즘'),
        (71021, '컴퓨터통신'),
        (71013, '화일처리론'),
        (71032, '소프트웨어공학'),
        (71019, '데이터베이스'),
        (71076, '마이크로프로세서설계및실습'),
        (72022, '소프트웨어응용'),
        (71020, '인공지능'),
        (71049, '임베디드시스템설계'),
        (71077, '컴퓨터과학종합설계'),
        (71048, '데이터베이스설계'),
        (71054, '멀티미디어개론'),
        (71063, '모바일소프트웨어설계'),
        (71066, '웹정보시스템'),
        (71018, '컴파일러구성'),
        (71065, '클라우드컴퓨팅'),
        (71075, '네트워크보안'),
        (71033, '컴퓨터그래픽스'),
    )
    cursor = db.cursor()
    query = "INSERT INTO boards_subject (subject_no, title) VALUES (%s, %s)"


    print("DB에 Subject 데이터를 삽입합니다.")
    
    for (subject_no, title) in SUBJECTS:
        print("insert (%d, %s)"%(subject_no, title))
        cursor.execute(query, (subject_no, title))
    db.commit()

    print("DB에 Subject 데이터 삽입을 완료했습니다.")



def insert_detailed_subject(db):
    year = datetime.datetime.now().year
    if datetime.datetime.now().month > 1 and datetime.datetime.now().month < 8:
        term = 'A10'
    else:
        term = 'A20'
    SEMESTER = {'A10': 1, 'A20': 2}

    # 컴퓨터과학부 전공 긁어오기
    URL = 'https://wise.uos.ac.kr/uosdoc/api.ApiUcrMjTimeInq.oapi?apiKey=201702358HOP35429&year=%d&term=%s&deptDiv=23600&dept=A204110511s &subDept=A200200120'%(year, term)
    response = requests.get(URL)
    root = elemTree.fromstring(response.text)
    mainlist = root.find('./mainlist')

    cursor = db.cursor()
    query = "INSERT INTO boards_detailedsubject (year, shyr, semester, professor, subject_id, class_no, admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    

    print("DB에 %d년 %d학기 DetailedSubject 데이터를 삽입합니다."%(year, SEMESTER[term]))

    for sublist in mainlist:
        subject_no = int(sublist.find('subject_no').text)
        if subject_no in (71071, 71072, 38141): # 학업설계상담, 인턴십 제외
            continue
        class_no = sublist.find('class_div').text
        shyr = int(sublist.find('shyr').text)
        professor = sublist.find('prof_nm').text
        
        print("insert (%d, %d, %s, %s, %d, %s)"%(year, shyr, term, professor, subject_no, class_no))
        cursor.execute(query, (year, shyr, term, professor, subject_no, class_no, None))
    db.commit()

    print("DB에 DetailedSubject 데이터 삽입을 완료했습니다.")
    


if __name__ == "__main__":
    main()