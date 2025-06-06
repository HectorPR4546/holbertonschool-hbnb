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

## Business Entities and Rules

### User
- **Attributes:** `first_name`, `last_name`, `email`, `password`, `is_admin`
- **Actions:** register, update, delete

### Place
- **Attributes:** `title`, `description`, `price`, `latitude`, `longitude`
- **Relationships:** belongs to a user (owner), has many amenities
- **Actions:** create, update, delete, list

### Review
- **Attributes:** `rating`, `comment`
- **Relationships:** belongs to a user and a place
- **Actions:** create, update, delete, list by place

### Amenity
- **Attributes:** `name`, `description`
- **Actions:** create, update, delete, list

> All entities will include a unique `id`, `created_at`, and `updated_at` fields for auditing.

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

## Author

**Hector Perez Velez**  
[HectorPR4546](https://github.com/HectorPR4546)  
Holberton School – Ponce, Puerto Rico  
June 2025
