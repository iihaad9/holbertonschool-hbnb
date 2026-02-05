# Task 1: Detailed Class Diagram for Business Logic Layer

## Overview
This document describes the core business logic entities of the HBnB Evolution application.
It includes their attributes, methods, and relationships.

## Class Diagram

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
