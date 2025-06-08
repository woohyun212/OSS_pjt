// === 설정 ===
const CLICK_SEND_INTERVAL_MS = 5000; // 서버 전송 주기
const RARE_DROP_CHANCE = 0.01; // 1% 확률로 이미지 획득

// === 상태 ===
let clickCount = 0;
let clickDelta = 0;
let uuid = getOrCreateUUID();

// === DOM ===
const clickImage = document.getElementById("click-image");
const clickCountDisplay = document.getElementById("click-count");
const toast = document.getElementById("toast");

// === 초기화 ===
document.addEventListener("DOMContentLoaded", () => {
  clickImage.addEventListener("click", handleClick);
  setInterval(sendClicksToServer, CLICK_SEND_INTERVAL_MS);
});

// === UUID 처리 ===
function getOrCreateUUID() {
  const key = "brainrot_uuid";
  let id = localStorage.getItem(key);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(key, id);
  }
  return id;
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

  fetch("/click", {
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

  fetch("/image/unlock", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ uuid: uuid })
  }).catch(err => {
    console.error("이미지 획득 전송 실패:", err);
  });
}

// === 토스트 메시지 표시 ===
function showToast(message) {
  toast.textContent = message;
  toast.classList.remove("hidden");
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}