# HBnB Evolution - Technical Documentation

## Overview

This repository contains the technical documentation for the **HBnB Evolution** project, a simplified AirBnB-like application. The goal of this phase is to define the system's architecture and design before development begins. This includes structural diagrams and behavior modeling to provide a clear blueprint for future implementation.

## Objective

Develop a comprehensive set of diagrams and design artifacts to:

- Illustrate the system architecture
- Define the core business logic
- Model key user interactions
- Support alignment across all development phases

---

## Problem Scope

The HBnB Evolution platform will support the following features:

### User Management
- Register and manage user profiles
- Distinguish between regular users and administrators

### Place Management
- List properties with details: title, description, price, coordinates
- Associate properties with amenities and owners

### Review Management
- Submit ratings and comments linked to users and places

### Amenity Management
- Create and manage a catalog of amenities

---

## Architectural Overview

The system is structured into three primary layers:

1. **Presentation Layer** – User interaction through APIs or services
2. **Business Logic Layer** – Models and core functionality
3. **Persistence Layer** – Handles data storage and retrieval

> The **Facade Pattern** is used to coordinate interactions between layers.

---

## Deliverables

### 1. High-Level Package Diagram
- Illustrates the layered architecture and the facade communication flow

### 2. Class Diagram (Business Logic Layer)
- Defines `User`, `Place`, `Review`, and `Amenity` classes with attributes, methods, and associations

### 3. Sequence Diagrams
- Visualizes flow for core API calls:
  - User registration
  - Place creation
  - Review submission
  - Fetching a list of places

### 4. Documentation Compilation
- Complete technical report with all diagrams and explanations

---

## Part 2: Enhanced Backend with Authentication and Database Integration

Part 2 focuses on enhancing the backend of the HBnB application by introducing user authentication, authorization, and database integration using SQLAlchemy and SQLite for development. It also prepares the application for MySQL in production environments.

Key features implemented in this part include:

- **JWT-based Authentication:** Secure user login and access to protected endpoints.
- **Role-Based Access Control (RBAC):** Differentiating between regular users and administrators.
- **SQLAlchemy Integration:** Transitioning from in-memory storage to a persistent database.
- **Entity-Relationship Mapping:** Defining models for User, Place, Review, and Amenity with their relationships.
- **SQL Scripts:** Generating database schema and populating initial data.
- **Database Diagrams:** Visualizing the database structure using Mermaid.js.

**Important Note:** All development and implementation for Part 2 were carried out within the `part2` directory. The `part3` directory serves as a final copy of the completed work for this section of the project.

## Part 4: Simple Web Client

Part 4 focuses on the front-end development of the HBnB application, creating an interactive user interface that connects with the backend services. This part utilizes HTML5, CSS3, and JavaScript ES6 to build a dynamic web application.

Key features implemented in this part include:

- **User-Friendly Interface:** Designed and implemented pages for Login, List of Places, Place Details, and Add Review.
- **Client-Side Functionality:** Implemented interactions with the backend API using Fetch API.
- **Session Management:** Handled JWT token storage in cookies for user sessions.
- **Dynamic Content:** Populated and filtered data dynamically without page reloads.

## Author

**Hector Perez Velez**  
[HectorPR4546](https://github.com/HectorPR4546)  
Holberton School – Ponce, Puerto Rico  
June 2025