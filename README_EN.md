# The Fifth Season 🌈

[简体中文](README.md) | **English**

A creative application for exploring emotional spectrum and reconstructing memory fragments

## 📖 Project Overview

"The Fifth Season" is an emotion analysis and story generation application developed with Python and Streamlit. It can deeply analyze complex emotions in text and weave scattered memory fragments into coherent stories, providing users with a unique platform for emotional exploration and creative expression.

### 🎯 Core Features

#### 🌈 Emotional Spectrum Analyzer
- **Multi-dimensional Emotion Recognition**: Beyond simple "positive" or "negative", it identifies nuanced emotions like "longing", "loss", "anticipation", "helplessness", etc.
- **Weight Calculation**: Assigns weights to each emotion to show emotional intensity distribution
- **Visualization**: Provides radar charts, bar charts, pie charts, and word clouds for visualization
- **Emotion Summary**: Automatically generates textual summaries of emotion analysis

#### 📖 Memory Fragment Story Generator
- **Intelligent Story Creation**: Based on Pollinations API, weaves scattered memory keywords into coherent stories
- **Multiple Styles**: Supports novel style, movie scenes, poetic prose, diary style, and more
- **Emotional Tone Control**: Can specify the emotional tone of stories, such as warm, melancholy, longing, etc.
- **Multi-version Generation**: Supports generating multiple versions of stories with the same theme

## 🛠️ Tech Stack

- **Python 3.12+**: Main development language
- **Streamlit**: Web interface framework
- **uv**: Modern Python package manager
- **jieba**: Chinese word segmentation
- **TextBlob**: English sentiment analysis
- **Plotly**: Interactive charts
- **WordCloud**: Word cloud generation
- **Pollinations API**: AI text generation

## 🚀 Quick Start

### Requirements
- Python 3.12 or higher
- uv package manager

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/zym9863/The-Fifth-Season.git
cd The\ Fifth\ Season
```

2. **Install dependencies**
```bash
uv sync
```

3. **Launch the application**
```bash
uv run streamlit run main.py
```

4. **Access the application**
Open your browser and visit `http://localhost:8501`

### Test functionality
```bash
uv run python test_app.py
```

## 📁 Project Structure

```
The Fifth Season/
├── main.py                    # Application entry file
├── test_app.py               # Function test script
├── pyproject.toml            # Project configuration file
├── README.md                 # Project documentation (Chinese)
├── README_EN.md              # Project documentation (English)
├── config/
│   └── settings.py           # Configuration file
├── src/
│   ├── __init__.py
│   ├── emotion_analyzer/     # Emotion analysis module
│   │   ├── __init__.py
│   │   ├── analyzer.py       # Emotion analysis core logic
│   │   └── visualizer.py     # Emotion visualization components
│   ├── story_generator/      # Story generation module
│   │   ├── __init__.py
│   │   └── generator.py      # Story generation core logic
│   ├── ui/                   # User interface module
│   │   ├── __init__.py
│   │   └── main_app.py       # Streamlit main interface
│   └── utils/                # Utility functions module
│       ├── __init__.py
│       └── helpers.py        # Helper functions
```

## 🎨 User Guide

### Emotional Spectrum Analysis

1. **Input Text**: Enter the text to be analyzed in the text box
2. **Start Analysis**: Click the "Start Analysis" button
3. **View Results**:
   - Emotion Summary: Textual description of analysis results
   - Visualization Charts: Radar chart, bar chart, pie chart
   - Emotion Word Cloud: Visual display of keywords
   - Detailed Information: Weight data and statistics

### Memory Fragment Story Generation

1. **Input Memory Fragments**:
   - Enter in the text box, separated by commas or newlines
   - Or use tag input method to add one by one
2. **Set Parameters**:
   - Choose story style (novel style, movie scenes, etc.)
   - Choose emotional tone (warm, melancholy, longing, etc.)
   - Choose story length (short, medium, long)
   - Add custom requirements (optional)
3. **Generate Story**: Click the "Generate Story" button
4. **View Results**: Read the generated story and related information

## 🔧 Configuration

### Emotion Category Configuration
You can customize emotion categories and keywords in `config/settings.py`:

```python
EMOTION_CATEGORIES = {
    "longing": ["miss", "yearn", "pine", "crave", "long for"],
    "loss": ["disappointed", "dejected", "discouraged", "lonely", "melancholy"],
    # ... more emotion categories
}
```

### API Configuration
Pollinations API configuration:

```python
POLLINATIONS_API_URL = "https://text.pollinations.ai"
DEFAULT_MODEL = "openai"
DEFAULT_SEED = 42
```

## 🎯 Special Features

### 1. Multi-dimensional Emotion Analysis
- Supports 8 basic emotion types
- Based on keyword matching and TextBlob sentiment analysis
- Calculates emotional diversity index
- Generates emotional weight distribution

### 2. Intelligent Story Generation
- Based on advanced AI models
- Supports multiple creative styles
- Controllable emotional tone
- Supports custom creative requirements

### 3. Rich Visualization
- Emotion Radar Chart: Shows emotion distribution
- Bar Chart: Displays emotion intensity ranking
- Pie Chart: Shows emotion proportions
- Word Cloud: Visualizes emotional keywords

### 4. User-friendly Interface
- Responsive design
- Real-time interaction
- History saving
- Detailed analysis information

## 🔍 Examples

### Emotion Analysis Example
**Input Text**: "Bright and dark, scattered fragments, overlapping memory scenes, blurring the past. Drops and dots, circles and rounds, like a broken thread."

**Analysis Results**:
- Dominant emotion: Longing (0.45)
- Secondary emotions: Loss (0.30), Calm (0.25)
- Emotional diversity: 0.68

### Story Generation Example
**Memory Fragments**: Sunset, old locust tree, cicada sounds, grandma's rocking chair, sweetness of popsicles

**Generated Story**: A warm story about childhood summer memories...

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve the project!

### Development Environment Setup
1. Fork the project
2. Create a feature branch
3. Install development dependencies: `uv sync --dev`
4. Run tests: `uv run python test_app.py`
5. Submit changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Excellent web application framework
- [Pollinations](https://pollinations.ai/) - Powerful AI text generation API
- [jieba](https://github.com/fxsjy/jieba) - Chinese word segmentation tool
- [Plotly](https://plotly.com/) - Interactive chart library

## 📞 Contact

If you have questions or suggestions, please contact us through:
- Submit an Issue
- Send an email
- Project discussion area

---

**The Fifth Season** - Explore the infinite possibilities of emotions 🌈✨
