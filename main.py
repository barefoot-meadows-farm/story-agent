import os
from typing import List, Optional, Dict, Any

from langchain_community.chat_models import ChatOpenAI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

from map_json import generate_rest_assured_code, generate_default_api_specs

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="User Story Generator API",
    description="API for generating user stories from business requirements using Crew AI",
    version="1.0.0"
)

# Ensure OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Configure LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)


# Define data models
class BusinessRequirement(BaseModel):
    requirement: str
    context: Optional[str] = None
    stakeholders: Optional[List[str]] = None
    api_required: Optional[bool] = False
    additional_details: Optional[str] = None


class ApiSpec(BaseModel):
    endpoint: str
    method: str
    description: str
    request_example: Dict[str, Any]
    response_example: Dict[str, Any]
    error_responses: List[Dict[str, Any]]


class TestCase(BaseModel):
    title: str
    scenario: str
    given: List[str]
    when: List[str]
    then: List[str]
    rest_assured_code: Optional[str] = None


class UserStory(BaseModel):
    story: str
    value_statement: str
    acceptance_criteria: List[str]
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    error_scenarios: List[Dict[str, str]]
    technical_considerations: List[str]
    use_case_examples: List[str]
    priority: str
    effort_estimate: str
    test_cases: List[TestCase]
    api_specs: Optional[List[ApiSpec]] = None


# Define output models for CrewAI Task output_json
class BusinessAnalystOutput(BaseModel):
    story: str
    value_statement: str


class ErrorScenario(BaseModel):
    scenario: str
    message: str


class ProductOwnerOutput(BaseModel):
    priority: str
    priority_justification: str
    effort_estimate: str
    effort_justification: str
    use_case_examples: List[str]


class TestCaseOutput(BaseModel):
    title: str
    scenario: str
    given: List[str]
    when: List[str]
    then: List[str]
    rest_assured_code: Optional[str] = None


class QAEngineerOutput(BaseModel):
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    acceptance_criteria: List[str]
    error_scenarios: List[ErrorScenario]
    test_cases: List[TestCaseOutput]


class ErrorResponse(BaseModel):
    status_code: str
    message: str
    description: str


class ApiSpecOutput(BaseModel):
    endpoint: str
    method: str
    description: str
    request_example: Dict[str, Any]
    response_example: Dict[str, Any]
    error_responses: List[ErrorResponse]


class TechnicalArchitectOutput(BaseModel):
    technical_considerations: List[str]
    api_required: bool
    api_specs: Optional[List[ApiSpecOutput]] = None


# Define agents
def create_agents():
    business_analyst = Agent(
        role="Business Analyst",
        goal="Understand business requirements and translate them into clear user stories with value statements",
        backstory="""You are an experienced business analyst with a strong 
        understanding of software development processes. You excel at breaking 
        down complex business requirements into actionable user stories that 
        clearly articulate user value.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    product_owner = Agent(
        role="Product Owner",
        goal="Ensure user stories are aligned with business value and prioritize them",
        backstory="""You are a product owner with years of experience in agile 
        product development. You know how to evaluate user stories for business 
        value and ensure they meet customer needs. You can identify real-world
        use cases that demonstrate the value of features.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    qa_engineer = Agent(
        role="QA Engineer",
        goal="Develop thorough acceptance criteria, error scenarios, and test cases",
        backstory="""You are a detail-oriented QA engineer who knows how to define 
        clear acceptance criteria and identify potential error scenarios. You ensure 
        that user stories are testable and that all edge cases are considered.
        You're an expert in writing Gherkin test scenarios and REST Assured tests.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    technical_architect = Agent(
        role="Technical Architect",
        goal="Identify technical considerations and design API specifications",
        backstory="""You are a seasoned technical architect with expertise in 
        software design and API development. You can identify technical considerations
        for implementing features and provide detailed API specifications with
        example requests and responses.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    return business_analyst, product_owner, qa_engineer, technical_architect


# API endpoints
@app.get("/")
async def root():
    return {"message": "User Story Generator API is running"}


@app.post("/generate-user-story")
async def generate_user_story(requirement: BusinessRequirement):
    try:
        # Create agents
        business_analyst, product_owner, qa_engineer, technical_architect = create_agents()

        # Create tasks
        task1 = Task(
            description=f"""Analyze the following business requirement and draft a user story with a value statement:

            Business Requirement: {requirement.requirement}

            Additional Context: {requirement.context if requirement.context else 'None provided'}

            Stakeholders: {', '.join(requirement.stakeholders) if requirement.stakeholders else 'None specified'}

            Additional Details: {requirement.additional_details if requirement.additional_details else 'None provided'}

            Draft a proper user story in the format: 'As a [role], I want [feature], so that [benefit]'.
            Also create a separate value statement that explains the business and user value of this feature.
            Ensure the user story is clear, concise, and focused on user value.
            """,
            expected_output="""User story in 'As a [role], I want [feature], so that [benefit]' format.
            Value statement explaining business and user value.""",
            output_json=BusinessAnalystOutput,
            agent=business_analyst
        )

        task2 = Task(
            description="""Review the drafted user story and provide the following:
            1. Priority (High/Medium/Low)
            2. Effort estimate (using story points: 1, 2, 3, 5, 8, 13)
            3. At least 3 real-world use case examples showing how users would benefit from this feature

            Explain your reasoning for the priority and effort estimate.
            Be specific and concrete in the use case examples.
            """,
            expected_output="""Priority level with justification.
            Effort estimate with story points.
            At least 3 real-world use case examples.""",
            output_json=ProductOwnerOutput,
            agent=product_owner,
            context=[task1]
        )

        task3 = Task(
            description="""Develop comprehensive acceptance criteria and test cases:

            1. Functional Requirements: List 3-5 specific functional requirements
            2. Non-Functional Requirements: List 2-3 non-functional requirements (performance, usability, security, etc.)
            3. Acceptance Criteria: Write at least 5 specific acceptance criteria
            4. Error Scenarios: Identify at least 3 potential error scenarios and propose appropriate error messages
            5. Test Cases: Develop at least 3 test cases in Gherkin format with a focus on REST Assured testing

            For each test case, follow this structure:
            - Title: A descriptive title
            - Scenario: A brief description of the test scenario
            - Given: Preconditions (at least 1)
            - When: Actions performed (at least 1)
            - Then: Expected outcomes (at least 1)
            - REST Assured Code: Sample Java code using REST Assured for API testing
            """,
            expected_output="""List of functional requirements.
            List of non-functional requirements.
            Acceptance criteria list.
            Error scenarios with messages.
            Gherkin test cases with REST Assured examples.""",
            output_json=QAEngineerOutput,
            agent=qa_engineer,
            context=[task1, task2]
        )

        task4 = Task(
            description=f"""Provide technical considerations and, if applicable, API specifications:

            1. Technical Considerations: List 3-5 technical considerations for implementing this user story

            API Required: {'Yes' if requirement.api_required else 'Analyze the requirement and determine if an API is needed'}

            If an API is required, provide the following for each API endpoint:
            - Endpoint URL (with examples)
            - HTTP Method
            - Description
            - Request payload example (JSON)
            - Response payload example (JSON)
            - Error response examples (at least 2)

            Format your response in a structured way that can be easily parsed.
            """,
            expected_output="""List of technical considerations.
            API specifications if required including endpoints, methods, payloads, and error responses.""",
            output_json=TechnicalArchitectOutput,
            agent=technical_architect,
            context=[task1, task2, task3]
        )

        # Create crew
        crew = Crew(
            agents=[business_analyst, product_owner, qa_engineer, technical_architect],
            tasks=[task1, task2, task3, task4],
            verbose=True
        )

        # Execute crew workflow
        result = crew.kickoff()

        response = {}
        # Use json_dict to get structured output
        try:
            task_list = result.tasks_output
            for task in task_list:
                task_dict = task.json_dict
                response[task.agent] = task_dict

            # Map response object to UserStory model
            return map_crew_output_to_user_story(response)
        except AttributeError:
            pass


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating user story: {str(e)}"
        )


def map_crew_output_to_user_story(crew_output: Dict[str, Any]) -> UserStory:
    """
    Maps the output from CrewAI agents to a UserStory object.

    Args:
        crew_output: Dictionary containing outputs from different CrewAI agents
                    (Business Analyst, Product Owner, QA Engineer, Technical Architect)

    Returns:
        A UserStory object with all the fields populated from the CrewAI output
    """
    # Extract data from each agent's output
    business_analyst_data = crew_output.get("Business Analyst", {})
    product_owner_data = crew_output.get("Product Owner", {})
    qa_engineer_data = crew_output.get("QA Engineer", {})
    technical_architect_data = crew_output.get("Technical Architect", {})

    # Create test cases with proper REST Assured code
    test_cases = []
    for test_case_data in qa_engineer_data.get("test_cases", []):
        # Add detailed REST Assured code if it's missing or too generic
        if not test_case_data.get("rest_assured_code") or "Sample Java code" in test_case_data.get("rest_assured_code",
                                                                                                   ""):
            rest_assured_code = generate_rest_assured_code(test_case_data)
        else:
            rest_assured_code = test_case_data.get("rest_assured_code")

        test_cases.append(TestCase(
            title=test_case_data.get("title", ""),
            scenario=test_case_data.get("scenario", ""),
            given=test_case_data.get("given", []),
            when=test_case_data.get("when", []),
            then=test_case_data.get("then", []),
            rest_assured_code=rest_assured_code
        ))

    # Generate API specs if they're not provided
    api_specs_data = technical_architect_data.get("api_specs", [])
    if not api_specs_data:
        # Create default API spec based on the requirements
        api_specs_data = generate_default_api_specs(
            business_analyst_data.get("story", ""),
            qa_engineer_data.get("functional_requirements", [])
        )

    api_specs = []
    for api_spec_data in api_specs_data:
        api_specs.append(ApiSpec(
            endpoint=api_spec_data.get("endpoint", ""),
            method=api_spec_data.get("method", ""),
            description=api_spec_data.get("description", ""),
            request_example=api_spec_data.get("request_example", {}),
            response_example=api_spec_data.get("response_example", {}),
            error_responses=api_spec_data.get("error_responses", [])
        ))

    # Create the UserStory object
    user_story = UserStory(
        story=business_analyst_data.get("story", ""),
        value_statement=business_analyst_data.get("value_statement", ""),
        acceptance_criteria=qa_engineer_data.get("acceptance_criteria", []),
        functional_requirements=qa_engineer_data.get("functional_requirements", []),
        non_functional_requirements=qa_engineer_data.get("non_functional_requirements", []),
        error_scenarios=qa_engineer_data.get("error_scenarios", []),
        technical_considerations=technical_architect_data.get("technical_considerations", []),
        use_case_examples=product_owner_data.get("use_case_examples", []),
        priority=product_owner_data.get("priority", "Medium"),
        effort_estimate=product_owner_data.get("effort_estimate", "3"),
        test_cases=test_cases,
        api_specs=api_specs
    )

    return user_story


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)