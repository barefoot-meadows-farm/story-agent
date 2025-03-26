# # Extract data from structured output
#             # Task 1 output (Business Analyst)
#             story = json_output.get("story", "")
#             value_statement = json_output.get("value_statement", "")
#
#             # Task 2 output (Product Owner)
#             priority = json_output.get("priority", "Medium")
#             effort_estimate = json_output.get("effort_estimate", "3")
#             use_case_examples = json_output.get("use_case_examples", [])
#
#             # Task 3 output (QA Engineer)
#             functional_requirements = json_output.get("functional_requirements", [])
#             non_functional_requirements = json_output.get("non_functional_requirements", [])
#             acceptance_criteria = json_output.get("acceptance_criteria", [])
#             error_scenarios = json_output.get("error_scenarios", [])
#             test_cases_json = json_output.get("test_cases", [])
#
#             # Task 4 output (Technical Architect)
#             technical_considerations = json_output.get("technical_considerations", [])
#             api_specs_json = json_output.get("api_specs", []) if json_output.get("api_required", False) else []
#
#             # Convert test cases from JSON to Pydantic models
#             test_cases = []
#             for test in test_cases_json:
#                 test_cases.append(TestCase(
#                     title=test.get("title", ""),
#                     scenario=test.get("scenario", ""),
#                     given=test.get("given", []),
#                     when=test.get("when", []),
#                     then=test.get("then", []),
#                     rest_assured_code=test.get("rest_assured_code", "")
#                 ))
#
#             # Convert API specs from JSON to Pydantic models if needed
#             api_specs = []
#             for api in api_specs_json:
#                 api_specs.append(ApiSpec(
#                     endpoint=api.get("endpoint", ""),
#                     method=api.get("method", ""),
#                     description=api.get("description", ""),
#                     request_example=api.get("request_example", {}),
#                     response_example=api.get("response_example", {}),
#                     error_responses=api.get("error_responses", [])
#                 ))
#
#             # Create the final UserStory object with the structured data
#             return UserStory(
#                 story=story,
#                 value_statement=value_statement,
#                 acceptance_criteria=acceptance_criteria,
#                 functional_requirements=functional_requirements,
#                 non_functional_requirements=non_functional_requirements,
#                 error_scenarios=error_scenarios,
#                 technical_considerations=technical_considerations,
#                 use_case_examples=use_case_examples,
#                 priority=priority,
#                 effort_estimate=effort_estimate,
#                 test_cases=test_cases,
#                 api_specs=api_specs if api_specs else None
#             )
#
#         except Exception as e:
#             # Fallback to text parsing if json_dict fails
#             print(f"Error using json_dict: {str(e)}")
#             print("Falling back to text parsing...")
#
#             # The rest of the text parsing code remains the same
#             sections = result.raw_output.split("\n\n")
#
#             # Extract the basic user story and value statement
#             user_story_section = next((s for s in sections if "As a " in s), "")
#             story = next((line for line in user_story_section.split('\n') if line.startswith('As a ')), "")
#
#             value_statement = next((s for s in sections if "Value Statement" in s), "")
#             value_statement = value_statement.replace("Value Statement:", "").strip()
#             if not value_statement:
#                 value_statement = "This feature provides value by improving user experience and business efficiency."
#
#             # Extract functional and non-functional requirements
#             functional_req_section = next((s for s in sections if "Functional Requirements" in s), "")
#             functional_requirements = [
#                 line.strip().replace("- ", "")
#                 for line in functional_req_section.split("\n")
#                 if line.strip().startswith("- ")
#             ]
#
#             non_functional_req_section = next((s for s in sections if "Non-Functional Requirements" in s), "")
#             non_functional_requirements = [
#                 line.strip().replace("- ", "")
#                 for line in non_functional_req_section.split("\n")
#                 if line.strip().startswith("- ")
#             ]
#
#             # Extract acceptance criteria
#             acceptance_criteria_section = next((s for s in sections if "Acceptance Criteria" in s), "")
#             acceptance_criteria = [
#                 line.strip()
#                 for line in acceptance_criteria_section.split("\n")
#                 if line.strip().startswith("- ") or (
#                             line.strip().startswith("Given") and "When" in line and "Then" in line)
#             ]
#
#             # Extract error scenarios
#             error_section = next((s for s in sections if "Error Scenarios" in s), "")
#             error_scenarios = []
#             for line in error_section.split("\n"):
#                 if line.strip().startswith("- ") or line.strip().startswith("1. "):
#                     scenario = line.replace("- ", "").replace("1. ", "").strip()
#                     message = ""
#                     if ":" in scenario:
#                         scenario_parts = scenario.split(":", 1)
#                         scenario = scenario_parts[0].strip()
#                         message = scenario_parts[1].strip()
#                     error_scenarios.append({"scenario": scenario, "message": message})
#
#             # Extract technical considerations
#             tech_section = next((s for s in sections if "Technical Considerations" in s), "")
#             technical_considerations = [
#                 line.strip().replace("- ", "").replace("* ", "")
#                 for line in tech_section.split("\n")
#                 if line.strip().startswith("- ") or line.strip().startswith("* ")
#             ]
#
#             # Extract use case examples
#             use_case_section = next((s for s in sections if "Use Case Examples" in s or "Real-world Use Cases" in s),
#                                     "")
#             use_case_examples = [
#                 line.strip().replace("- ", "").replace("* ", "")
#                 for line in use_case_section.split("\n")
#                 if line.strip().startswith("- ") or line.strip().startswith("* ")
#             ]
#
#             # Extract priority and effort
#             priority_line = next((line for line in result.raw_output.split('\n') if "Priority:" in line),
#                                  "Priority: Medium")
#             priority = priority_line.split('Priority:')[1].strip() if 'Priority:' in priority_line else "Medium"
#
#             effort_line = next((line for line in result.raw_output.split('\n') if
#                                 "Effort Estimate:" in line or "Story Points:" in line), "")
#             effort_estimate = ""
#             if "Effort Estimate:" in effort_line:
#                 effort_estimate = effort_line.split('Effort Estimate:')[1].strip()
#             elif "Story Points:" in effort_line:
#                 effort_estimate = effort_line.split('Story Points:')[1].strip()
#             else:
#                 effort_estimate = "3"
#
#             # Extract test cases in Gherkin format
#             test_cases = []
#             test_case_sections = [s for s in sections if "Scenario:" in s and ("Given" in s or "GIVEN" in s)]
#
#             for test_section in test_case_sections:
#                 test_lines = test_section.split('\n')
#                 title = next((line for line in test_lines if "Title:" in line), "Test Case")
#                 title = title.replace("Title:", "").strip()
#
#                 scenario = next((line for line in test_lines if "Scenario:" in line), "")
#                 scenario = scenario.replace("Scenario:", "").strip()
#
#                 given_lines = [line.strip() for line in test_lines if
#                                line.strip().startswith("Given") or line.strip().startswith(
#                                    "GIVEN") or line.strip().startswith("And ") and "given" in test_section.lower()]
#                 when_lines = [line.strip() for line in test_lines if
#                               line.strip().startswith("When") or line.strip().startswith(
#                                   "WHEN") or line.strip().startswith("And ") and "when" in test_section.lower()]
#                 then_lines = [line.strip() for line in test_lines if
#                               line.strip().startswith("Then") or line.strip().startswith(
#                                   "THEN") or line.strip().startswith("And ") and "then" in test_section.lower()]
#
#                 rest_assured_section = "\n".join(test_lines[test_lines.index(next((line for line in test_lines if
#                                                                                    "REST Assured" in line or "RestAssured" in line or "```java" in line),
#                                                                                   "")) + 1:])
#                 rest_assured_code = ""
#                 if "```" in rest_assured_section:
#                     rest_assured_code = rest_assured_section.split("```")[1].replace("java", "").strip()
#                 else:
#                     rest_assured_code = rest_assured_section.strip()
#
#                 test_cases.append(TestCase(
#                     title=title,
#                     scenario=scenario,
#                     given=given_lines,
#                     when=when_lines,
#                     then=then_lines,
#                     rest_assured_code=rest_assured_code if rest_assured_code else None
#                 ))
#
#             # Extract API specifications if available
#             api_specs = []
#             api_sections = [s for s in sections if "Endpoint URL:" in s or "HTTP Method:" in s]
#
#             for api_section in api_sections:
#                 api_lines = api_section.split('\n')
#
#                 endpoint = next((line for line in api_lines if "Endpoint URL:" in line), "")
#                 endpoint = endpoint.replace("Endpoint URL:", "").strip()
#
#                 method = next((line for line in api_lines if "HTTP Method:" in line), "")
#                 method = method.replace("HTTP Method:", "").strip()
#
#                 description = next((line for line in api_lines if "Description:" in line), "")
#                 description = description.replace("Description:", "").strip()
#
#                 # Extract JSON examples for request and response
#                 request_example = {}
#                 response_example = {}
#                 error_responses = []
#
#                 in_request = False
#                 in_response = False
#                 in_error = False
#                 request_json = ""
#                 response_json = ""
#                 error_json = ""
#
#                 for i, line in enumerate(api_lines):
#                     if "Request Example:" in line or "Request Payload:" in line:
#                         in_request = True
#                         in_response = False
#                         in_error = False
#                         continue
#                     elif "Response Example:" in line or "Response Payload:" in line:
#                         in_request = False
#                         in_response = True
#                         in_error = False
#                         continue
#                     elif "Error Response:" in line or "Error Response Example:" in line:
#                         in_request = False
#                         in_response = False
#                         in_error = True
#                         continue
#
#                     if in_request:
#                         request_json += line + "\n"
#                     elif in_response:
#                         response_json += line + "\n"
#                     elif in_error:
#                         error_json += line + "\n"
#
#                 # Simple parsing of JSON-like content from text
#                 import re
#                 import json
#
#                 def extract_json_from_text(text):
#                     # Find JSON-like structures in the text
#                     matches = re.findall(r'({[\s\S]*?})', text)
#                     if matches:
#                         # Try to parse the first match as JSON
#                         try:
#                             return json.loads(matches[0])
#                         except:
#                             # If parsing fails, return a simple placeholder
#                             return {"content": text.strip()}
#                     return {"content": text.strip()}
#
#                 try:
#                     request_example = extract_json_from_text(request_json)
#                     response_example = extract_json_from_text(response_json)
#
#                     # For error responses, we might have multiple examples
#                     error_responses = []
#                     error_examples = error_json.split("Example")
#                     for error_ex in error_examples:
#                         if error_ex.strip():
#                             try:
#                                 error_responses.append(extract_json_from_text(error_ex))
#                             except:
#                                 error_responses.append({"error": "Parsing error", "message": error_ex.strip()})
#
#                     if endpoint and method:
#                         api_specs.append(ApiSpec(
#                             endpoint=endpoint,
#                             method=method,
#                             description=description,
#                             request_example=request_example,
#                             response_example=response_example,
#                             error_responses=error_responses if error_responses else [{"error": "Not specified"}]
#                         ))
#                 except Exception as e:
#                     print(f"Error parsing API specs: {str(e)}")
#
#             # Create the final UserStory object
#             return UserStory(
#                 story=story,
#                 value_statement=value_statement,
#                 acceptance_criteria=acceptance_criteria if acceptance_criteria else ["Feature works as expected"],
#                 functional_requirements=functional_requirements if functional_requirements else [
#                     "Implement the requested functionality"],
#                 non_functional_requirements=non_functional_requirements if non_functional_requirements else [
#                     "System maintains performance standards"],
#                 error_scenarios=error_scenarios if error_scenarios else [
#                     {"scenario": "General error", "message": "An unexpected error occurred"}],
#                 technical_considerations=technical_considerations if technical_considerations else [
#                     "Standard development practices should be followed"],
#                 use_case_examples=use_case_examples if use_case_examples else [
#                     "Basic user interaction with the feature"],
#                 priority=priority,
#                 effort_estimate=effort_estimate,
#                 test_cases=test_cases if test_cases else [TestCase(
#                     title="Basic Functionality Test",
#                     scenario="Verify the feature works as expected",
#                     given=["The system is operational"],
#                     when=["User interacts with the feature"],
#                     then=["The expected outcome is achieved"],
#                     rest_assured_code=None
#                 )],
#                 api_specs=api_specs if api_specs else None
#             )
#         story = next((line for line in user_story_section.split('\n') if line.startswith('As a ')), "")
#
#         value_statement = next((s for s in sections if "Value Statement" in s), "")
#         value_statement = value_statement.replace("Value Statement:", "").strip()
#         if not value_statement:
#             value_statement = "This feature provides value by improving user experience and business efficiency."
#
#         # Extract functional and non-functional requirements
#         functional_req_section = next((s for s in sections if "Functional Requirements" in s), "")
#         functional_requirements = [
#             line.strip().replace("- ", "")
#             for line in functional_req_section.split("\n")
#             if line.strip().startswith("- ")
#         ]
#
#         non_functional_req_section = next((s for s in sections if "Non-Functional Requirements" in s), "")
#         non_functional_requirements = [
#             line.strip().replace("- ", "")
#             for line in non_functional_req_section.split("\n")
#             if line.strip().startswith("- ")
#         ]
#
#         # Extract acceptance criteria
#         acceptance_criteria_section = next((s for s in sections if "Acceptance Criteria" in s), "")
#         acceptance_criteria = [
#             line.strip()
#             for line in acceptance_criteria_section.split("\n")
#             if line.strip().startswith("- ") or (line.strip().startswith("Given") and "When" in line and "Then" in line)
#         ]
#
#         # Extract error scenarios
#         error_section = next((s for s in sections if "Error Scenarios" in s), "")
#         error_scenarios = []
#         for line in error_section.split("\n"):
#             if line.strip().startswith("- ") or line.strip().startswith("1. "):
#                 scenario = line.replace("- ", "").replace("1. ", "").strip()
#                 message = ""
#                 if ":" in scenario:
#                     scenario_parts = scenario.split(":", 1)
#                     scenario = scenario_parts[0].strip()
#                     message = scenario_parts[1].strip()
#                 error_scenarios.append({"scenario": scenario, "message": message})
#
#         # Extract technical considerations
#         tech_section = next((s for s in sections if "Technical Considerations" in s), "")
#         technical_considerations = [
#             line.strip().replace("- ", "").replace("* ", "")
#             for line in tech_section.split("\n")
#             if line.strip().startswith("- ") or line.strip().startswith("* ")
#         ]
#
#         # Extract use case examples
#         use_case_section = next((s for s in sections if "Use Case Examples" in s or "Real-world Use Cases" in s), "")
#         use_case_examples = [
#             line.strip().replace("- ", "").replace("* ", "")
#             for line in use_case_section.split("\n")
#             if line.strip().startswith("- ") or line.strip().startswith("* ")
#         ]
#
#         # Extract priority and effort
#         priority_line = next((line for line in result.split('\n') if "Priority:" in line), "Priority: Medium")
#         priority = priority_line.split('Priority:')[1].strip() if 'Priority:' in priority_line else "Medium"
#
#         effort_line = next(
#             (line for line in result.split('\n') if "Effort Estimate:" in line or "Story Points:" in line), "")
#         effort_estimate = ""
#         if "Effort Estimate:" in effort_line:
#             effort_estimate = effort_line.split('Effort Estimate:')[1].strip()
#         elif "Story Points:" in effort_line:
#             effort_estimate = effort_line.split('Story Points:')[1].strip()
#         else:
#             effort_estimate = "3"
#
#         # Extract test cases in Gherkin format
#         test_cases = []
#         test_case_sections = [s for s in sections if "Scenario:" in s and ("Given" in s or "GIVEN" in s)]
#
#         for test_section in test_case_sections:
#             test_lines = test_section.split('\n')
#             title = next((line for line in test_lines if "Title:" in line), "Test Case")
#             title = title.replace("Title:", "").strip()
#
#             scenario = next((line for line in test_lines if "Scenario:" in line), "")
#             scenario = scenario.replace("Scenario:", "").strip()
#
#             given_lines = [line.strip() for line in test_lines if
#                            line.strip().startswith("Given") or line.strip().startswith(
#                                "GIVEN") or line.strip().startswith("And ") and "given" in test_section.lower()]
#             when_lines = [line.strip() for line in test_lines if
#                           line.strip().startswith("When") or line.strip().startswith("WHEN") or line.strip().startswith(
#                               "And ") and "when" in test_section.lower()]
#             then_lines = [line.strip() for line in test_lines if
#                           line.strip().startswith("Then") or line.strip().startswith("THEN") or line.strip().startswith(
#                               "And ") and "then" in test_section.lower()]
#
#             rest_assured_section = "\n".join(test_lines[test_lines.index(next(
#                 (line for line in test_lines if "REST Assured" in line or "RestAssured" in line or "```java" in line),
#                 "")) + 1:])
#             rest_assured_code = ""
#             if "```" in rest_assured_section:
#                 rest_assured_code = rest_assured_section.split("```")[1].replace("java", "").strip()
#             else:
#                 rest_assured_code = rest_assured_section.strip()
#
#             test_cases.append(TestCase(
#                 title=title,
#                 scenario=scenario,
#                 given=given_lines,
#                 when=when_lines,
#                 then=then_lines,
#                 rest_assured_code=rest_assured_code if rest_assured_code else None
#             ))
#
#         # Extract API specifications if available
#         api_specs = []
#         api_sections = [s for s in sections if "Endpoint URL:" in s or "HTTP Method:" in s]
#
#         for api_section in api_sections:
#             api_lines = api_section.split('\n')
#
#             endpoint = next((line for line in api_lines if "Endpoint URL:" in line), "")
#             endpoint = endpoint.replace("Endpoint URL:", "").strip()
#
#             method = next((line for line in api_lines if "HTTP Method:" in line), "")
#             method = method.replace("HTTP Method:", "").strip()
#
#             description = next((line for line in api_lines if "Description:" in line), "")
#             description = description.replace("Description:", "").strip()
#
#             # Extract JSON examples for request and response
#             request_example = {}
#             response_example = {}
#             error_responses = []
#
#             in_request = False
#             in_response = False
#             in_error = False
#             request_json = ""
#             response_json = ""
#             error_json = ""
#
#             for i, line in enumerate(api_lines):
#                 if "Request Example:" in line or "Request Payload:" in line:
#                     in_request = True
#                     in_response = False
#                     in_error = False
#                     continue
#                 elif "Response Example:" in line or "Response Payload:" in line:
#                     in_request = False
#                     in_response = True
#                     in_error = False
#                     continue
#                 elif "Error Response:" in line or "Error Response Example:" in line:
#                     in_request = False
#                     in_response = False
#                     in_error = True
#                     continue
#
#                 if in_request:
#                     request_json += line + "\n"
#                 elif in_response:
#                     response_json += line + "\n"
#                 elif in_error:
#                     error_json += line + "\n"
#
#             # Simple parsing of JSON-like content from text
#             import re
#             import json
#
#             def extract_json_from_text(text):
#                 # Find JSON-like structures in the text
#                 matches = re.findall(r'({[\s\S]*?})', text)
#                 if matches:
#                     # Try to parse the first match as JSON
#                     try:
#                         return json.loads(matches[0])
#                     except:
#                         # If parsing fails, return a simple placeholder
#                         return {"content": text.strip()}
#                 return {"content": text.strip()}
#
#             try:
#                 request_example = extract_json_from_text(request_json)
#                 response_example = extract_json_from_text(response_json)
#
#                 # For error responses, we might have multiple examples
#                 error_responses = []
#                 error_examples = error_json.split("Example")
#                 for error_ex in error_examples:
#                     if error_ex.strip():
#                         try:
#                             error_responses.append(extract_json_from_text(error_ex))
#                         except:
#                             error_responses.append({"error": "Parsing error", "message": error_ex.strip()})
#
#                 if endpoint and method:
#                     api_specs.append(ApiSpec(
#                         endpoint=endpoint,
#                         method=method,
#                         description=description,
#                         request_example=request_example,
#                         response_example=response_example,
#                         error_responses=error_responses if error_responses else [{"error": "Not specified"}]
#                     ))
#             except Exception as e:
#                 print(f"Error parsing API specs: {str(e)}")
#
#         # Create the final UserStory object
#         return UserStory(
#             story=story,
#             value_statement=value_statement,
#             acceptance_criteria=acceptance_criteria if acceptance_criteria else ["Feature works as expected"],
#             functional_requirements=functional_requirements if functional_requirements else [
#                 "Implement the requested functionality"],
#             non_functional_requirements=non_functional_requirements if non_functional_requirements else [
#                 "System maintains performance standards"],
#             error_scenarios=error_scenarios if error_scenarios else [
#                 {"scenario": "General error", "message": "An unexpected error occurred"}],
#             technical_considerations=technical_considerations if technical_considerations else [
#                 "Standard development practices should be followed"],
#             use_case_examples=use_case_examples if use_case_examples else ["Basic user interaction with the feature"],
#             priority=priority,
#             effort_estimate=effort_estimate,
#             test_cases=test_cases if test_cases else [TestCase(
#                 title="Basic Functionality Test",
#                 scenario="Verify the feature works as expected",
#                 given=["The system is operational"],
#                 when=["User interacts with the feature"],
#                 then=["The expected outcome is achieved"],
#                 rest_assured_code=None
#             )],
#             api_specs=api_specs if api_specs else None
#         )