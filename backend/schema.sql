-- From lines 3 to 27, I asked ChatGPT how to create the database schema for the event registration system.

CREATE TABLE IF NOT EXISTS member ( -- This line creates a table named 'member' if it doesn't already exist
  id INT AUTO_INCREMENT PRIMARY KEY, -- This line defines an 'id' column as an integer that auto-increments and serves as the primary key
  name VARCHAR(100) NOT NULL, -- This line defines a 'name' column as a variable character string with a maximum length of 100 characters and it cannot be null
  details TEXT, -- This line defines a 'details' column as a text field that can store longer strings of text
  title VARCHAR(100), -- This line defines a 'title' column as a variable character string with a maximum length of 100 characters
  level ENUM('Bronze','Silver','Gold') NOT NULL -- This line defines a 'level' column as an enumeration that can only take the values 'Bronze', 'Silver', or 'Gold' and it cannot be null
);

CREATE TABLE IF NOT EXISTS event ( -- This line creates a table named 'event' if it doesn't already exist
  id INT AUTO_INCREMENT PRIMARY KEY, -- This line defines an 'id' column as an integer that auto-increments and serves as the primary key
  name VARCHAR(120) NOT NULL, -- this line defines a 'name' column as a variable character string with a maximum length of 120 characters and it cannot be null
  capacity INT NOT NULL, -- This line defines a 'capacity' column as an integer that cannot be null
  level ENUM('Bronze','Silver','Gold') NOT NULL, -- This line defines a 'level' column as an enumeration that can only take the values 'Bronze', 'Silver', or 'Gold' and it cannot be null
  date DATE NOT NULL, -- This line defines a 'date' column as a date type that cannot be null
  CONSTRAINT uq_event_date UNIQUE (date) -- This line adds a unique constraint on the 'date' column, ensuring that no two events can have the same date
);

CREATE TABLE IF NOT EXISTS registration ( -- This line creates a table named 'registration' if it doesn't already exist
  id INT AUTO_INCREMENT PRIMARY KEY, -- This line defines an 'id' column as an integer that auto-increments and serves as the primary key
  event_id INT NOT NULL, -- This line defines an 'event_id' column as an integer that cannot be null, which will be used to reference the 'event' table
  member_id INT NOT NULL, -- This line defines a 'member_id' column as an integer that cannot be null, which will be used to reference the 'member' table
  CONSTRAINT fk_reg_event FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE, -- This line adds a foreign key constraint on the 'event_id' column, referencing the 'id' column of the 'event' table. The 'ON DELETE CASCADE' clause means that if an event is deleted, all associated registrations will also be deleted.
  CONSTRAINT fk_reg_member FOREIGN KEY (member_id) REFERENCES member(id) ON DELETE CASCADE, -- This line adds a foreign key constraint on the 'member_id' column, referencing the 'id' column of the 'member' table. The 'ON DELETE CASCADE' clause means that if a member is deleted, all associated registrations will also be deleted.
  CONSTRAINT uq_reg_event_member UNIQUE (event_id, member_id) -- This line adds a unique constraint on the combination of 'event_id' and 'member_id', ensuring that a member can only register for a specific event once
);