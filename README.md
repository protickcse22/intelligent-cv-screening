# Intelligent CV Screening System

An AI-powered multi-agent system for automated candidate evaluation and CV-LinkedIn profile verification using CrewAI framework.

## 🎯 Overview

The Intelligent CV Screening System is a sophisticated multi-agent AI application that automates the candidate screening process by:

- **Analyzing CV documents** and extracting structured candidate information
- **Processing LinkedIn profiles** to gather professional data
- **Cross-verifying information** between CV and LinkedIn profiles for consistency
- **Making data-driven hiring decisions** based on job requirements and candidate fit

## 🚀 Features

### Multi-Agent Architecture
- **CV Analyst Agent**: Extracts and structures data from CV PDFs
- **LinkedIn Agent**: Processes LinkedIn profile PDFs
- **Verification Agent**: Cross-references data between sources for consistency
- **Supervisor Agent**: Makes final hiring decisions based on structured analysis

### Intelligent Processing
- 📄 **PDF Processing**: Reads and extracts text from CV and LinkedIn PDFs
- 🔍 **Data Extraction**: Structures candidate information (skills, experience, education, certifications)
- ✅ **Verification**: Identifies discrepancies between CV and LinkedIn data
- 📊 **Scoring System**: Calculates confidence and matching scores
- 🎯 **Decision Making**: Provides transparent hiring recommendations

### Key Capabilities
- Fuzzy name matching for profile verification
- Skills overlap percentage calculation
- Employment period validation
- Profile completeness assessment
- Evidence-based decision explanations

## 🛠️ Technology Stack

- **Framework**: [CrewAI](https://crewai.com) - Multi-agent AI framework
- **PDF Processing**: PyMuPDF for document parsing
- **Language Model**: OpenAI GPT (configurable)
- **Data Validation**: Pydantic models
- **Configuration**: YAML-based agent and task definitions

## 📋 Prerequisites

- Python >= 3.10, < 3.14
- OpenAI API key
- UV package manager (recommended)

## ⚡ Quick Start

### 1. Installation

Install UV package manager (if not already installed):
```bash
pip install uv
```

Clone and set up the project:
```bash
git clone <repository-url>
cd intelligent_cv_screening
```

Install dependencies using CrewAI CLI:
```bash
crewai install
```

Or using UV directly:
```bash
uv install
```

### 2. Configuration

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Prepare Data

Organize your candidate files:
```
knowledge/
├── resumes/
│   ├── candidate_name.pdf
│   └── another_candidate.pdf
└── linkedin/
    ├── candidate_name.pdf
    └── another_candidate.pdf
```

**Note**: CV and LinkedIn files should have matching names (e.g., `john_doe.pdf`) for automatic pairing.

### 4. Run the System

```bash
python src/intelligent_cv_screening/main.py
```

## 📁 Project Structure

```
intelligent_cv_screening/
├── src/intelligent_cv_screening/
│   ├── config/
│   │   ├── agents.yaml          # Agent configurations
│   │   └── tasks.yaml           # Task definitions
│   ├── knowledge/
│   │   ├── resumes/             # CV PDF files
│   │   └── linkedin/            # LinkedIn PDF files
│   ├── model/
│   │   └── final_decision_model.py  # Output data models
│   ├── tools/
│   │   └── pdf_reader.py        # PDF processing tools
│   ├── utils/
│   │   └── utils.py             # File matching utilities
│   ├── crew.py                  # Main crew orchestration
│   └── main.py                  # Application entry point
├── pyproject.toml               # Project dependencies
└── README.md
```

## 🔧 Customization

### Modifying Agents

Edit `src/intelligent_cv_screening/config/agents.yaml` to customize agent roles, goals, and backstories.

### Adjusting Tasks

Modify `src/intelligent_cv_screening/config/tasks.yaml` to change task descriptions and expected outputs.

### Custom Job Descriptions

Update the job description in `main.py`:
```python
job_description = "Your custom job requirements here"
```

## 📊 Output Format

The system provides structured JSON output including:

```json
{
  "verdict": "Select/Reject",
  "justification": "Detailed reasoning based on analysis",
  "confidence_score": 85,
  "matching_score": 78,
  "discrepancies": [
    {
      "field": "experience",
      "cv_value": "5 years",
      "linkedin_value": "4 years",
      "issue": "Mismatch"
    }
  ]
}
```

## 🚦 Usage Examples

### Basic Screening
```python
from src.intelligent_cv_screening.crew import crew

result = crew.kickoff(
    inputs={
        "cv_file_path": "path/to/cv.pdf",
        "linkedin_file_path": "path/to/linkedin.pdf",
        "job_description": "Python developer with Django experience"
    }
)
```

### Batch Processing
The system automatically processes all matched CV-LinkedIn pairs in the knowledge folders.

## 🔍 Key Components

### Agents
- **CV Analyst**: Specializes in CV data extraction and job fit evaluation
- **LinkedIn Agent**: Focuses on LinkedIn profile data parsing
- **Verification Agent**: Cross-references information for consistency
- **Supervisor**: Makes final hiring decisions based on structured evidence

### Tools
- **PDF Reader**: Extracts text content from PDF documents
- **File Matcher**: Automatically pairs CV and LinkedIn files by candidate name

## 📈 Scoring System

- **Confidence Score** (1-100): How well the candidate matches job requirements
- **Matching Score** (0-100): Consistency between CV and LinkedIn profiles
- **Breakdown Scores**: Individual scores for name, company, dates, skills, completeness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions, issues, or feature requests:
- Create an issue in the repository
- Check the [CrewAI documentation](https://docs.crewai.com)
- Review the configuration files for customization options

## 🙏 Acknowledgments

- Built with [CrewAI](https://crewai.com) multi-agent framework
- Powered by OpenAI's language models
- PDF processing via PyMuPDF

---

**Note**: This system is designed for automated screening assistance. Final hiring decisions should always involve human review and comply with applicable employment laws and regulations.
