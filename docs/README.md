## API 문서 (v1)

### POST /api/v1/init-user
> 사용자 초기화: 닉네임 부여
- i: (쿠키) user_uuid
- o: { "nickname": str }

### POST /api/v1/click
> UUID + 클릭 수 전송
- i: (쿠키) user_uuid, JSON { "delta": int }
- o: { "status": "ok" }

### GET /api/v1/inventory
> 현재 수집한 이미지 목록 조회
- i: (쿠키) user_uuid
- o: { "inventory": [ image_id, ... ] }

### POST /api/v1/image/unlock
> 새 이미지 잠금 해제 (10% 확률 새 이미지 지급)
- i: (쿠키) user_uuid
- o: { "new_image_id": str }

### GET /api/v1/image/<image_id>
> 특정 이미지 ID로 이미지 조회
- i: URL param image_id
- o: { "image_id": str, "name": str, "prompt": str, "b64_json": str }

### GET /api/v1/image/generate
> 캐시된 이미지 중 하나를 가져옴
- i: (없음)
- o: { "image_id": str, "name": str, "prompt": str, "b64_json": str }

### GET /api/v1/world-records
> 전체 유저 중 클릭 수 TOP10 조회
- i: (없음)
- o: [ { "user_uuid": str, "click_count": int }, ... ]
