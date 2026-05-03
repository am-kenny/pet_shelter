# Pet Shelter Management System

This project is a Django-based web application developed for managing a pet shelter. The application includes features for managing pets, users, and a blog for posting updates about the shelter.

## Features

- **Pet Management**: Add, edit, and track the pets in the shelter.
- **Blog**: Post updates and information related to the shelter.
- **Feedbacks**: User feedbacks
- **Scheduling**: Reliable scheduling system to select a timeslot.

## Technologies Used

- **Backend**: Django (Python)
- **Package manager**: [uv](https://docs.astral.sh/uv/) (lockfile: `uv.lock`)
- **Frontend**: Django templates, HTML, CSS, JS
- **Database**: PostgreSQL
- **Containerization**: Docker

## Setup and Installation

To run this project locally, follow the steps below:

### Python version

- Use Python 3.12 for local development.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/am-kenny/pet_shelter.git
    cd pet_shelter
    ```

2. **Install dependencies with uv** (install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed):

    ```bash
    uv sync
    ```

    Run Django commands through uv so they use the project environment, for example:

    ```bash
    uv run python manage.py migrate
    uv run python manage.py runserver
    ```

3. **Run the stack with Docker Compose (development only)** — [`docker-compose.yml`](docker-compose.yml) bind-mounts your working tree for live code, stores dependencies in a **`django_venv`** volume at **`/app/.venv`** (so the mount does not replace the image’s virtualenv), then runs **`migrate`** and **`runserver`**. Do **not** treat this compose file as a production deployment.

    ```bash
    docker compose up --build -d
    ```

    After changing **`pyproject.toml`** or **`uv.lock`**, rebuild the web image and recreate the venv volume so the container picks up new packages:

    ```bash
    docker compose build web_app
    docker volume rm pet_shelter_django_venv
    docker compose up -d
    ```

    **Fixture data (one-time):** [`seed_data.json`](seed_data.json). After the stack is up and migrations have applied, load it once if you need seed data:

    ```bash
    docker compose exec web_app python manage.py loaddata seed_data.json
    ```

**4. Access the application:**

   Open your browser and go to `http://localhost:8000`.

## Usage

- Add pets and update shelter information through the admin interface.
- Post shelter updates using the blog feature.
- Manage user roles for staff and administrators via the Django admin panel.
- Manage scheduled slots for pets

## License

This project is licensed under the [MIT License](LICENSE).
