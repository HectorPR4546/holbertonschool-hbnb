# HBnB UML Diagrams – Task Folder

This directory contains all the **Mermaid diagrams** developed as part of the technical documentation for the **HBnB Evolution** project. Each `.mmd` file corresponds to a specific task in the documentation phase.

## Folder Contents

### 🗂 Task 0 – High-Level Package Diagram
- **File:** `Task 0.mmd`
- **Description:**  
  Represents the overall architecture of the application, illustrating the three-layered structure:
  - Presentation Layer
  - Business Logic Layer
  - Persistence Layer  
  The diagram also shows how these layers interact using the **Facade Pattern**.

---

### 🗂 Task 1 – Class Diagram for Business Logic Layer
- **File:** `Task 1.mmd`
- **Description:**  
  A detailed UML class diagram showing the core entities:
  - `User`
  - `Place`
  - `Review`
  - `Amenity`  
  Includes attributes, methods, and relationships such as ownership and associations (e.g., places having amenities).

---

### 🗂 Task 2 – Sequence Diagrams for API Calls

#### 🔹 Task 2.1 – User Registration
- **File:** `Task 2 User Registration.mmd`
- **Description:**  
  Sequence diagram showing the interaction between layers when a new user registers.

#### 🔹 Task 2.2 – Place Creation
- **File:** `Task 2_2 Place Creation.mmd`
- **Description:**  
  Models the steps and component interactions for creating a new place listing.

#### 🔹 Task 2.3 – Review Submission
- **File:** `Task 2_3 Review Submission.mmd`
- **Description:**  
  Captures the flow of submitting a review, linking users and places.

#### 🔹 Task 2.4 – Fetching a List of Places
- **File:** `Task 2_4 Fetching a List of Places.mmd`
- **Description:**  
  Describes how a user retrieves a list of available places from the system.

---

## How to View

You can preview these `.mmd` Mermaid diagrams:

- **On GitHub** using compatible browser extensions like *Mermaid Live Preview*.
- **Using [Mermaid Live Editor](https://mermaid.live/edit)** – Paste the file contents to render the diagram.
- **With VS Code** by installing the *"Markdown Preview Mermaid Support"* or *"Live Preview"* extensions.

---

## Author

**Hector Perez Velez**  
[HectorPR4546](https://github.com/HectorPR4546)  
Holberton School – Ponce, Puerto Rico  
June 2025
