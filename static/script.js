// === 설정 ===
const CLICK_SEND_INTERVAL_MS = 5000; // 서버 전송 주기
const RARE_DROP_CHANCE = 0.01; // 1% 확률로 이미지 획득
const API_PREFIX = "/api/v1";


// === DOM ===
const clickImage = document.getElementById("click-image");
const clickCountDisplay = document.getElementById("click-count");
const toast = document.getElementById("toast");

// === 상태 ===
let clickCount = clickCountDisplay.textContent;
let clickDelta = 0;
let uuid = getOrCreateUUID();
let nickname = document.getElementById("nickname").innerText;

function loadRanking() {
  fetch(`${API_PREFIX}/world-records`)
    .then(res => res.json())
    .then(rankings => {
      const rankBox = document.getElementById("rank-box");
      rankBox.innerHTML = "<h3>🏆 TOP 5</h3><hr style='margin: 0.5rem 0;'>";
      rankings.forEach((user, index) => {
        const item = document.createElement("div");
        item.className = "rank-item";
        item.innerHTML = `${index + 1}. ${user.nickname} <span>${user.click_count.toLocaleString()} 클릭</span>`;
        rankBox.appendChild(item);
        });
        rankBox.appendChild(document.createElement("hr", "style='margin: 0.5rem 0;"));
        const item = document.createElement("div");
        item.className = "rank-item";
        item.innerHTML = `${nickname} <span>${clickCount.toLocaleString()} 클릭</span>`;
        rankBox.appendChild(item);
    })
    .catch(err => {
      console.error("랭킹 불러오기 실패:", err);
    });
}


// === 초기화 ===
document.addEventListener("DOMContentLoaded", () => {
  clickImage.addEventListener("click", handleClick);
  loadRanking();
  setInterval(sendClicksToServer, CLICK_SEND_INTERVAL_MS);
  setInterval(loadRanking, CLICK_SEND_INTERVAL_MS); // 랭킹 주기적으로 갱신
});

// === UUID 처리 ===
function getOrCreateUUID() {
    const key = "user_uuid";
    const match = document.cookie.match(new RegExp("(^| )" + key + "=([^;]+)"));
    
    if (match) {
        return match[2];  // 이미 존재하면 그대로 사용
    } else {
        const id = crypto.randomUUID();

        // 쿠키 저장
        document.cookie = `${key}=${id}; path=/; max-age=31536000`; // 1년

        // ✅ 백엔드에 닉네임 생성 요청 (비동기)
        fetch("/api/v1/init-user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(res => {
            if (!res.ok) {
                throw new Error("초기 사용자 생성 실패");
            }
            return res.json();
        })
        .then(data => {
            console.log("닉네임 생성 완료:", data.nickname);
            nickname = data.nickname;
        })
        .catch(err => {
            console.error("init-user 요청 오류:", err);
        });

        return id;
    }
}


// === 클릭 처리 ===
function handleClick() {
    clickCount++;
    clickDelta++;
    clickCountDisplay.textContent = clickCount.toLocaleString();

    // 희귀 이미지 획득 처리
    if (Math.random() < RARE_DROP_CHANCE) {
        unlockNewImage();
    }

    // 클릭 애니메이션 또는 효과음 추가 가능
}

// === 서버로 클릭 수 전송 ===
function sendClicksToServer() {
    if (clickDelta === 0) return;

    fetch(`${API_PREFIX}/click`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            uuid: uuid,
            delta: clickDelta
        })
    }).catch(err => {
        console.error("클릭 전송 실패:", err);
    });

    clickDelta = 0;
}

// === 이미지 획득 시 처리 ===
function unlockNewImage() {
    showToast("🎉 새로운 브레인롯 이미지 획득!");

    fetch(`${API_PREFIX}/image/unlock`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({uuid: uuid})
    })
        .then(res => res.json())
        .then(imageResponse => {
            const imageUrl = `${API_PREFIX}/image/` + imageResponse['new_image_id'];
            addImageToInventory(imageUrl);
        })
        .catch(err => {
            console.error("이미지 획득 전송 실패:", err);
        });
}

function addImageToInventory(imageUrl) {
    const slotCount = inventoryList.children.length;
    if (slotCount >= 8) return; // 8칸 초과 방지

    const slot = document.createElement("div");
    slot.classList.add("inventory-slot");

    const img = document.createElement("img");
    img.src = imageUrl;
    img.alt = "획득한 이미지";
    slot.appendChild(img);

    // 클릭하면 메인 클릭 이미지로 설정
    slot.addEventListener("click", () => {
        clickImage.src = imageUrl;
    });

    inventoryList.appendChild(slot);
}


// === 토스트 메시지 표시 ===
function showToast(message) {
    toast.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}

const inventoryDrawer = document.getElementById("inventory-drawer");
const inventoryList = document.getElementById("inventory-list");
const inventoryBtn = document.getElementById("inventory-btn");
const closeInventoryBtn = document.getElementById("close-inventory");

inventoryBtn.addEventListener("click", () => {
    fetch(`${API_PREFIX}/inventory`)
        .then(res => res.json())
        .then(images => {
            images = images['inventory'];
            inventoryList.innerHTML = "";

            const totalSlots = images.length;
            for (let i = 0; i < totalSlots; i++) {
                const slot = document.createElement("div");
                slot.classList.add("inventory-slot");
                console.log(`이미지 ${i + 1}:`, images[i]);
                if (images[i]) {
                    const imageId = images[i];
                    fetch(`${API_PREFIX}/image/${imageId}`)
                        .then(res => res.json())
                        .then(data => {
                            const b64 = data['b64_json'];

                            const img = document.createElement("img");
                            img.src = `data:image/png;base64,${b64}`;
                            img.alt = `획득한 이미지 ${i + 1}`;
                            slot.appendChild(img);

                            slot.addEventListener("click", () => {
                                clickImage.src = `data:image/png;base64,${b64}`;
                            });
                        })
                        .catch(err => {
                            console.error("이미지 로딩 실패:", err);
                        });
                } else {
                    slot.textContent = "빈칸";
                    slot.style.color = "#aaa";
                    slot.style.fontSize = "0.8rem";
                }

                inventoryList.appendChild(slot);
            }

            inventoryDrawer.classList.add("active");
        })
        .catch(err => {
            console.error("인벤토리 불러오기 실패:", err);
        });
});

inventoryBtn.addEventListener("click", () => {
    inventoryDrawer.classList.add("active");
});

closeInventoryBtn.addEventListener("click", () => {
    inventoryDrawer.classList.remove("active");
});