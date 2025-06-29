## Notes
- IF YOU JUST NEED EXISTING DATA: unzip the relevant event and move it into the "data" directory


## Features

- **Data collector:** A python project using FastF1 to extract telemetry data per drive, per event
- **.NET API** WIP for analyizing results and running prediction models

## Tech Stack

- [Docker](https://www.docker.com/get-started/) - Docker
- [NET](https://dotnet.microsoft.com/en-us/download) - .NET 8
- [Python](https://www.python.org/downloads/) - Python 3.10.10
- [venv](https://packaging.python.org/en/latest/guides/) - venv 20.16.5
- [TimescaleDB](https://github.com/timescale/timescaledb) - Timescale DB (Postgres)

## Getting Started
# API
- Create .env file in the  "Web" directory root and create values for: RacingDBUsername, RacingDBPassword, RacingDBName, RacingDBPort, RacingDBHost
- Run in Visual studio or use "docker compose up -d"
# Python project
- Create a venv project
- With the venv active, in the "python/src" directory run "pip install -r requirements"
- In Visual studio run main.py or "python ./main.py"
# Existing Data
- The "events" folder has zipped files of events which have already been extracted
### Prerequisites
- [Docker](https://www.docker.com/get-started/) - Docker
- [NET](https://dotnet.microsoft.com/en-us/download) - .NET 8
- [Python](https://www.python.org/downloads/) - Python 3.10.10
- [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) - venv 20.16.5