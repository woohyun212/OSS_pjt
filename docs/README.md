# Method	Endpoint	설명
## POST	/click	UUID + 누적 클릭 수 전송
  - i: USER_UUID, click_count
  - o: "ok"
  
## GET	/inventory	사용자 인벤토리 이미지 리스트
  - i: USER_UUID
  - o:

## POST	/image/unlock	새 이미지 획득 등록
  - i: USER_UUID
  - o:
  
## POST	/gen-image	Gemini + Nebius 통한 이미지 생성 요청 (선택적)
  - i:
  - o: 
    
## GET	/world-records	사용자 인벤토리 이미지 리스트
  - i: 
  - o: TOP 10 records
