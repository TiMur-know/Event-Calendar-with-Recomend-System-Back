# Calendar App Backend

This is the backend for the Calendar App, built with Flask.

## Features

- RESTful API for calendar events
- User authentication (JWT)
- CRUD operations for events
- SQLite/PostgreSQL support

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/TiMur-know/Event-Calendar-with-Recomend-System-Back.git
cd calendar-app-backend
python -m venv venv
source venv/bin/activate
pipenv install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and update settings as needed.

### Running the Server

```bash
flask run
```

## API Endpoints

| Method | Endpoint         | Description           |
|--------|------------------|----------------------|
| POST   | /auth/register   | Register user        |
| POST   | /auth/login      | Login user           |
| GET    | /events          | List all events      |
| POST   | /events          | Create new event     |
| PUT    | /events/<id>     | Update event         |
| DELETE | /events/<id>     | Delete event         |

## License

MIT
