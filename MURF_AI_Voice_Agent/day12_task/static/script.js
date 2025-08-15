// Day 12: Revamped UI and consolidated chat logic
document.addEventListener('DOMContentLoaded', () => {
    const recordButton = document.getElementById('record-button');
    const statusBar = document.getElementById('status-bar');
    const statusText = document.getElementById('status-text');
    const chatHistory = document.getElementById('chat-history');
    const aiChatPlayer = document.getElementById('ai-chat-player');
    const fallbackPlayer = document.getElementById('fallback-player');

    let mediaRecorder;
    let audioChunks = [];
    let appState = 'idle'; // idle, recording, processing, speaking
    const SESSION_ID = Math.random().toString(36).slice(2, 10);

    const setState = (newState) => {
        appState = newState;
        updateUIForState(newState);
    };

    const updateUIForState = (state) => {
        recordButton.className = 'record-button'; // Reset classes
        const icon = recordButton.querySelector('i');

        switch (state) {
            case 'idle':
                statusText.textContent = 'Ready to listen';
                icon.className = 'fas fa-microphone';
                recordButton.disabled = false;
                break;
            case 'recording':
                statusText.textContent = 'Listening...';
                recordButton.classList.add('recording');
                icon.className = 'fas fa-stop';
                recordButton.disabled = false;
                break;
            case 'processing':
                statusText.textContent = 'Thinking...';
                recordButton.classList.add('processing');
                icon.className = 'fas fa-spinner';
                recordButton.disabled = true;
                break;
            case 'speaking':
                statusText.textContent = 'Speaking... (click mic to interrupt)';
                icon.className = 'fas fa-microphone';
                recordButton.disabled = false; // Allow barge-in
                break;
            case 'error':
                 statusText.textContent = 'An error occurred. Try again.';
                 icon.className = 'fas fa-exclamation-triangle';
                 recordButton.disabled = false;
                 break;
        }
    };

    const addMessageToHistory = (text, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        // Use the 'marked' library to convert Markdown to HTML
        const sanitizedHtml = marked.parse(text.replace(/^[\u200B\u200C\u200D\u200E\u200F\uFEFF]/,""));
        messageElement.innerHTML = sanitizedHtml;
        
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    // Stop and completely teardown any playing audio to avoid buffering/overlap
    const stopAllAudio = () => {
        try {
            if (aiChatPlayer) {
                try { aiChatPlayer.pause(); } catch(e) {}
                try { aiChatPlayer.currentTime = 0; } catch(e) {}
                try { aiChatPlayer.removeAttribute('src'); } catch(e) {}
                try { aiChatPlayer.load(); } catch(e) {}
            }

            if (fallbackPlayer) {
                try { fallbackPlayer.pause(); } catch(e) {}
                try { fallbackPlayer.currentTime = 0; } catch(e) {}
                try { fallbackPlayer.removeAttribute('src'); } catch(e) {}
                try { fallbackPlayer.load(); } catch(e) {}
            }
        } catch (err) {
            console.warn('Error stopping audio players:', err);
        }
    };

    const handleRecordButtonClick = () => {
        if (appState === 'idle' || appState === 'error') {
            startRecording();
        } else if (appState === 'recording') {
            stopRecording();
        } else if (appState === 'speaking') {
            // Barge-in: stop any playing audio and immediately start recording
            stopAllAudio();
            startRecording();
        }
    };

    const startRecording = async () => {
        // Ensure any playing audio is fully stopped before opening the mic
        stopAllAudio();
        // If an existing MediaRecorder is active, stop it first
        try {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
        } catch (e) {
            console.warn('Error stopping existing mediaRecorder before starting new one', e);
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) audioChunks.push(event.data);
            };

            mediaRecorder.onstop = handleRecordingStop;

            mediaRecorder.start();
            setState('recording');
        } catch (err) {
            console.error('Error accessing microphone:', err);
            addMessageToHistory('Could not access the microphone. Please check your browser permissions.', 'assistant');
            setState('error');
        }
    };

    const stopRecording = () => {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
    };

    const handleRecordingStop = async () => {
        setState('processing');
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.webm');

        try {
            const res = await fetch(`/agent/chat/${SESSION_ID}`, {
                method: 'POST',
                body: formData,
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error(data.error || 'Server error');
            }
            
            addMessageToHistory(data.transcript, 'user');
            addMessageToHistory(data.llm_text, 'assistant');

            aiChatPlayer.src = data.audio_url;
            aiChatPlayer.play();
            setState('speaking');

        } catch (err) {
            console.error('Error during chat processing:', err);
            addMessageToHistory(`Error: ${err.message}. Please try again.`, 'assistant');
            // Check if there's a fallback audio path and play it
            if (err.fallback_audio_path) {
                fallbackPlayer.src = err.fallback_audio_path;
                fallbackPlayer.play();
            }
            setState('error');
        }
    };

    aiChatPlayer.onended = () => {
        setState('idle');
    };
    
    fallbackPlayer.onended = () => {
        setState('idle');
    };

    aiChatPlayer.onerror = () => {
        addMessageToHistory('Error playing AI response.', 'assistant');
        setState('error');
    };

    recordButton.addEventListener('click', handleRecordButtonClick);
    
    // Initial state
    setState('idle');
});
