# Story Create

A powerful API service that generates detailed user stories from business requirements using AI. This project leverages CrewAI to simulate a team of experts (Business Analyst, Product Owner, QA Engineer, and Technical Architect) to create comprehensive user stories with acceptance criteria, test cases, and API specifications.

## Features

- Generate detailed user stories from business requirements
- AI-powered analysis using GPT-3.5 Turbo
- Comprehensive output including:
  - User story and value statement
  - Acceptance criteria
  - Functional and non-functional requirements
  - Error scenarios
  - Technical considerations
  - Use case examples
  - Priority and effort estimates
  - Test cases with Rest Assured code
  - API specifications (when applicable)

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone git@github.com:barefoot-meadows-farm/story-agent.git
cd story-agent
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the API server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. Access the API documentation at `http://localhost:8000/docs`

4. Make a POST request to `/generate-user-story` with a JSON body containing:
```json
{
    "requirement": "Your business requirement here",
    "context": "Optional context",
    "stakeholders": ["Optional", "list", "of", "stakeholders"],
    "api_required": false,
    "additional_details": "Optional additional details"
}
```

## API Endpoints

- `GET /`: Health check endpoint
- `POST /generate-user-story`: Generate a user story from business requirements

## Development

The project uses:
- FastAPI for the web framework
- CrewAI for AI-powered task execution
- LangChain for LLM integration
- Pydantic for data validation
- Python-dotenv for environment variable management
