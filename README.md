```markdown
# chat-LLM

`chat-LLM` 是一个实现语音输入与语音输出交互的本地大语言模型（LLM）应用程序。它借助语音识别技术将用户的语音转换为文本，再利用本地大语言模型生成回复，并通过语音合成技术将回复以语音形式输出，实现音频到音频的交互。

## 功能特点
- **自动语音识别**：利用 `faster_whisper` 模型实时识别用户的语音输入。
- **本地大语言模型交互**：与本地的 `Ollama` 模型（如 `qwen2.5:latest`）进行通信，获取文本回复。
- **语音合成**：使用 `MeloTTS_ONNX` 模型将模型的回复转换为语音输出。
- **聊天历史记录**：记录用户与模型的对话历史，并在界面上(`streamlit`)显示。

## 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/your-repo/chat-LLM.git
cd chat-LLM
```

### 2. 创建并激活虚拟环境（可选但推荐）
```bash
python -m venv venv
source venv/bin/activate  # 对于 Windows 用户，使用 `venv\Scripts\activate`
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 下载模型
确保你已经下载了所需的模型，并将其放置在相应的目录中：
- `faster whisper` 模型：请下载后将如`models--Systran--faster-whisper-small`放置到 `./models/` 目录下。
- `MeloTTS_ONNX` 模型：将模型文件放置在 `./models/seasonstudio/melotts_zh_mix_en_onnx/` 目录。

### 推荐下载地址（不翻墙）
- https://hf-mirror.com/Systran/faster-whisper-small
- https://www.modelscope.cn/models/seasonstudio/melotts_zh_mix_en_onnx/summary

## 使用方法

### 1. 启动 `Ollama` 服务
确保你的本地 `Ollama` 服务已经启动，并且你所选择的模型（如 `qwen2.5:latest`）已经可用。

### 2. 运行应用程序
```bash
streamlit run main.py
```

### 3. 开始对话
- 打开浏览器，访问 `http://localhost:8501`。
- 当看到提示 “请说吧...” 时，说出你的问题。
- 应用程序会自动识别你的语音，将其转换为文本，发送给 `Ollama` 模型，并将模型的回复以语音形式播放出来。

## 项目结构
```
chat-LLM/
├── .gitignore           # Git 忽略文件配置
├── main.py              # 主程序文件
├── requirements.txt     # 项目依赖文件
├── README.md            # 项目说明文档
├── models/              # 模型文件存放目录
│   └── models--Systran--faster-whisper-small
|       └── blobs
|       └── refs
|       └── snapshots       
|   └── seasonstudio/
│       └── melotts_zh_mix_en_onnx/
│           └── ...
└── temp/                # 临时文件存放目录
    └── temp_audio.wav
```

## 配置说明
在 `main.py` 文件中，你可以根据需要修改以下配置：
- `WHISPER_MODEL_NAME`：选择不同大小的 `Whisper` 模型（如 `tiny`, `base`, `small`, `medium`, `large`）。
- `WHISPER_DEVICE`：指定模型运行的设备（`cpu` 或 `cuda`）。
- `OLLAMA_MODEL_NAME`：选择本地 `Ollama` 服务中可用的模型。

## 注意事项
- 确保你的系统具备音频输入和输出设备，以便正常使用语音识别和语音合成功能。
- 在使用过程中，如果遇到与 `Ollama` 通信的错误，请检查 `Ollama` 服务是否正常运行。

## 贡献
如果你对该项目有任何改进建议或发现了 bug，请随时提交 `issue` 或 `pull request`。

## 许可证
本项目采用 [许可证名称] 许可证，详情请参阅 `LICENSE` 文件。

## 感谢
 - 豆包
 - TRAE
 - 不熬夜的我
```

