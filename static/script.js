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
  })
  .then(res => res.json())
  .then(imageUrl => {
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
  fetch(`/image/list?uuid=${uuid}`)
    .then(res => res.json())
    .then(images => {
      inventoryList.innerHTML = "";

      const totalSlots = 8;
      for (let i = 0; i < totalSlots; i++) {
        const slot = document.createElement("div");
        slot.classList.add("inventory-slot");

        if (images[i]) {
          const img = document.createElement("img");
          img.src = images[i];
          img.alt = `획득한 이미지 ${i + 1}`;
          slot.appendChild(img);

          // 슬롯 클릭 시 클릭 이미지로 설정
          slot.addEventListener("click", () => {
            clickImage.src = images[i];
          });
        } else {
          // 빈 슬롯 텍스트
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