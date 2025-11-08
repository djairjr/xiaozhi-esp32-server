// DOM element
const connectButton = document.getElementById('connectButton');
const serverUrlInput = document.getElementById('serverUrl');
const connectionStatus = document.getElementById('connectionStatus');
const messageInput = document.getElementById('messageInput');
const sendTextButton = document.getElementById('sendTextButton');
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
// session_recording
const conversationDiv = document.getElementById('conversation');
const logContainer = document.getElementById('logContainer');
let visualizerCanvas = document.getElementById('audioVisualizer');

// ota is_the_connection_successful，modify_to_the_corresponding_style
export function otaStatusStyle (flan) {
    if(flan){
        document.getElementById('otaStatus').textContent = 'ota已连接';
        document.getElementById('otaStatus').style.color = 'green';
    }else{
        document.getElementById('otaStatus').textContent = 'ota未连接';
        document.getElementById('otaStatus').style.color = 'red';
    }
}

// ota is_the_connection_successful，modify_to_the_corresponding_style
export function getLogContainer (flan) {
    return  logContainer;
}

// update_opus_library_status_display
export function updateScriptStatus(message, type) {
    const statusElement = document.getElementById('scriptStatus');
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.className = `script-status ${type}`;
        statusElement.style.display = 'block';
        statusElement.style.width = 'auto';
    }
}

// add_message_to_conversation_record
export function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'server'}`;
    messageDiv.textContent = text;
    conversationDiv.appendChild(messageDiv);
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

