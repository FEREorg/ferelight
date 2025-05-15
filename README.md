# FERElight | ˈferēlīt |
[![pypi](https://img.shields.io/pypi/v/ferelight.svg)](https://pypi.org/project/ferelight/)

Extremely lightweight and purpose-built feature extraction and retrieval engine (FERE).

## Installation

### From PyPI
```
pip install ferelight
```

### From Source
```
pip install git+https://github.com/FEREorg/ferelight.git
```

## Usage
To configure the pgvector PostgreSQL connection, create a file `config.json` in the root directory with the following content:

```json
{
  "DBHOST": "<host>",
  "DBPORT": "<port>",
  "DBUSER": "<user>",
  "DBPASSWORD": "<password>"
}
```

To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m ferelight
```

You can also specify a custom path to the configuration file:

```
python3 -m ferelight --config /path/to/your/config.json
# or using the short option
python3 -m ferelight -c /path/to/your/config.json
```

## Running with Docker

### Using Docker Hub

The Docker image is available on Docker Hub. You can pull and run it directly:

```bash
docker pull florianspiess/ferelight:latest
docker run -p 8080:8080 florianspiess/ferelight:latest
```

### Building Locally

To build and run the server on a Docker container locally, execute the following from the root directory:

```bash
# building the image
docker build -t ferelight .

# starting up a container
docker run -p 8080:8080 ferelight
```

## Development

### Releasing New Versions

To release a new version:

1. Update the version number in `ferelight/__init__.py`
2. Create a new GitHub release or tag with a version number (e.g., `v1.0.1`)
3. The GitHub Actions workflows will automatically:
   - Build and publish the package to PyPI
   - Build and publish the Docker image to Docker Hub (as both `latest` and version-specific tags)
