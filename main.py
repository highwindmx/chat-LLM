import os
import wave
import streamlit as st
from streamlit_chat import message
import speech_recognition as sr
from faster_whisper import WhisperModel
import ollama
from melo_onnx import MeloTTS_ONNX
import sounddevice as sd

class VoiceChatBot:
    # 定义常量
    WHISPER_MODEL_NAME = 'small'  # 'tiny', 'base', 'small', 'medium', 'large' 参考fastwhisper
    WHISPER_DEVICE = 'auto'  # 'cpu' or 'cuda'
    WHISPER_DOWNLOAD_ROOT = "./models/"
    TTS_MODEL_PATH = "./models/seasonstudio/melotts_zh_mix_en_onnx/"
    OLLAMA_MODEL_NAME = "qwen2.5:latest"  # 根据本地Ollama list 选择
    TEMP_AUDIO_FILE = "./temp/temp_audio.wav"

    def __init__(self):
        # 初始化语音识别器
        self.r = sr.Recognizer()
        # 初始化聊天历史
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        # 自动加载语音识别模型
        self.load_whisper_model()
        # 创建一个占位符用于显示聊天内容
        self.chat_placeholder = st.empty()

    def load_whisper_model(self):
        # 显示模型正在加载的提示
        loading_message = st.info("语音识别模型正在加载，请稍候...")
        # 初始化 Whisper 模型
        self.whisper_model = WhisperModel(self.WHISPER_MODEL_NAME, device=self.WHISPER_DEVICE, local_files_only=False, download_root=self.WHISPER_DOWNLOAD_ROOT)
        # 加载完成后移除提示
        loading_message.empty()
        # 开始自动语音识别
        self.auto_recognize_speech()

    def auto_recognize_speech(self):
        with sr.Microphone() as source:
            with st.chat_message("assistant"):
                st.write("请说吧...")
            audio = self.r.listen(source)
        try:
            # 保存音频数据到临时文件
            with wave.open(self.TEMP_AUDIO_FILE, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                wf.writeframes(audio.get_wav_data())

            # 使用临时文件进行转录
            segments, info = self.whisper_model.transcribe(self.TEMP_AUDIO_FILE, beam_size=5)
            text = ''.join([segment.text for segment in segments])
            # 删除临时文件
            if os.path.exists(self.TEMP_AUDIO_FILE):
                os.remove(self.TEMP_AUDIO_FILE)

            if text:
                message(f"{text}", is_user=True, key=str(len(st.session_state.chat_history)))
                st.session_state.chat_history.append(("你", text))
                # 显示模型正在思考的提示
                thinking_msg = st.chat_message("assistant")
                thinking_msg.write(f"{self.OLLAMA_MODEL_NAME} 正在思考...")

                try:
                    # 发送消息到 Ollama
                    response = ollama.generate(self.OLLAMA_MODEL_NAME, text)
                    response_text = response["response"]

                    # 替换思考提示为实际回复
                    thinking_msg.empty()
                    st.session_state.chat_history.append(("Ollama", response_text))
                    # 立即显示 Ollama 的回复
                    message(response_text, is_user=False, key=str(len(st.session_state.chat_history) - 1))

                    # 语音合成 Ollama 的回复
                    self.speak(response_text)
                except Exception as e:
                    thinking_msg.empty()
                    st.session_state.chat_history.append(("Ollama", f"与 Ollama 通信时发生错误: {e}"))
                    message(f"与 Ollama 通信时发生错误: {e}", is_user=False, key=str(len(st.session_state.chat_history) - 1))

            # 更新聊天内容并滚动到最新消息
            self.update_chat()

            # 继续监听语音输入
            self.auto_recognize_speech()
        except Exception as e:
            st.write(f"识别错误: {e}")
            # 继续监听语音输入
            self.auto_recognize_speech()

    def play_audio(self, aud, spr):
        stream = sd.OutputStream(samplerate=spr, channels=1)
        with stream:
            stream.write(aud)

    def speak(self, text):
        # 显示正在进行语音合成的提示
        synthesizing_msg = st.chat_message("assistant")
        synthesizing_msg.write("正在进行语音合成，请稍候...")
        # 检查是否已经初始化了 TTS 模型，如果没有则进行初始化
        if not hasattr(self, 'tts'):
            self.tts = MeloTTS_ONNX(self.TTS_MODEL_PATH)
        audio = self.tts.speak(text, self.tts.speakers[0])
        sample_rate = self.tts.sample_rate
        synthesizing_msg.empty()
        synthesizing_msg.write("语音合成完成。")
        self.play_audio(audio, sample_rate)

    def update_chat(self):
        with self.chat_placeholder.container():
            # 显示聊天历史
            for i, (sender, msg) in enumerate(st.session_state.chat_history):
                is_user = sender == "你"
                message(msg, is_user=is_user, key=str(i))
            # 使用 JavaScript 滚动到最新消息
            st.markdown(
                """
                <script>
                    var element = document.getElementById('root');
                    if (element) {
                        element.scrollTop = element.scrollHeight;
                    }
                </script>
                """,
                unsafe_allow_html=True
            )

    def run(self):
        # 主界面
        st.title("语音聊天机器人")

        # 更新聊天内容并滚动到最新消息
        self.update_chat()

if __name__ == "__main__":
    bot = VoiceChatBot()
    bot.run()
