# Future Finance A.I. Challenge

## 프론트엔드 프레임워크: FLUTTER
## 백엔드 프레임워크: FASTAPI
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
![IMG_5395](https://github.com/intelryzen/KB-Datory/assets/66426612/9d6a8061-1710-42d5-826c-11168adf6f8a){: width="100" height="100"}
![IMG_5392](https://github.com/intelryzen/KB-Datory/assets/66426612/f5de2998-eaf4-4ed1-90be-dce8233bc8a1){: width="80" height="80"}
![IMG_5394](https://github.com/intelryzen/KB-Datory/assets/66426612/40e960aa-e822-4a7d-8f97-dc4834862355)
![IMG_5393](https://github.com/intelryzen/KB-Datory/assets/66426612/ada8096a-3d1a-4360-b49f-9434ffc41bf3)

### 실행 전 사전 작업

1. private.py 파일 생성 필요

private.py:

    class Private:
        MYSQL_USER = "your_name"
        MYSQL_PW = "your_password"

2. mysql 서버 시작
"KB_AI" DB 생성 필요    
