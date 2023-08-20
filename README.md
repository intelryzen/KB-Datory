<<<<<<< HEAD
# Future Finance A.I. Challenge

## 백엔드 프레임워크: FASTAPI
Github: https://github.com/intelryzen/KB-Datory

## 프론트엔드 프레임워크: FLUTTER
Github: https://github.com/intelryzen/KB-Datory-Front

## DB: MYSQL

### 클라인언트 작동 OS : Android, iOS

### 테스트 환경: iOS 
### 특징
iOS는 통화 중 음성 녹음이 불가하므로, 실제 전화 앱과 유사하게 UI를 구성하여 전화하는 상황을 가정하였습니다.
실제 통화앱이 아닐 뿐 녹음은 정상적으로 진행되며 모든 기능들은 완벽히 잘 작동하고 있습니다.

### 주요 기능
1. 통화를 받을 때 15초마다 서버(localhost)에 음성 파일을 보내고 보이스피싱 확률을 실시간으로 받아옵니다.
2. 보이스피싱으로 인지되면 서버 DB에 자동으로 해당 번호가 스팸으로 등록되어, 타 사용자에게 똑같은 번호로 전화가 오면 전화를 받기 전, <span style="color:yellow">"보이스피싱 #회 신고 접수"</span> 와 같은 문구가 표시됩니다.

### 앱 서비스 작동 사진
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/9d6a8061-1710-42d5-826c-11168adf6f8a" width="400" height="900"/>
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/f5de2998-eaf4-4ed1-90be-dce8233bc8a1" width="400" height="900"/>
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/40e960aa-e822-4a7d-8f97-dc4834862355" width="400" height="900"/>
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/ada8096a-3d1a-4360-b49f-9434ffc41bf3" width="400" height="900"/>

### 실행 전 사전 작업

1. private.py 파일 생성 필요

private.py:

    class Private:
        MYSQL_USER = "your_name"
        MYSQL_PW = "your_password"

2. mysql 서버 시작
"KB_AI" DB 생성 필요    
=======
# Future Finance A.I. Challenge ( KBeep 팀)
# 팀원: 신백록, 우승식, 김종해
<br/>
  
## 백엔드 프레임워크: Fastapi, Mysql
Github: https://github.com/intelryzen/KB-Datory
<br/>
  
## 프론트엔드 프레임워크: Flutter
Github: https://github.com/intelryzen/KB-Datory-Front
<br/>
  
### 클라인언트 OS : Android, iOS
### 실제 테스트 환경: iOS 시뮬레이터
<br/>
  
### 특징
iOS는 통화 중 음성 녹음이 불가하므로, 실제 전화 앱과 유사하게 UI를 구성하여 전화하는 상황을 가정하였습니다.
실제 통화앱이 아닐 뿐 녹음과 보이스피싱 탐지는 정상적으로 진행되며 세부 기능이 잘 작동합니다.
<br/>
  
### 주요 기능
1. 통화 수신(상황 1)이 되면 해당 번호가 보이스피싱 의심 번호인지 자체 서버 DB 에서 번호를 조회를 합니다.
2. 통화를 받을 때(상황 2) 3초마다 서버(localhost)에 음성 파일을 보내고 보이스피싱 확률을 거의 실시간으로 받아옵니다.
3. AI 모델이 보이스피싱으로 인지되면 서버 DB에 해당 번호가 자동 등록되어, 타 사용자에게 똑같은 번호로 전화가 오면, 전화를 받기 전, <span style="color:yellow">"보이스피싱 #회 신고 접수"</span> 와 같은 문구가 화면에 표시됩니다.
<br/>
  
### 서비스 작동 사진
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/9833fd5e-9051-4589-ba8d-e2331184a123" width="400" height="900"/>
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/99e70bfd-4e79-41ad-b4db-1342a281b0c9" width="400" height="900"/>
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/241b0e97-9579-4f90-8471-f5e9f0da4f1c" width="400" height="900"/>
<img src="https://github.com/intelryzen/KB-Datory/assets/66426612/91f22444-1c78-4092-aba4-bfc5e820be8b" width="400" height="900"/>
<br/>
  
### 파일 실행 전 사전 작업
1. 구글 드라이브에 업로드된 AI 모델 다운로드 후 업로드
2. private.py 파일 생성 (아래는 예시)

private.py:

    class Private:
        MYSQL_USER = "your_name"
        MYSQL_PW = "your_password"
        
3. mysql 서버 시작
"KB_AI" DB 생성 작업 필요    
>>>>>>> b09bd02b29651aea70641a11652006481b5c5066
