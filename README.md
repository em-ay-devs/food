# food

[![CircleCI](https://circleci.com/gh/em-ay-devs/food.svg?style=svg)](https://circleci.com/gh/em-ay-devs/food)

A service for helping Connexta developers at the MA office with the very difficult task of deciding on a place to get lunch from 😵🤕.

## Usage
By default, the service will run on port `5000`. To make the service accessible from outside networks, you can use a tool like [ngrok](https://ngrok.com/) to create a public URL and point it to your chosen port.
1. Build the Docker image
    ```bash
    docker build -t em-ay-devs-food -f Dockerfile .
    ```
2. Create and start the container in the background
    ```bash
    docker run -d -p 5000:5000 --name food em-ay-devs-food
    ```
    - To stop the container:
        ```bash
        docker stop food
        ```
        
## Testing

Unit tests are located in the `tests/` directory. To execute only the tests and get the results, simply run `pytest` in your terminal. If you want a more detailed output with coverage measurements, run the following:
```bash
pytest -v --cov-report term --cov=src tests/
```
