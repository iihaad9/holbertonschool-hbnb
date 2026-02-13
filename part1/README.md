HBnB Evolution – Technical Documentation

Part 1: System Architecture and Design
1. Introduction

This document provides the technical documentation for HBnB Evolution, a simplified AirBnB-like application.
The purpose of this document is to describe the system architecture, core business entities, and the interaction flow between components.

This documentation serves as a blueprint for the implementation phases of the project and ensures a shared understanding of the system design among team members.

⸻

2. High-Level Architecture

HBnB Evolution follows a layered architecture composed of three main layers:
	1.	Presentation Layer
	2.	Business Logic Layer
	3.	Persistence Layer

The communication between layers is simplified using the Facade Pattern, which provides a unified interface between layers and reduces coupling.

Responsibilities of Each Layer
	•	Presentation Layer
Handles user interaction through APIs and services. It receives requests and sends responses.
	•	Business Logic Layer
Contains the core models and rules of the application such as Users, Places, Reviews, and Amenities.
	•	Persistence Layer
Responsible for storing and retrieving data from the database.
classDiagram
class PresentationLayer {
    <<Interface>>
    +API
    +Services
}

class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
}

class PersistenceLayer {
    +Repository
    +DatabaseAccess
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Data Persistence
3. Business Logic Layer – Class Diagram

The Business Logic Layer contains the core entities of the system:
	•	User
	•	Place
	•	Review
	•	Amenity

Each entity:
	•	Has a unique ID
	•	Tracks creation and update timestamps
classDiagram
class BaseEntity {
    +id
    +created_at
    +updated_at
}

class User {
    +first_name
    +last_name
    +email
    +password
    +is_admin
    +create()
    +update()
    +delete()
}

class Place {
    +title
    +description
    +price
    +latitude
    +longitude
    +create()
    +update()
    +delete()
}

class Review {
    +rating
    +comment
    +create()
    +update()
    +delete()
}

class Amenity {
    +name
    +description
    +create()
    +update()
    +delete()
}

BaseEntity <|-- User
BaseEntity <|-- Place
BaseEntity <|-- Review
BaseEntity <|-- Amenity

User "1" --> "many" Place : owns
User "1" --> "many" Review : writes
Place "1" --> "many" Review : has
Place "many" --> "many" Amenity : includes
Entity Explanations
	•	User
Represents a system user. Users can be regular users or administrators.
	•	Place
Represents a property listed by a user. A place can have multiple amenities and reviews.
	•	Review
Represents feedback left by a user for a specific place.
	•	Amenity
Represents a feature that can be associated with multiple places.
4. API Interaction Flow – Sequence Diagrams

4.1 User Registration
sequenceDiagram
User ->> API: Register Request
API ->> BusinessLogic: validateUser()
BusinessLogic ->> Persistence: saveUser()
Persistence -->> BusinessLogic: success
BusinessLogic -->> API: userCreated
API -->> User: Response
4.2 Place Creation
sequenceDiagram
User ->> API: Create Place
API ->> BusinessLogic: validatePlace()
BusinessLogic ->> Persistence: savePlace()
Persistence -->> BusinessLogic: success
BusinessLogic -->> API: placeCreated
API -->> User: Response
4.3 Review Submission
sequenceDiagram
User ->> API: Submit Review
API ->> BusinessLogic: validateReview()
BusinessLogic ->> Persistence: saveReview()
Persistence -->> BusinessLogic: success
BusinessLogic -->> API: reviewCreated
API -->> User: Response
4.4 Fetch List of Places
sequenceDiagram
User ->> API: Get Places
API ->> BusinessLogic: getPlaces()
BusinessLogic ->> Persistence: fetchPlaces()
Persistence -->> BusinessLogic: placesList
BusinessLogic -->> API: placesList
API -->> User: Response
5. Design Decisions


	•	Layered Architecture was chosen to separate concerns and improve maintainability.
	•	Facade Pattern simplifies communication between layers.
	•	Associations in UML are used instead of IDs to clearly express relationships, even if IDs are used in implementation.
	•	BaseEntity is used to avoid duplication of shared attributes like ID and timestamps.





6. Conclusion


This document defines the architecture and design of the HBnB Evolution application.
It provides a clear understanding of system components, their relationships, and the flow of data between layers.

This technical documentation will guide the implementation phases and serve as a reference throughout the project lifecycle.