# Pet Shelter Management System

This project is a Django-based web application developed for managing a pet shelter. The application includes features for managing pets, users, and a blog for posting updates about the shelter.

## Features

- **Pet Management**: Add, edit, and track the pets in the shelter.
- **Blog**: Post updates and information related to the shelter.
- **Feedbacks**: User feedbacks
- **Scheduling**: Reliable scheduling system to select a timeslot.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: Django templates, HTML, CSS, JS
- **Database**: PostgreSQL
- **Containerization**: Docker

## Setup and Installation

To run this project locally, follow the steps below:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/am-kenny/pet_shelter.git
    cd pet_shelter
    ```

2. **Build and start the Docker containers:**

    ```bash
    docker-compose up --build
    ```
Note: [docker-compose.yml](docker-compose.yml)  includes application container, database container, migration and test data loading scripts.

**4. Access the application:**

   Open your browser and go to `http://localhost:8000`.

## Usage

- Add pets and update shelter information through the admin interface.
- Post shelter updates using the blog feature.
- Manage user roles for staff and administrators via the Django admin panel.
- Manage scheduled slots for pets

## License

This project is licensed under the [MIT License](LICENSE). See the
