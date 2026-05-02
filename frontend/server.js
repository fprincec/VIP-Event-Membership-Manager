// From lines 2 to 60, 94 to 101, I asked ChatGPT how to create an Express and EJS frontend server that connects to my Flask REST API.

const express = require("express"); // This line imports Express, which is used to create the frontend web server.
const path = require("path"); // This line imports the path module, which helps build safe file paths.
const axios = require("axios"); // This line imports Axios, which is used to send HTTP requests to the Flask backend API.

const app = express(); // This line creates an Express application and stores it in the variable app.
const PORT = 3000; // This line sets the port number where the frontend server will run.
const API_BASE_URL = "http://127.0.0.1:5000"; // This line stores the base URL for the Flask backend API.

function formatDateForInput(dateValue) { // This function converts backend date values into the format required by HTML date inputs.
    if (!dateValue) { // This line checks if the date value is empty or missing.
        return ""; // This line returns an empty string if there is no date.
    }

    const date = new Date(dateValue); // This line creates a JavaScript Date object from the backend date value.

    if (isNaN(date.getTime())) { // This line checks if JavaScript could not understand the date.
        return dateValue.toString().substring(0, 10); // This line uses the first 10 characters as a backup format.
    }

    return date.toISOString().substring(0, 10); // This line returns the date in YYYY-MM-DD format for the HTML date input.
}

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

// From lines 62 - 123, I asked ChatGPT how to create Express routes that let my EJS frontend create, update, and delete members by communicating with my Flask REST API.
app.post("/members/create", async (req, res) => { // This line creates a POST route that runs when the user submits the add member form.
    try { // This line starts a try block to handle possible errors.
        const memberData = { // This line creates an object containing the member data from the form.
            name: req.body.name, // This line gets the member name from the submitted form.
            details: req.body.details, // This line gets the member details from the submitted form.
            title: req.body.title, // This line gets the member title from the submitted form.
            level: req.body.level // This line gets the member level from the submitted form.
        };

        await axios.post(`${API_BASE_URL}/members`, memberData); // This line sends the new member data to the Flask backend.
        res.redirect("/members"); // This line sends the user back to the members page after the member is created.
    } catch (error) { // This line catches any error that happens during the API request.
        res.redirect("/members"); // This line sends the user back to the members page if something goes wrong.
    }
});

app.post("/members/update", async (req, res) => { // This line creates a POST route that runs when the user submits an update member form.
    try { // This line starts a try block to handle possible errors.
        const memberId = req.body.member_id; // This line gets the hidden member id from the form so the backend knows which member to update.

        const memberData = { // This line creates an object containing the updated member data.
            name: req.body.name, // This line gets the updated member name from the form.
            details: req.body.details, // This line gets the updated member details from the form.
            title: req.body.title, // This line gets the updated member title from the form.
            level: req.body.level // This line gets the updated member level from the form.
        };

        await axios.put(`${API_BASE_URL}/members/${memberId}`, memberData); // This line sends the updated member data to the Flask backend.
        res.redirect("/members"); // This line sends the user back to the members page after updating.
    } catch (error) { // This line catches any error that happens during the update request.
        res.redirect("/members"); // This line sends the user back to the members page if something goes wrong.
    }
});

app.post("/members/delete", async (req, res) => { // This line creates a POST route that runs when the user clicks a delete button.
    try { // This line starts a try block to handle possible errors.
        const memberId = req.body.member_id; // This line gets the hidden member id from the form.

        await axios.delete(`${API_BASE_URL}/members/${memberId}`); // This line sends a delete request to the Flask backend for the selected member.
        res.redirect("/members"); // This line sends the user back to the members page after deleting.
    } catch (error) { // This line catches any error that happens during the delete request.
        res.redirect("/members"); // This line sends the user back to the members page if something goes wrong.
    }
});

app.get("/events", async (req, res) => { // This line creates a GET route for the events page.
    try { // This line starts a try block to handle possible API errors.
        const response = await axios.get(`${API_BASE_URL}/events`); // This line requests all events from the backend.

        const events = response.data.map(event => { // This line loops through each event and prepares the date for the form.
            return { // This line returns a cleaned-up event object.
                ...event, // This line keeps all the original event data.
                formattedDate: formatDateForInput(event.date) // This line adds a properly formatted date value for the HTML date input.
            };
        });

        res.render("events", { events: events }); // This line renders events.ejs and sends the cleaned event data to the page.
    } catch (error) { // This line catches errors if the events cannot be loaded.
        res.render("events", { events: [], error: "Could not load events from the backend." }); // This line renders the page with an error message.
    }
});

// From lines 125 to 169, I asked ChatGPT how to create Express routes that let my EJS frontend create, update, and delete events by communicating with my Flask REST API.
app.post("/events/create", async (req, res) => { // This line creates a POST route that runs when the user submits the add event form.
    try { // This line starts a try block to handle possible errors.
        const eventData = { // This line creates an object containing the event data from the form.
            name: req.body.name, // This line gets the event name from the submitted form.
            capacity: req.body.capacity, // This line gets the event capacity from the submitted form.
            level: req.body.level, // This line gets the event level from the submitted form.
            date: req.body.date // This line gets the event date from the submitted form.
        };

        await axios.post(`${API_BASE_URL}/events`, eventData); // This line sends the new event data to the Flask backend.
        res.redirect("/events"); // This line sends the user back to the events page after the event is created.
    } catch (error) { // This line catches any error that happens during the API request.
        res.redirect("/events"); // This line sends the user back to the events page if something goes wrong.
    }
});

app.post("/events/update", async (req, res) => { // This line creates a POST route that runs when the user submits an update event form.
    try { // This line starts a try block to handle possible errors.
        const eventId = req.body.event_id; // This line gets the hidden event id from the form so the backend knows which event to update.

        const eventData = { // This line creates an object containing the updated event data.
            name: req.body.name, // This line gets the updated event name from the form.
            capacity: req.body.capacity, // This line gets the updated event capacity from the form.
            level: req.body.level, // This line gets the updated event level from the form.
            date: req.body.date // This line gets the updated event date from the form.
        };

        await axios.put(`${API_BASE_URL}/events/${eventId}`, eventData); // This line sends the updated event data to the Flask backend.
        res.redirect("/events"); // This line sends the user back to the events page after updating.
    } catch (error) { // This line catches any error that happens during the update request.
        res.redirect("/events"); // This line sends the user back to the events page if something goes wrong.
    }
});

app.post("/events/delete", async (req, res) => { // This line creates a POST route that runs when the user clicks a delete button.
    try { // This line starts a try block to handle possible errors.
        const eventId = req.body.event_id; // This line gets the hidden event id from the form.

        await axios.delete(`${API_BASE_URL}/events/${eventId}`); // This line sends a delete request to the Flask backend for the selected event.
        res.redirect("/events"); // This line sends the user back to the events page after deleting.
    } catch (error) { // This line catches any error that happens during the delete request.
        res.redirect("/events"); // This line sends the user back to the events page if something goes wrong.
    }
});

// From lines 173 to 229, I asked ChatGPT how to create a registration page route that loads members, events, registrations, and selected event members from my Flask API.
app.get("/registrations", async (req, res) => { // This line creates a GET route for the registrations page.
    try { // This line starts a try block to handle possible API errors.
        const selectedEventId = req.query.event_id; // This line gets the selected event id from the page URL if the user selected an event.

        const membersResponse = await axios.get(`${API_BASE_URL}/members`); // This line requests all members for the member dropdown.
        const eventsResponse = await axios.get(`${API_BASE_URL}/events`); // This line requests all events for the event dropdown.
        const registrationsResponse = await axios.get(`${API_BASE_URL}/registrations`); // This line requests all registrations from the backend.

        const members = membersResponse.data; // This line stores the members list in a variable.
        const events = eventsResponse.data; // This line stores the events list in a variable.
        const registrations = registrationsResponse.data.map(registration => { // This line loops through registrations and adds readable member and event names.
            const member = members.find(member => member.id === registration.member_id); // This line finds the member connected to the registration.
            const event = events.find(event => event.id === registration.event_id); // This line finds the event connected to the registration.

            return { // This line returns a cleaned registration object for the page.
                id: registration.id, // This line keeps the registration id for hidden form actions only.
                memberName: member ? member.name : "Unknown Member", // This line stores the member name for display.
                eventName: event ? event.name : "Unknown Event", // This line stores the event name for display.
                eventLevel: event ? event.level : "Unknown", // This line stores the event level for display.
                eventDate: event ? formatDateForInput(event.date) : "" // This line stores the formatted event date for display.
            };
        });

        let selectedEventMembers = []; // This line creates an empty list for members registered for the selected event.
        let selectedEventName = ""; // This line creates an empty variable for the selected event name.

        if (selectedEventId) { // This line checks if the user selected an event.
            const selectedEvent = events.find(event => event.id == selectedEventId); // This line finds the selected event in the events list.
            selectedEventName = selectedEvent ? selectedEvent.name : ""; // This line stores the selected event name if it exists.

            const eventMembersResponse = await axios.get(`${API_BASE_URL}/events/${selectedEventId}/members`); // This line requests members registered for the selected event.
            selectedEventMembers = eventMembersResponse.data; // This line stores the selected event members from the backend.
        }

        res.render("registrations", { // This line renders the registrations.ejs page.
            members: members, // This line sends all members to the page.
            events: events, // This line sends all events to the page.
            registrations: registrations, // This line sends readable registrations to the page.
            selectedEventId: selectedEventId, // This line sends the selected event id for the dropdown.
            selectedEventName: selectedEventName, // This line sends the selected event name for the heading.
            selectedEventMembers: selectedEventMembers // This line sends the members registered for the selected event.
        });
    } catch (error) { // This line catches errors if registration data cannot be loaded.
        res.render("registrations", { // This line still renders the page if there is an error.
            members: [], // This line sends an empty members list.
            events: [], // This line sends an empty events list.
            registrations: [], // This line sends an empty registrations list.
            selectedEventId: "", // This line sends an empty selected event id.
            selectedEventName: "", // This line sends an empty selected event name.
            selectedEventMembers: [], // This line sends an empty selected event members list.
            error: "Could not load registration data from the backend." // This line sends an error message to the page.
        });
    }
});

// From lines 228 to 255, I asked ChatGPT how to create Express routes that let my EJS frontend create and delete registrations by communicating with my Flask REST API.
app.post("/registrations/create", async (req, res) => { // This line creates a POST route that runs when the user submits the add registration form.
    try { // This line starts a try block to handle possible errors.
        const registrationData = { // This line creates an object containing the registration data from the form.
            event_id: req.body.event_id, // This line gets the selected event id from the event dropdown.
            member_id: req.body.member_id // This line gets the selected member id from the member dropdown.
        };

        await axios.post(`${API_BASE_URL}/registrations`, registrationData); // This line sends the new registration data to the Flask backend.
        res.redirect("/registrations"); // This line sends the user back to the registrations page after creating the registration.
    } catch (error) { // This line catches any error that happens during the API request.
        res.redirect("/registrations"); // This line sends the user back to the registrations page if something goes wrong.
    }
});

app.post("/registrations/delete", async (req, res) => { // This line creates a POST route that runs when the user clicks a delete registration button.
    try { // This line starts a try block to handle possible errors.
        const registrationId = req.body.registration_id; // This line gets the hidden registration id from the form.

        await axios.delete(`${API_BASE_URL}/registrations/${registrationId}`); // This line sends a delete request to the Flask backend for the selected registration.
        res.redirect("/registrations"); // This line sends the user back to the registrations page after deleting.
    } catch (error) { // This line catches any error that happens during the delete request.
        res.redirect("/registrations"); // This line sends the user back to the registrations page if something goes wrong.
    }
});

app.listen(PORT, () => { // This line starts the frontend server.
    console.log(`Frontend server running at http://localhost:${PORT}`); // This line prints the frontend URL in the terminal.
});