// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD-d1Iqeo9_KK_XPHIRXKy-_g9m_GUI5F8",
  authDomain: "caoop-d1eef.firebaseapp.com",
  projectId: "caoop-d1eef",
  storageBucket: "caoop-d1eef.firebasestorage.app",
  messagingSenderId: "1074780931759",
  appId: "1:1074780931759:web:d0f8be5ee1acc34926b65a",
  measurementId: "G-WLMWX6EL03"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// DOM elements
const chatWindow = document.getElementById("chat-window");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

// Send message
sendButton.addEventListener("click", () => {
  const message = messageInput.value.trim();
  if (message !== "") {
    db.collection("messages").add({
      text: message,
      timestamp: firebase.firestore.FieldValue.serverTimestamp(),
    });
    messageInput.value = "";
  }
});

// Display messages
db.collection("messages")
  .orderBy("timestamp")
  .onSnapshot((snapshot) => {
    chatWindow.innerHTML = "";
    snapshot.forEach((doc) => {
      const message = doc.data().text;
      const messageElement = document.createElement("div");
      messageElement.textContent = message;
      chatWindow.appendChild(messageElement);
    });
  });
