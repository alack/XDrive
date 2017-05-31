Require : 
Python 3.6.1
PyQt5 5.8.2

Install :
pip install pyqt5


--------------Bug list------------------------------
1. mydir 폴더 열때 에러 - 원인미상

2. drive_action_list = []
구글 추가 -> 구글 제거 -> 박스 추가 -> 박스 제거(에러)
QActionGroup으로 바꾸기

3. 공백 폴더 or 파일 처리

4. 폴더 더블클릭 시에 파일 이름 바꾸는 index가 이상한거 가리킴 -> 에러발생

---------------TODO----------------------------------
처음 root 폴더 로드 시 아이콘 표시 - Done.
드랍 업로드 - 파일이나 폴더 추가되면 리스트에도 추가 - Done.
파일 이름 레이블 붙이기 - Done.
파일 이름 레이블 색 수정 - #FFFFFF(default) -> (R,G,B,투명도):(0, 0, 0, 0) - Done.
파일 이름 레이블 수정가능하도록하기 -> 
 2. 파일 - Label 더블클릭 : 현재 이름 나오도록 하고 다른 값 입력시 수정되도록 - Done.


-------------기능필요---------------------------------
드랍 업로드 시 파일이 가장 처음 위치(0,0) 에 등록-> 보이는 것과 위치 다름. 수정필요.
  - self.model.add_piece(image, QPoint(0, 0)) 이거 문제인듯

파일 이름 레이블 수정가능하도록하기 -> 
 1. F2키 : UIComponent / DirectoryView / keyPressEvent에서 처리하기 - setData 불러오면 될듯
 3. 보이는 이름으로 파일 이름 수정하기(1 or 2 다음 subject)

폴더 추가할 때 이름 지정 필요 -> 파일 이름 레이블 수정의 다음 subject

폴더추가에 mkdir 붙이기 -> 폴더 추가 시에 이름 지정 다음 subject

드래그 아웃 저장

더블클릭 다운로드
다운로드 경로 지정

마우스 오른쪽 메뉴 추가 - 아름바꾸기, 다운로드, 삭제

아이콘/글자크기 조절 버튼 2개 추가

File icon 바꾸기 (QFileIconProvider) 시도
http://nullege.com/codes/show/src%40c%40a%40calibre-HEAD%40src%40calibre%40gui2%40__init__.py/581/PyQt4.Qt.QFileIconProvider.icon/python


-----------------참고---------------------------
http://doc.qt.io/qt-5/qt.html#ItemDataRole-enum
http://doc.qt.io/qt-5/qabstractlistmodel.html