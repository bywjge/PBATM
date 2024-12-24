# Prediction of Bus Arrival Times in Macau

## Project Overview
This project aims to predict bus arrival times in Macau.

## Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Setup
1. Add the following line to your crontab to run the crawler every minute:
    ```bash
    * * * * * /home/ubuntu/bus_crontab.sh
    ```

2. Start the Flask backend:
    ```bash
    python Flask_backend.py
    ```

## Usage

Once the setup is complete, the backend will be running and the crawler will update the current bus status for a specific route approximately every five seconds.


To get bus information, you can call the `/bus_info` endpoint with the required parameters. Here is an example using `curl`:

```bash
curl -G http://localhost:8889/bus_info --data-urlencode "route=21A" --data-urlencode "direction=0" --data-urlencode "station=T309"
```

This will return a JSON response with the predicted arrival times for the specified route, direction, and station.


## License
This project is licensed under the MIT License.


