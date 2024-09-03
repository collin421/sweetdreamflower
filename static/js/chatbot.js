const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".chat-close-btn");

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p>${message}</p>` : `<span class="material-symbols-outlined">smart_toy</span><p>${message}</p>`;
    chatLi.innerHTML = chatContent;
    return chatLi;
}

const generateResponse = (userMessage, thinkingLi) => {
    const API_URL = "/chat"; // Flask 서버의 URL로 수정해야 합니다.

    // POST 요청을 위한 옵션 설정
    const requestOptions = {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    }

    // Flask 서버로 POST 요청 보내기
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        // "Thinking..." 메시지 제거
        chatbox.removeChild(thinkingLi);
        // 응답으로 받은 메시지로 채팅 LI 생성 및 추가
        const incomingChatLi = createChatLi(data.response, "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }).catch((error) => {
        console.error('Error:', error);
        // "Thinking..." 메시지 제거
        chatbox.removeChild(thinkingLi);
        // 에러 메시지 추가
        const errorLi = createChatLi("Oops! Something went wrong. Please try again.", "incoming");
        chatbox.appendChild(errorLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    });
}

const handleChat = () => {
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;
    chatInput.value = "";

    // 사용자의 메시지를 채팅박스에 추가
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    // "Thinking..." 메시지 추가
    const thinkingLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(thinkingLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    // 서버에 메시지 전송 및 응답 처리, "Thinking..." 메시지 제거 포함
    generateResponse(userMessage, thinkingLi);
}

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault(); // 기본 이벤트 방지
        handleChat(); // 채팅 처리 함수 호출
    }
});

sendChatBtn.addEventListener("click", handleChat);
chatbotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
