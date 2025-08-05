# AI Interview Assistant 🤖

An intelligent screenshot analysis tool that automatically solves coding problems and technical questions using GPT-4 Vision API. Perfect for interview preparation, coding practice, and learning programming concepts.

## ✨ Features

- **🔍 Screenshot Analysis**: Capture any coding problem or technical question with a simple keyboard shortcut
- **🐍 Multi-Language Support**: Generate solutions in both Python and C++ with detailed explanations
- **🌐 Web Interface**: Beautiful web dashboard with LaTeX rendering and syntax highlighting
- **⚡ Real-time Processing**: Instant AI analysis with structured, professional responses
- **📚 Educational Focus**: Multiple solution approaches with complexity analysis and explanations
- **🔄 Universal Compatibility**: Works on macOS, Windows, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- OpenAI API key (GPT-4 Vision access required)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-interview-assistant.git
   cd ai-interview-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install openai pillow pyautogui pynput flask
   ```

3. **Configure API Key:**
   Edit the API key in both `ai_agent_python_gpt.py` and `ai_agent_cpp_gpt.py`:
   ```python
   API_KEY = 'your-openai-api-key-here'
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

## 🎯 Usage

### Basic Workflow

1. **Start the Application:**
   ```bash
   python run.py
   ```
   The web interface will be available at `http://localhost:5001`

2. **Capture Screenshot:**
   - Press `Cmd+Shift+7` (macOS) or `Ctrl+Shift+7` (Windows/Linux)
   - The screenshot will be automatically saved

3. **Choose Language:**
   - Press `Ctrl+Shift+P` for **Python** solutions
   - Press `Ctrl+Shift+C` for **C++** solutions

4. **View Results:**
   - Open `http://localhost:5001` in your browser
   - Results will appear automatically with professional formatting

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+7` | Capture screenshot (macOS) |
| `Ctrl+Shift+7` | Capture screenshot (Windows/Linux) |
| `Ctrl+Shift+P` | Generate Python solution |
| `Ctrl+Shift+C` | Generate C++ solution |

## 📋 What You Get

For each coding problem, the AI provides:

1. **📊 Problem Analysis** - Clear breakdown of requirements
2. **🔧 Solution Description** - High-level approach explanation
3. **💻 Code Implementation** - Clean, well-commented code
4. **🎯 Alternative Approach** - Different solution method
5. **📚 Detailed Explanations** - How and why each solution works
6. **⏱️ Complexity Analysis** - Time and space complexity breakdown

## 🏗️ Project Structure

```
ai-interview-assistant/
├── run.py                    # Universal startup script
├── scripts/
│   ├── main.py              # Main application controller
│   ├── web_server.py        # Flask web server & LaTeX processing
│   ├── ai_agent_python_gpt.py  # Python solution generator
│   ├── ai_agent_cpp_gpt.py     # C++ solution generator
│   └── screenshot.py        # Screenshot utilities
├── templates/
│   └── index.html          # Web interface template
├── screenshots/            # Generated screenshots
├── results.txt            # AI analysis results
└── README.md              # This file
```

## 🛠️ Technical Details

### Technologies Used

- **Backend**: Python, Flask
- **AI Processing**: OpenAI GPT-4 Vision API
- **Image Processing**: Pillow (PIL)
- **Screenshot Capture**: PyAutoGUI
- **Keyboard Monitoring**: pynput
- **Web Rendering**: HTML, CSS, JavaScript with MathJax
- **Code Highlighting**: Prism.js

### Key Components

1. **Screenshot Capture System**
   - Cross-platform keyboard listener
   - Automatic image optimization
   - Base64 encoding for API transmission

2. **AI Processing Pipeline**
   - Image analysis using GPT-4 Vision
   - Structured prompting for consistent results
   - Language-specific solution generation

3. **Web Interface**
   - LaTeX to HTML conversion
   - Mathematical expression rendering
   - Syntax-highlighted code blocks
   - Responsive design

## 🔧 Configuration

### API Settings

Edit the following files to customize AI behavior:

**`ai_agent_python_gpt.py` and `ai_agent_cpp_gpt.py`:**
```python
# Model configuration
model="gpt-4.1"           # AI model to use
temperature=0.2           # Response creativity (0-1)
max_tokens=2000          # Maximum response length
```

### Web Server Settings

**`web_server.py`:**
```python
# Server configuration
host='0.0.0.0'           # Listen on all interfaces
port=5001                # Web server port
debug=False              # Debug mode
```

## 🐛 Troubleshooting

### Common Issues

**1. Screenshot not capturing:**
- Ensure you have screen recording permissions
- Try running with administrator/sudo privileges
- Check if PyAutoGUI is working: `python -c "import pyautogui; pyautogui.screenshot()"`

**2. API errors:**
- Verify your OpenAI API key is valid
- Ensure you have GPT-4 Vision access
- Check your API usage limits

**3. Web interface not loading:**
- Confirm Flask is installed: `pip install flask`
- Check if port 5001 is available
- Look for template file in `templates/index.html`

**4. Import errors:**
- Install missing dependencies: `pip install -r requirements.txt`
- Ensure you're using Python 3.7+

### Debug Mode

Enable detailed logging by modifying `web_server.py`:
```python
log.setLevel(logging.DEBUG)  # Show all logs
app.run(debug=True)          # Enable Flask debug mode
```

## 📝 Example Output

### Input: Screenshot of LeetCode Problem
### Output:
```
🔍 PROBLEM ANALYSIS
Find the longest palindromic substring in a given string.

🛠️ SOLUTION DESCRIPTION (Common Approach)
Dynamic Programming approach with 2D table to store palindrome states...

💻 SOLUTION 1 (Common Approach)
def longestPalindrome(s):
    n = len(s)
    # Create DP table
    dp = [[False] * n for _ in range(n)]
    ...

🎯 ALTERNATIVE APPROACH
Expand Around Centers technique for O(n²) time with O(1) space...

📊 COMPLEXITY ANALYSIS
- Time Complexity: O(n²)
- Space Complexity: O(1)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the powerful GPT-4 Vision API
- The open-source community for the excellent Python libraries
- Interview preparation platforms for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/ai-interview-assistant/issues)
3. Create a new issue with detailed information

---

**⭐ Star this repository if it helped you ace your coding interviews!**

Made with ❤️ for the coding community