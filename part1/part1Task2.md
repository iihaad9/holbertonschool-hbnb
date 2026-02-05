# Task 2: Sequence Diagrams for API Calls

## 1) User Registration (POST /users)
```mermaid
sequenceDiagram
actor Client
participant API as Presentation(API)
participant Facade as Business(HBnBFacade)
participant UserRepo as Persistence(UserRepository)
participant DB as Database

Client->>API: POST /users (user data)
API->>Facade: register_user(data)
Facade->>UserRepo: create(data)
UserRepo->>DB: INSERT user
DB-->>UserRepo: user saved
UserRepo-->>Facade: user entity
Facade-->>API: user DTO
API-->>Client: 201 Created (user)
