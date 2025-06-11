import streamlit as st
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import openai
from dataclasses import dataclass, asdict

# Configure the page
st.set_page_config(
    page_title="TalentScout - AI Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class CandidateInfo:
    """Data class to store candidate information"""
    full_name: str = ""
    email: str = ""
    phone: str = ""
    experience_years: str = ""
    desired_positions: str = ""
    current_location: str = ""
    tech_stack: str = ""
    session_start: str = ""

class HiringAssistant:
    """Main class for the Hiring Assistant chatbot"""
    
    def __init__(self):
        self.conversation_stages = {
            "greeting": 0,
            "name": 1,
            "email": 2,
            "phone": 3,
            "experience": 4,
            "position": 5,
            "location": 6,
            "tech_stack": 7,
            "technical_questions": 8,
            "completed": 9
        }
        
        # Tech stack categories for better question generation
        self.tech_categories = {
            "programming_languages": ["python", "java", "javascript", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin"],
            "web_frameworks": ["django", "flask", "fastapi", "react", "angular", "vue", "nodejs", "express", "spring", "laravel"],
            "databases": ["mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "cassandra", "elasticsearch"],
            "cloud_platforms": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform"],
            "data_science": ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "matplotlib", "seaborn"],
            "mobile": ["react native", "flutter", "android", "ios", "xamarin"]
        }
        
        # Conversation ending keywords
        self.exit_keywords = ["bye", "goodbye", "exit", "quit", "end", "stop", "thank you", "thanks"]
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "candidate_info" not in st.session_state:
            st.session_state.candidate_info = CandidateInfo(session_start=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        
        if "current_stage" not in st.session_state:
            st.session_state.current_stage = 0
        
        if "technical_questions" not in st.session_state:
            st.session_state.technical_questions = []
        
        if "current_question_index" not in st.session_state:
            st.session_state.current_question_index = 0
        
        if "conversation_ended" not in st.session_state:
            st.session_state.conversation_ended = False
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove spaces, dashes, and parentheses
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it contains only digits and optional + at the beginning
        pattern = r'^\+?[1-9]\d{9,14}$'
        return re.match(pattern, cleaned_phone) is not None
    
    def check_exit_intent(self, user_input: str) -> bool:
        """Check if user wants to end the conversation"""
        user_input_lower = user_input.lower().strip()
        return any(keyword in user_input_lower for keyword in self.exit_keywords)
    
    def generate_greeting(self) -> str:
        """Generate initial greeting message"""
        return """
        🤖 **Hello! Welcome to TalentScout's AI Hiring Assistant!**
        
        I'm here to help streamline your application process. I'll be gathering some basic information about you and then asking a few technical questions based on your expertise.
        
        This conversation will take about 5-10 minutes and will help us better understand your background and skills.
        
        Ready to get started? Please tell me your **full name**.
        
        *(You can type 'exit' or 'bye' at any time to end our conversation)*
        """
    
    def generate_technical_questions(self, tech_stack: str) -> List[str]:
        """Generate technical questions based on the candidate's tech stack"""
        questions = []
        tech_stack_lower = tech_stack.lower()
        
        # Split tech stack into individual technologies
        technologies = [tech.strip() for tech in re.split(r'[,;|\n]', tech_stack_lower)]
        
        question_templates = {
            "python": [
                "Explain the difference between list and tuple in Python and when you would use each.",
                "What are Python decorators and can you provide a simple example?",
                "How do you handle exceptions in Python? Explain try-except blocks.",
                "What is the difference between '==' and 'is' operators in Python?",
                "Explain list comprehensions in Python and provide an example.",
                "What are Python generators and when would you use them?"
            ],
            "r": [
                "What is the difference between data.frame and matrix in R?",
                "Explain the concept of vectorization in R with an example.",
                "How do you handle missing values (NA) in R?",
                "What are R packages and how do you install them?",
                "Explain the apply family of functions in R."
            ],
            "java": [
                "Explain the concept of Object-Oriented Programming in Java.",
                "What is the difference between ArrayList and LinkedList in Java?",
                "Explain the concept of inheritance and polymorphism in Java.",
                "What are Java interfaces and when would you use them?"
            ],
            "javascript": [
                "Explain the difference between 'var', 'let', and 'const' in JavaScript.",
                "What are JavaScript promises and how do they work?",
                "Explain the concept of closures in JavaScript with an example.",
                "What is the difference between '==' and '===' in JavaScript?"
            ],
            "react": [
                "What are React hooks and why are they useful?",
                "Explain the difference between state and props in React.",
                "What is the virtual DOM and how does it improve performance?",
                "How do you handle forms in React applications?"
            ],
            "django": [
                "Explain the MVC pattern in Django and how it's implemented.",
                "What are Django models and how do you define relationships between them?",
                "How do you handle user authentication in Django?",
                "What is Django ORM and how does it work?"
            ],
            "sql": [
                "Explain the difference between INNER JOIN and LEFT JOIN.",
                "What are database indexes and when should you use them?",
                "How do you optimize a slow SQL query?",
                "Explain the concept of database normalization.",
                "What is the difference between WHERE and HAVING clauses?",
                "How do you handle NULL values in SQL queries?"
            ],
            "mysql": [
                "What are the different storage engines in MySQL?",
                "Explain the difference between MyISAM and InnoDB.",
                "How do you optimize MySQL queries for better performance?",
                "What is database replication in MySQL?"
            ],
            "postgresql": [
                "What are the advantages of PostgreSQL over other databases?",
                "Explain ACID properties in PostgreSQL.",
                "What are PostgreSQL indexes and how do they work?",
                "How do you handle concurrent transactions in PostgreSQL?"
            ],
            "aws": [
                "What are the main differences between EC2, ECS, and Lambda?",
                "Explain the concept of S3 bucket policies and IAM roles.",
                "How do you ensure high availability in AWS architecture?",
                "What is the difference between RDS and DynamoDB?"
            ],
            "pandas": [
                "What is the difference between DataFrame and Series in pandas?",
                "How do you handle missing data in pandas?",
                "Explain groupby operations in pandas with an example.",
                "What are pandas indexes and how do you use them?"
            ],
            "numpy": [
                "What is the difference between NumPy arrays and Python lists?",
                "Explain broadcasting in NumPy with an example.",
                "How do you perform matrix operations in NumPy?",
                "What are NumPy universal functions (ufuncs)?"
            ],
            "machine learning": [
                "Explain the difference between supervised and unsupervised learning.",
                "What is overfitting and how do you prevent it?",
                "Explain the bias-variance tradeoff in machine learning.",
                "What are the different types of cross-validation techniques?"
            ],
            "data science": [
                "What is the typical data science workflow?",
                "How do you handle outliers in your data?",
                "Explain the difference between correlation and causation.",
                "What are the key steps in exploratory data analysis?"
            ]
        }
        
        # Generate questions based on detected technologies
        for tech in technologies:
            tech = tech.strip()
            # Check for exact matches first
            if tech in question_templates:
                questions.extend(question_templates[tech][:2])  # Add 2 questions per technology
            # Check for partial matches
            else:
                for key in question_templates:
                    if key in tech or tech in key:
                        questions.extend(question_templates[key][:2])
                        break
        
        # Special handling for data science related terms
        data_science_keywords = ["data", "analytics", "statistics", "ml", "ai", "analysis"]
        if any(keyword in tech_stack_lower for keyword in data_science_keywords):
            if "data science" in question_templates:
                questions.extend(question_templates["data science"][:2])
            if "machine learning" in question_templates:
                questions.extend(question_templates["machine learning"][:1])
        
        # If no specific questions found, generate generic ones based on the tech stack
        if not questions:
            questions = [
                f"Can you explain your experience with {technologies[0] if technologies else 'your primary technology'}?",
                "Describe a challenging technical problem you've solved recently.",
                "How do you stay updated with the latest trends in your tech stack?",
                "What best practices do you follow in your development process?",
                "How do you approach debugging and troubleshooting in your projects?"
            ]
        
        return questions[:5]  # Return maximum 5 questions
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input based on current conversation stage"""
        if self.check_exit_intent(user_input):
            st.session_state.conversation_ended = True
            return self.generate_goodbye_message()
        
        current_stage = st.session_state.current_stage
        candidate_info = st.session_state.candidate_info
        
        # Start with greeting if this is the first interaction
        if current_stage == 0 and not user_input.strip():
            st.session_state.current_stage = 1
            return self.generate_greeting()
        
        elif current_stage == 1:  # Name collection
            if len(user_input.strip()) < 2:
                return "Please provide your full name (at least 2 characters)."
            candidate_info.full_name = user_input.strip()
            st.session_state.current_stage = 2
            return f"Nice to meet you, {candidate_info.full_name}! 👋\n\nNow, could you please provide your **email address**?"
        
        elif current_stage == 2:  # Email collection
            if not self.validate_email(user_input.strip()):
                return "Please provide a valid email address (e.g., john@example.com)."
            candidate_info.email = user_input.strip()
            st.session_state.current_stage = 3
            return "Thank you! Now, please provide your **phone number**."
        
        elif current_stage == 3:  # Phone collection
            if not self.validate_phone(user_input.strip()):
                return "Please provide a valid phone number (e.g., +1234567890 or 123-456-7890)."
            candidate_info.phone = user_input.strip()
            st.session_state.current_stage = 4
            return "Great! How many **years of experience** do you have in your field?"
        
        elif current_stage == 4:  # Experience collection
            if not user_input.strip():
                return "Please provide your years of experience (e.g., '3 years' or '0-1 year')."
            candidate_info.experience_years = user_input.strip()
            st.session_state.current_stage = 5
            return "What **position(s)** are you interested in? (e.g., 'Software Developer', 'Data Scientist', 'Full Stack Developer')"
        
        elif current_stage == 5:  # Position collection
            if not user_input.strip():
                return "Please specify the position(s) you're interested in."
            candidate_info.desired_positions = user_input.strip()
            st.session_state.current_stage = 6
            return "What is your **current location**? (City, State/Country)"
        
        elif current_stage == 6:  # Location collection
            if not user_input.strip():
                return "Please provide your current location."
            candidate_info.current_location = user_input.strip()
            st.session_state.current_stage = 7
            return """Perfect! Now for the technical part. 
            
Please list your **tech stack** - the programming languages, frameworks, databases, and tools you're proficient in.

*For example: "Python, Django, PostgreSQL, React, AWS, Docker"*"""
        
        elif current_stage == 7:  # Tech stack collection
            if not user_input.strip():
                return "Please provide your tech stack (programming languages, frameworks, tools, etc.)."
            candidate_info.tech_stack = user_input.strip()
            
            # Generate technical questions
            questions = self.generate_technical_questions(candidate_info.tech_stack)
            st.session_state.technical_questions = questions
            st.session_state.current_question_index = 0
            st.session_state.current_stage = 8
            
            return f"""Excellent! Based on your tech stack: **{candidate_info.tech_stack}**

I'll now ask you {len(questions)} technical questions to assess your proficiency. Don't worry - just answer to the best of your ability!

**Question 1 of {len(questions)}:**
{questions[0]}"""
        
        elif current_stage == 8:  # Technical questions
            questions = st.session_state.technical_questions
            current_q_index = st.session_state.current_question_index
            
            # Store the answer
            st.session_state.conversation_history.append({
                "question": questions[current_q_index],
                "answer": user_input,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            current_q_index += 1
            st.session_state.current_question_index = current_q_index
            
            if current_q_index < len(questions):
                return f"""Thank you for your answer!

**Question {current_q_index + 1} of {len(questions)}:**
{questions[current_q_index]}"""
            else:
                st.session_state.current_stage = 9
                return self.generate_completion_message()
        
        return "I didn't understand that. Could you please try again?"
    
    def generate_completion_message(self) -> str:
        """Generate completion message"""
        candidate_info = st.session_state.candidate_info
        return f"""🎉 **Congratulations, {candidate_info.full_name}!** 

You've successfully completed the initial screening process with TalentScout's AI Hiring Assistant.

**Here's a summary of what we collected:**
- **Name:** {candidate_info.full_name}
- **Email:** {candidate_info.email}
- **Phone:** {candidate_info.phone}
- **Experience:** {candidate_info.experience_years}
- **Desired Position(s):** {candidate_info.desired_positions}
- **Location:** {candidate_info.current_location}
- **Tech Stack:** {candidate_info.tech_stack}
- **Technical Questions Answered:** {len(st.session_state.technical_questions)}

**Next Steps:**
1. Our recruitment team will review your responses within 2-3 business days
2. If your profile matches our current openings, we'll reach out via email or phone
3. You may be invited for a detailed technical interview or assessment

Thank you for your time and interest in TalentScout! We appreciate your effort in completing this screening process.

*You can now close this window or type 'exit' to end our conversation.*"""
    
    def generate_goodbye_message(self) -> str:
        """Generate goodbye message"""
        return """👋 **Thank you for using TalentScout's AI Hiring Assistant!**

We appreciate your time. If you'd like to complete the screening process later, please feel free to start a new session.

Have a great day! 🌟"""
    
    def export_candidate_data(self) -> Dict:
        """Export candidate data for download"""
        return {
            "candidate_info": asdict(st.session_state.candidate_info),
            "technical_qa": st.session_state.conversation_history,
            "session_completed": st.session_state.current_stage == 9,
            "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def main():
    """Main application function"""
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize the hiring assistant
    assistant = HiringAssistant()
    assistant.initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 TalentScout AI Hiring Assistant</h1>
        <p>Streamlining the recruitment process with intelligent screening</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with candidate information
    with st.sidebar:
        st.header("📋 Candidate Information")
        
        candidate_info = st.session_state.candidate_info
        
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        
        info_fields = [
            ("Full Name", candidate_info.full_name),
            ("Email", candidate_info.email),
            ("Phone", candidate_info.phone),
            ("Experience", candidate_info.experience_years),
            ("Desired Position", candidate_info.desired_positions),
            ("Location", candidate_info.current_location),
            ("Tech Stack", candidate_info.tech_stack)
        ]
        
        for field, value in info_fields:
            if value:
                st.write(f"**{field}:** {value}")
            else:
                st.write(f"**{field}:** *Not provided yet*")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress indicator
        stage_names = ["Start", "Name", "Email", "Phone", "Experience", "Position", "Location", "Tech Stack", "Questions", "Complete"]
        current_stage = min(st.session_state.current_stage, len(stage_names) - 1)
        
        st.header("📈 Progress")
        progress = current_stage / (len(stage_names) - 1)
        st.progress(progress)
        st.write(f"Stage: {stage_names[current_stage]} ({current_stage + 1}/{len(stage_names)})")
        
        # Export data button (only show when completed)
        if st.session_state.current_stage == 9:
            st.header("💾 Export Data")
            if st.button("Download Session Data"):
                data = assistant.export_candidate_data()
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name=f"candidate_data_{candidate_info.full_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Initialize conversation if not started
    if st.session_state.current_stage == 0:
        # Show initial greeting automatically
        st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
        st.markdown("**🤖 TalentScout Assistant:**")
        st.markdown(assistant.generate_greeting())
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.current_stage = 1  # Move to name collection stage
    
    # Display conversation history for technical questions
    if st.session_state.current_stage == 8 and st.session_state.conversation_history:
        st.subheader("Technical Q&A History")
        for i, qa in enumerate(st.session_state.conversation_history):
            st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
            st.markdown(f"**🤖 Question {i+1}:** {qa['question']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="chat-message user-message">', unsafe_allow_html=True)
            st.markdown(f"**👤 Your Answer:** {qa['answer']}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if not st.session_state.conversation_ended and st.session_state.current_stage < 9:
        
        # Show current prompt based on stage
        current_prompts = {
            1: "Please provide your **full name**:",
            2: "Please provide your **email address**:",
            3: "Please provide your **phone number**:",
            4: "How many **years of experience** do you have?",
            5: "What **position(s)** are you interested in?",
            6: "What is your **current location**?",
            7: "Please list your **tech stack** (programming languages, frameworks, tools):",
            8: f"**Question {st.session_state.current_question_index + 1} of {len(st.session_state.technical_questions)}:**" if st.session_state.technical_questions else "Technical Questions:"
        }
        
        if st.session_state.current_stage in current_prompts:
            st.info(current_prompts[st.session_state.current_stage])
            
            # Show current technical question if in technical stage
            if st.session_state.current_stage == 8 and st.session_state.technical_questions:
                current_q_index = st.session_state.current_question_index
                if current_q_index < len(st.session_state.technical_questions):
                    st.markdown(f"**{st.session_state.technical_questions[current_q_index]}**")
        
        user_input = st.text_input(
            "Your response:",
            key=f"user_input_{st.session_state.current_stage}_{st.session_state.current_question_index}",
            placeholder="Type your response here..."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            send_button = st.button("Send", type="primary")
        with col2:
            if st.button("End Conversation"):
                st.session_state.conversation_ended = True
                st.rerun()
        
        if send_button and user_input:
            # Process input and get response
            bot_response = assistant.process_user_input(user_input)
            
            # Display user message
            st.markdown('<div class="chat-message user-message">', unsafe_allow_html=True)
            st.markdown(f"**👤 You:** {user_input}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display bot response
            st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
            st.markdown("**🤖 TalentScout Assistant:**")
            st.markdown(bot_response)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Rerun to update the interface
            st.rerun()
    
    elif st.session_state.conversation_ended:
        st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
        st.markdown("**🤖 TalentScout Assistant:**")
        st.markdown(assistant.generate_goodbye_message())
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Start New Session"):
            # Reset session state
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    elif st.session_state.current_stage == 9:
        st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
        st.markdown("**🤖 TalentScout Assistant:**")
        st.markdown(assistant.generate_completion_message())
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start New Session"):
                # Reset session state
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()
        with col2:
            if st.button("End Session"):
                st.session_state.conversation_ended = True
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 <strong>TalentScout AI Hiring Assistant</strong> - Powered by Advanced Language Models</p>
        <p><em>Streamlining recruitment through intelligent automation</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()