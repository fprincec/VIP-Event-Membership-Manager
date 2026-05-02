[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Ic9iTi2K)

# VIP Event & Membership Manager

This project is a full stack web application for managing VIP organization members, events, and event registrations.

The project follows a three-tier architecture:

- UI: Node.js, Express, and EJS
- REST API Services: Python Flask
- Database: AWS RDS MySQL

## Project Structure

final-project-fprincec/
  backend/
    app.py
    db.py
    schema.sql
    requirements.txt
  frontend/
    server.js
    package.json
    views/
    public/
  video-link.txt
  README.md

Sprint 1 Backend
The backend is located in the backend folder.
The backend provides REST API routes for:
members
events
registrations
viewing members registered for a selected event
To run the backend:
cd backend
source .venv/bin/activate
python3 app.py
The backend runs on:
http://127.0.0.1:5000

Sprint 2 Frontend
The frontend is located in the frontend folder.
The frontend was created with Node.js, Express, and EJS. It communicates with the Flask backend API.
To run the frontend:
cd frontend
npm install
npm start
The frontend runs on:
http://localhost:3000

Main Features
Dashboard showing total members, events, and registrations
Create, update, and delete members
Create, update, and delete events
Register members for events using dropdowns
Delete registrations
Select an event and view the members registered for that event
Uses dropdowns instead of requiring users to type member or event names manually
Uses the backend API to communicate with the database

Business Rules:
The application follows these rules:
Gold events can only be attended by Gold members.
Silver events can be attended by Silver or Gold members.
Bronze events can be attended by Bronze, Silver, or Gold members.
A member cannot register for the same event more than once.
A member cannot register for an event that is already at capacity.
Two events cannot have the same date.

Presentation Video
The Sprint 2 presentation video link is included in the video-link.txt file.
