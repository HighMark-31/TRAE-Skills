# Skill: Refactoring Legacy Controller

## Purpose
To modernize and clean up "fat controllers" by extracting business logic into services, improving readability, and making the code testable.

## When to Use
- When a controller file exceeds ~200 lines or handles too many responsibilities.
- When logic is duplicated across multiple controllers.
- When unit testing the controller is difficult due to mixed concerns.

## Procedure
1.  **Analyze Responsibilities**: Identify validation, business logic, data access, and response formatting mixed in the controller.
2.  **Extract Service Layer**:
    - Create a Service class/module for the business domain (e.g., `UserService`).
    - Move business logic and DB calls to the Service.
3.  **Extract Validation**: Move input validation to middleware or a separate validator helper.
4.  **Refine Controller**:
    - The controller should only:
        1. Parse request.
        2. Call Service method.
        3. Send response based on result.
5.  **Update Tests**: Create/Update unit tests for the new Service and integration tests for the Controller.

## Constraints
- Ensure functionality remains exactly the same (refactoring, not rewriting).
- Do not pass `req` or `res` objects into the Service layer (keep it framework-agnostic).
- Handle errors consistently (throw in Service, catch in Controller/Middleware).

## Expected Output
A slim controller file and a corresponding service file containing the business logic, improving maintainability and testability.
