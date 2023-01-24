# README

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker

### Environment Variables

- REPLICATE_API_TOKEN

### Installing

1. Clone the repository
`git clone https://github.com/<username>/<projectname>.git`

2. Build the Docker image
`docker build -t <image-name> .`

3. Run the Docker container
`docker run -p 8000:8000 -e REPLICATE_API_TOKEN=<your-api-token> <image-name>`


## Usage
You can test the API endpoint by sending a POST request to `http://localhost:8000/process-image/` with a `multipart/form-data` payload containing the image file with key `image`.

`curl -X POST "http://localhost:8000/process-image/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "image=@/path/to/image.jpg"`
