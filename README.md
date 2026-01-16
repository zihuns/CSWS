# CSWS (Computer Science Web Services)

**CSWS**는 서울시립대학교 컴퓨터과학부 학생들을 위한 통합 클라우드 웹 서비스 플랫폼입니다. 학생들에게 개인화된 서버 환경, 코드 공유 커뮤니티, 그리고 웹 호스팅 서비스를 제공하여 학습 효율을 높이고 실습 환경을 지원합니다.

## 📋 목차

- [CSWS (Computer Science Web Services)](#csws-computer-science-web-services)
  - [📋 목차](#-목차)
  - [📝 소개](#-소개)
  - [📅 개발 기간](#-개발-기간)
  - [👥 구성원](#-구성원)
  - [✨ 주요 기능](#-주요-기능)
  - [🛠 기술 스택](#-기술-스택)
  - [🚀 설치 및 실행](#-설치-및-실행)
    - [1. Image Build](#1-image-build)
    - [2. Container 생성 및 실행](#2-container-생성-및-실행)
    - [3. Container 진입](#3-container-진입)
    - [4. Database 설정 (Container 내부)](#4-database-설정-container-내부)
    - [5. Django Migration (Container 내부)](#5-django-migration-container-내부)
    - [6. Superuser 생성](#6-superuser-생성)
    - [7. Server 실행](#7-server-실행)

## 📝 소개

이 프로젝트(**Team Server-B**)는 부족한 컴퓨팅 자원을 대체하고, 학생들에게 호환성 문제 없는 공동의 작업 환경을 제공하기 위해 개발되었습니다.
사용자는 CSWS를 통해 클라우드 서버를 체험하고, 웹 호스팅을 통해 자신만의 웹페이지를 배포하며, 커뮤니티를 통해 코드를 공유하고 학습할 수 있습니다.

📄 **보고서**: [Server-B Wiki](https://capstone.uos.ac.kr/cdc/index.php/Server-B)

## 📅 개발 기간

- 2020년 3월 ~ 2020년 6월 (총 4개월)

## 👥 구성원

- 김창헌(팀장), 김윤태, 백승록, 서지훈, 장영선

## ✨ 주요 기능

- **CSCS (CS Cloud Services)**:
  - OpenStack 및 Docker 기반의 개인 컨테이너 서버 생성 및 관리
  - 웹 기반 터미널(Shellinabox)을 통한 CLI 환경 접속
- **CS Overflow (Board & Compiler)**:
  - 코드 스니펫이 포함된 질문/답변 게시판
  - 웹 컴파일러를 통한 실시간 코드 실행 및 결과 확인 (C, Java, Python 등 지원)
  - 과제 제출 및 자동 채점 시스템 (Test case 기반)
- **CSWS (CS Web Server)**:
  - 개인 웹 페이지 호스팅 (HTML/CSS/JS 파일 업로드/다운로드/삭제)
  - 외부 접속 가능한 URL 제공

## 🛠 기술 스택

이 프로젝트는 다음 기술을 기반으로 합니다.

| 분류             | 기술                                             |
| ---------------- | ------------------------------------------------ |
| **Frontend**     | HTML5, CSS3, JavaScript, Bootstrap 4, Ace Editor |
| **Backend**      | Python, Django                                   |
| **Database**     | MariaDB (MySQL)                                  |
| **Infra/DevOps** | Docker, OpenStack                                |

## 🚀 설치 및 실행

Docker 환경에서 프로젝트를 빌드하고 실행하는 방법입니다.

### 1. Image Build

`web_backend` 폴더와 내부 파일들을 포함하여 이미지를 빌드합니다.

```bash
docker build -t server_b:1.0 .
```

### 2. Container 생성 및 실행

```bash
docker run -it -d -p 8000:8000 --privileged=true --name test server_b:1.0
```

### 3. Container 진입

```bash
docker exec -it test bash
```

### 4. Database 설정 (Container 내부)

```bash
systemctl start mariadb.service
echo "create database db_server_b; grant all privileges on db_server_b.* to 'admin'@'localhost' identified by '1234';" | mysql -u root
```

### 5. Django Migration (Container 내부)

```bash
cd /app
python3 manage.py makemigrations accounts
python3 manage.py migrate accounts
python3 manage.py migrate
python3 manage.py makemigrations shell
python3 manage.py makemigrations web_hosting
python3 manage.py makemigrations boards
python3 manage.py migrate
```

### 6. Superuser 생성

```bash
python3 manage.py createsuperuser
```

### 7. Server 실행

```bash
python3 manage.py runserver 0.0.0.0:8000 &
```
