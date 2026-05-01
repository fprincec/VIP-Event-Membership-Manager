// From lines 2 to 69, I asked ChatGPT how to create an Express and EJS frontend server that connects to my Flask REST API.

const express = require("express"); // This line imports Express, which is used to create the frontend web server.
const path = require("path"); // This line imports the path module, which helps build safe file paths.
const axios = require("axios"); // This line imports Axios, which is used to send HTTP requests to the Flask backend API.

const app = express(); // This line creates an Express application and stores it in the variable app.
const PORT = 3000; // This line sets the port number where the frontend server will run.
const API_BASE_URL = "http://127.0.0.1:5000"; // This line stores the base URL for the Flask backend API.

app.set("view engine", "ejs"); // This line tells Express to use EJS as the template engine.
app.set("views", path.join(__dirname, "views")); // This line tells Express where the EJS view files are located.

app.use(express.urlencoded({ extended: true })); // This line allows Express to read form data submitted from HTML forms.
app.use(express.json()); // This line allows Express to read JSON data if needed.
app.use(express.static(path.join(__dirname, "public"))); // This line allows Express to serve static files like CSS from the public folder.

app.get("/", async (req, res) => { // This line creates a GET route for the home page.
    try { // This line starts a try block to catch any errors from the API requests.
        const membersResponse = await axios.get(`${API_BASE_URL}/members`); // This line gets all members from the Flask backend.
        const eventsResponse = await axios.get(`${API_BASE_URL}/events`); // This line gets all events from the Flask backend.
        const registrationsResponse = await axios.get(`${API_BASE_URL}/registrations`); // This line gets all registrations from the Flask backend.

        res.render("index", { // This line renders the index.ejs page and sends data to it.
            members: membersResponse.data, // This line sends the members list to the home page.
            events: eventsResponse.data, // This line sends the events list to the home page.
            registrations: registrationsResponse.data // This line sends the registrations list to the home page.
        });
    } catch (error) { // This line catches errors if the Flask backend cannot be reached.
        res.render("index", { // This line still renders the home page even if there is an error.
            members: [], // This line sends an empty members list if the API request fails.
            events: [], // This line sends an empty events list if the API request fails.
            registrations: [], // This line sends an empty registrations list if the API request fails.
            error: "Could not connect to the Flask backend. Make sure the backend is running on port 5000." // This line sends an error message to the page.
        });
    }
});

app.get("/members", async (req, res) => { // This line creates a GET route for the members page.
    try { // This line starts a try block to handle possible API errors.
        const response = await axios.get(`${API_BASE_URL}/members`); // This line requests all members from the backend.
        res.render("members", { members: response.data }); // This line renders members.ejs and sends the members data to the page.
    } catch (error) { // This line catches errors if the members cannot be loaded.
        res.render("members", { members: [], error: "Could not load members from the backend." }); // This line renders the page with an error message.
    }
});

app.get("/events", async (req, res) => { // This line creates a GET route for the events page.
    try { // This line starts a try block to handle possible API errors.
        const response = await axios.get(`${API_BASE_URL}/events`); // This line requests all events from the backend.
        res.render("events", { events: response.data }); // This line renders events.ejs and sends the events data to the page.
    } catch (error) { // This line catches errors if the events cannot be loaded.
        res.render("events", { events: [], error: "Could not load events from the backend." }); // This line renders the page with an error message.
    }
});

app.get("/registrations", async (req, res) => { // This line creates a GET route for the registrations page.
    try { // This line starts a try block to handle possible API errors.
        const membersResponse = await axios.get(`${API_BASE_URL}/members`); // This line requests all members for the registration dropdown.
        const eventsResponse = await axios.get(`${API_BASE_URL}/events`); // This line requests all events for the registration dropdown.
        const registrationsResponse = await axios.get(`${API_BASE_URL}/registrations`); // This line requests all registrations from the backend.

        res.render("registrations", { // This line renders registrations.ejs and sends all needed data.
            members: membersResponse.data, // This line sends members to the registration page.
            events: eventsResponse.data, // This line sends events to the registration page.
            registrations: registrationsResponse.data // This line sends registrations to the registration page.
        });
    } catch (error) { // This line catches errors if any registration data cannot be loaded.
        res.render("registrations", { members: [], events: [], registrations: [], error: "Could not load registration data from the backend." }); // This line renders the page with empty lists and an error.
    }
});

app.listen(PORT, () => { // This line starts the frontend server.
    console.log(`Frontend server running at http://localhost:${PORT}`); // This line prints the frontend URL in the terminal.
});