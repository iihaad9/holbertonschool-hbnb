# HBnB Evolution - High-Level Package Diagram (Task 0)

## Overview
This diagram shows the **three-layer architecture** of the HBnB application:
- **Presentation Layer**: API endpoints + services (what the client talks to)
- **Business Logic Layer**: core domain models and application rules
- **Persistence Layer**: repositories / database access

A **Facade** is used as the single entry point from Presentation to Business Logic.

---

## Package Diagram (Mermaid)

```mermaid
classDiagram
direction TB

class PresentationLayer {
  <<package>>
  +API
  +Services
}

class BusinessLogicLayer {
  <<package>>
  +Facade
  +User
  +Place
  +Review
  +Amenity
}

class PersistenceLayer {
  <<package>>
  +Repositories
  +Database
}

PresentationLayer --> BusinessLogicLayer : calls Facade
BusinessLogicLayer --> PersistenceLayer : CRUD operations
PersistenceLayer --> BusinessLogicLayer : returns data
