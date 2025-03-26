from typing import Dict, Any, List


def generate_rest_assured_code(test_case_data: Dict[str, Any]) -> str:
    """
    Generates REST Assured code based on the test case data.

    Args:
        test_case_data: Dictionary containing test case information

    Returns:
        REST Assured code as a string
    """
    title = test_case_data.get("title", "")
    scenario = test_case_data.get("scenario", "")

    # Create method name from title
    method_name = "test" + "".join(word.capitalize() for word in title.split())

    # Generate appropriate REST Assured code based on the scenario
    if "valid" in scenario.lower() and "invalid" not in scenario.lower():
        # Happy path test
        return f"""
@Test
public void {method_name}() {{
    // Set up test data
    Map<String, Object> requestData = new HashMap<>();
    requestData.put("address", "123 Main St, City, State 12345");
    requestData.put("enrreqad_setting", "TRUE");

    // Make API request
    given()
        .contentType(ContentType.JSON)
        .body(requestData)
    .when()
        .post("/api/v1/enrollment")
    .then()
        .statusCode(200)
        .body("status", equalTo("success"))
        .body("addressValidation.status", equalTo("valid"));
}}"""
    elif "invalid" in scenario.lower():
        # Invalid input test
        return f"""
@Test
public void {method_name}() {{
    // Set up test data with invalid input
    Map<String, Object> requestData = new HashMap<>();
    requestData.put("address", "Invalid Address Format");
    requestData.put("enrreqad_setting", "TRUE");

    // Make API request
    given()
        .contentType(ContentType.JSON)
        .body(requestData)
    .when()
        .post("/api/v1/enrollment")
    .then()
        .statusCode(400)
        .body("status", equalTo("error"))
        .body("message", containsString("Address format is invalid"));
}}"""
    elif "fail" in scenario.lower() or "error" in scenario.lower():
        # Error case test
        return f"""
@Test
public void {method_name}() {{
    // Setup mock to simulate service failure
    // This would be setup in the test class or before method

    // Set up test data
    Map<String, Object> requestData = new HashMap<>();
    requestData.put("address", "123 Main St, City, State 12345");
    requestData.put("enrreqad_setting", "TRUE");

    // Make API request
    given()
        .contentType(ContentType.JSON)
        .body(requestData)
    .when()
        .post("/api/v1/enrollment")
    .then()
        .statusCode(500)
        .body("status", equalTo("error"))
        .body("message", containsString("validation failed"));
}}"""
    else:
        # Generic test
        return f"""
@Test
public void {method_name}() {{
    // Set up test data
    Map<String, Object> requestData = new HashMap<>();
    // Add required fields based on test case

    // Make API request
    given()
        .contentType(ContentType.JSON)
        .body(requestData)
    .when()
        .post("/api/endpoint")
    .then()
        .statusCode(200)
        .body("status", equalTo("success"));
}}"""


def generate_default_api_specs(story: str, functional_requirements: List[str]) -> List[Dict[str, Any]]:
    """
    Generates default API specifications based on the user story and functional requirements.

    Args:
        story: User story text
        functional_requirements: List of functional requirements

    Returns:
        List of API specification dictionaries
    """
    # Create a basic API endpoint based on the story context
    if "ENRREQAD" in story:
        return [
            {
                "endpoint": "/api/v1/enrollment",
                "method": "POST",
                "description": "Creates a new customer enrollment with address validation based on ENRREQAD setting",
                "request_example": {
                    "customer": {
                        "firstName": "John",
                        "lastName": "Doe",
                        "email": "john.doe@example.com"
                    },
                    "address": {
                        "line1": "123 Main St",
                        "line2": "Apt 4B",
                        "city": "Anytown",
                        "state": "ST",
                        "zipCode": "12345"
                    },
                    "enrreqad_setting": "TRUE"
                },
                "response_example": {
                    "status": "success",
                    "customerId": "CUST12345",
                    "addressValidation": {
                        "status": "valid",
                        "message": "Address successfully validated"
                    }
                },
                "error_responses": [
                    {
                        "status_code": "400",
                        "error": "invalid_address",
                        "message": "Error: Address format is invalid. Please correct it based on the selected configuration."
                    },
                    {
                        "status_code": "500",
                        "error": "validation_service_error",
                        "message": "Error: Address validation failed. Please try again or contact support for assistance."
                    }
                ]
            },
            {
                "endpoint": "/api/v1/customers/{customerId}/address",
                "method": "PUT",
                "description": "Updates a customer's address with validation based on ENRREQAD setting",
                "request_example": {
                    "address": {
                        "line1": "456 New St",
                        "line2": "Unit 7C",
                        "city": "Othertown",
                        "state": "ST",
                        "zipCode": "98765"
                    },
                    "enrreqad_setting": "TRUE"
                },
                "response_example": {
                    "status": "success",
                    "customerId": "CUST12345",
                    "addressValidation": {
                        "status": "valid",
                        "message": "Address successfully updated and validated"
                    }
                },
                "error_responses": [
                    {
                        "status_code": "400",
                        "error": "invalid_address",
                        "message": "Error: Address format is invalid. Please correct it based on the selected configuration."
                    },
                    {
                        "status_code": "404",
                        "error": "customer_not_found",
                        "message": "Error: Customer not found with the specified ID."
                    }
                ]
            }
        ]
    else:
        # Generic API endpoint if the story doesn't mention ENRREQAD
        return [
            {
                "endpoint": "/api/v1/resource",
                "method": "POST",
                "description": "Creates a new resource",
                "request_example": {
                    "name": "Example Resource",
                    "attributes": {
                        "key1": "value1",
                        "key2": "value2"
                    }
                },
                "response_example": {
                    "id": "resource123",
                    "status": "created",
                    "name": "Example Resource"
                },
                "error_responses": [
                    {
                        "status_code": "400",
                        "error": "invalid_request",
                        "message": "Invalid request data. Please check your input."
                    },
                    {
                        "status_code": "500",
                        "error": "server_error",
                        "message": "Server encountered an error. Please try again later."
                    }
                ]
            }
        ]