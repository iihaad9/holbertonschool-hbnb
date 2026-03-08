🏠 HBnB – Modular Backend Architecture
A structured backend application simulating a simplified Airbnb-like system, designed using clean layered architecture principles.
 
📖 Overview
HBnB is a backend system built with a focus on:
• 
Clear separation of concerns
• 
Scalable architecture
• 
Maintainable code structure
• 
Future-ready persistence layer abstraction
The application follows a layered design pattern to ensure modularity and easy extensibility.
 
🏗️ Architecture
The system is divided into four main layers:
1️⃣ API Layer
Handles HTTP requests and defines application endpoints.
2️⃣ Service Layer (Facade)
Implements the business logic and acts as a single entry point to the system.
3️⃣ Models Layer
Defines domain entities such as User, Place, Review, and Amenity.
4️⃣ Persistence Layer
Abstracts data storage logic using an InMemoryRepository (designed to be replaceable with a real database).
 
 hbnb/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   └── facade.py
│   ├── persistence/
│   │   └── repository.py
├── run.py
├── config.py
├── requirements.txt
└── README.md

📦 Component Description
📌 app/api/
Defines versioned REST endpoints.
📌 app/models/
Contains core domain entities.
📌 app/services/facade.py
Implements HBnBFacade, which:
• 
Coordinates repositories
• 
Applies business rules
• 
Acts as a unified interface for the API layer
📌 app/persistence/repository.py
Provides InMemoryRepository:
• 
Stores data in memory
• 
Abstracts storage mechanism
• 
Designed to be replaced by a database implementation later
📌 run.py
Application entry point.
📌 config.py
Environment and configuration settings.
 
🔄 Design Principles
• 
Layered architecture
• 
Repository pattern
• 
Facade pattern
• 
Separation of concerns
• 
Scalable design
 
🚀 Future Improvements
• 
Replace in-memory storage with a relational database
• 
Add authentication & authorization
• 
Implement input validation
• 
Add automated testing
• 
Containerize using Docker
 
📜 License
This project is for educational purposes.