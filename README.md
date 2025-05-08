# 🎙 AI Voice Assistant with Language Support

A sleek, modern, and multilingual AI-powered voice assistant built with Python and [Google Gemini](https://ai.google.dev). Communicate via voice or text in multiple languages with real-time translation, smart responses, and a beautiful dark/light themed UI powered by **CustomTkinter**.

---

## 🖥️ UI & UX Highlights

- 🎤 **Voice-first interface** with fallback to text
- 🌍 **Multilingual support** (English, Tamil, Malayalam, Telugu, Hindi, Arabic, French)
- 🌓 **Light/Dark mode toggle**
- 💬 **Chat bubble layout** for natural conversations
- 🔊 **Real-time text-to-speech** responses
- ⚡ **Non-blocking, responsive UI** with threading
- 📱 Modern feel, compact layout, user-friendly icons

---

## 📸 Screenshots

> *(Add your own images in a `/screenshots` folder and link them here)*

| Light Mode                           | Dark Mode                          |
|--------------------------------------|------------------------------------|
| ![Light Mode](screenshots/light.png) | ![Dark Mode](screenshots/dark.png) |

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
```

### 2️⃣ Set up your environment

```bash
python -m venv venv
# Activate the virtual environment:
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add your Google Gemini API key

Edit the Python script to set your API key:

```python
API_KEY = "your_actual_api_key_here"
```

Get a free API key from [Google AI Studio](https://ai.google.dev).

---

## 💡 Usage

Run the application:

```bash
python main.py
```

Once launched:

- **Choose input/output language.**
- **Use 🎤 to speak or ⌨️ to type.**
- **AI replies will be spoken and shown as chat bubbles.**
- **Toggle 🌓 theme anytime.**
- **Switch input and output languages using dropdown menus.**

---

## 🌐 Supported Languages

- English 🇺🇸
- Tamil 🇮🇳
- Malayalam 🇮🇳
- Telugu 🇮🇳
- Hindi 🇮🇳
- Arabic 🇸🇦
- French 🇫🇷

---

## ⚙️ Tech Stack

| Purpose           | Library               |
|-------------------|-----------------------|
| GUI Framework     | CustomTkinter         |
| AI Model          | google-generativeai   |
| Voice Recognition | speechrecognition     |
| Text-to-Speech    | pyttsx3               |
| Translation       | googletrans==4.0.0rc1 |

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
