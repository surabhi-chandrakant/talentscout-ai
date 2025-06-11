# 🤖 TalentScout - AI Hiring Assistant

A sophisticated AI-powered hiring assistant built with Streamlit that streamlines the recruitment process through intelligent candidate screening and technical assessment.

## 🌟 Features

- **Automated Candidate Screening**: Collects essential candidate information systematically
- **Dynamic Technical Assessment**: Generates relevant technical questions based on candidate's tech stack
- **Interactive Chat Interface**: User-friendly conversational experience
- **Real-time Progress Tracking**: Visual progress indicators for both candidate and recruiter
- **Data Export Functionality**: Export candidate data and responses in JSON format
- **Responsive Design**: Works seamlessly across different screen sizes
- **Input Validation**: Ensures data quality with email and phone number validation

## 🚀 Live Demo

Try the application live on Hugging Face Spaces: [TalentScout AI Assistant](https://huggingface.co/spaces/YOUR_USERNAME/talentscout-ai)

## 📋 How It Works

The application follows a structured screening process:

1. **Welcome & Introduction**: Introduces the AI assistant and process
2. **Personal Information Collection**: 
   - Full name
   - Email address (with validation)
   - Phone number (with validation)
   - Years of experience
   - Desired positions
   - Current location
3. **Technical Profile**: Tech stack and expertise areas
4. **Technical Assessment**: Dynamic questions based on provided tech stack
5. **Completion**: Summary and next steps

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Language**: Python 3.8+
- **Data Processing**: Built-in Python libraries (json, re, datetime)
- **UI/UX**: Custom CSS styling with Streamlit components

## 🏗️ Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/surabhi-chandrakant/talentscout-ai.git
   cd talentscout-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

### Hugging Face Deployment

1. **Fork/Upload to GitHub**
2. **Connect to Hugging Face Spaces**
3. **Select Streamlit as the framework**
4. **Deploy automatically**

## 📁 Project Structure

```
talentscout-ai/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── DOCUMENTATION.md      # Detailed code documentation
└── .gitignore           # Git ignore file
```

## 🎯 Key Components

### CandidateInfo Class
- Dataclass for storing candidate information
- Includes validation and structured data management

### HiringAssistant Class
- Main application logic
- Conversation flow management
- Technical question generation
- Input validation and processing

### Conversation Stages
1. Greeting (0)
2. Name Collection (1)
3. Email Collection (2)
4. Phone Collection (3)
5. Experience Collection (4)
6. Position Collection (5)
7. Location Collection (6)
8. Tech Stack Collection (7)
9. Technical Questions (8)
10. Completion (9)

## 🔧 Configuration

The application includes several configurable elements:

- **Tech Categories**: Predefined technology categories for question generation
- **Question Templates**: Customizable technical questions for different technologies
- **Validation Rules**: Email and phone number validation patterns
- **UI Styling**: Custom CSS for enhanced user experience

## 📊 Supported Technologies

The AI assistant can generate technical questions for:

- **Programming Languages**: Python, Java, JavaScript, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin
- **Web Frameworks**: Django, Flask, FastAPI, React, Angular, Vue.js, Node.js, Express, Spring, Laravel
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, SQLite, Oracle, Cassandra, Elasticsearch
- **Cloud Platforms**: AWS, Azure, GCP, Docker, Kubernetes, Terraform
- **Data Science**: Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Matplotlib, Seaborn
- **Mobile**: React Native, Flutter, Android, iOS, Xamarin

## 🎨 UI Features

- **Gradient Header**: Eye-catching header with company branding
- **Sidebar Information**: Real-time candidate data display
- **Progress Tracking**: Visual progress bar and stage indicators
- **Chat Interface**: Conversational UI with distinct message styling
- **Responsive Design**: Adapts to different screen sizes

## 📤 Data Export

The application provides data export functionality:
- Candidate information summary
- Technical Q&A responses
- Session metadata
- JSON format for easy integration

## 🚦 Usage Guidelines

1. **Start Session**: Begin with the welcome message
2. **Follow Prompts**: Answer each question as prompted
3. **Technical Questions**: Provide detailed answers for technical assessment
4. **Review Summary**: Check the completion summary
5. **Export Data**: Download session data if needed

## 🔒 Data Privacy

- No data is stored permanently on servers
- Session data is cleared after completion
- Export functionality allows local data storage
- Follows best practices for data handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by modern recruitment automation needs
- Designed for seamless candidate experience

## 📞 Support

For support, please create an issue in the GitHub repository or contact the development team.

---

**TalentScout AI Hiring Assistant** - Streamlining recruitment through intelligent automation 🚀
