# HBnB Evolution – Part 1: Technical Documentation

## Description
This directory contains the technical documentation for Part 1 of the HBnB Evolution project.
The goal of this part is to design and document the system architecture, business logic,
and interactions using UML diagrams.

## Contents
- High-Level Package Diagram
- Detailed Class Diagram for the Business Logic Layer
- Sequence Diagrams for API interactions

## Tasks
- **Task 0:** High-Level Package Diagram  
  Illustrates the three-layer architecture (Presentation, Business Logic, Persistence)
  and their communication using the Facade pattern.

## Tools
- UML
- Mermaid.js

## Authors
HBnB Team
uml

---

## Task 1: Detailed Class Diagram for Business Logic Layer

### Overview
This diagram represents the core business logic entities of the HBnB Evolution application,
including their attributes, methods, and relationships.

```mermaid
classDiagram
direction TB

class BaseEntity {
  +UUID id
  +datetime created_at
  +datetime updated_at
}

class User {
  +string first_name
  +string last_name
  +string email
  +string password
  +bool is_admin
  +create()
  +update()
  +delete()
}

class Place {
  +string title
  +string description
  +float price
  +float latitude
  +float longitude
  +create()
  +update()
  +delete()
}

class Review {
  +int rating
  +string comment
  +create()
  +update()
  +delete()
}

class Amenity {
  +string name
  +string description
  +create()
  +update()
  +delete()
}

BaseEntity <|-- User
BaseEntity <|-- Place
BaseEntity <|-- Review
BaseEntity <|-- Amenity

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" -- "0..*" Amenity : includes

