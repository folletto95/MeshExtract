# MeshExtract

This project provides tools for collecting and viewing data from the Meshsense API.

## Components

* `fetch_data.py` – Script that downloads node data from the Meshsense API and stores it in a local SQLite database (`data.db`). Configure the API endpoint and token via the environment variables `MESHSENSE_API_URL` and `MESHSENSE_API_TOKEN`.
* `app.py` – A simple Flask web server that exposes a page to filter and view the stored data.
* `Dockerfile` – Build definition for running the web interface in a container.

## Usage

1. **Build the container**

   ```bash
   docker build -t meshextract .
   ```

2. **Run data extraction**

   ```bash
   docker run --rm -e MESHSENSE_API_URL=<url> -e MESHSENSE_API_TOKEN=<token> \
       -v $(pwd)/data.db:/app/data.db meshextract python fetch_data.py
   ```

   The command above contacts the Meshsense API and writes the results to `data.db` in the current directory.

3. **Start the web interface**

   ```bash
   docker run -p 5000:5000 -v $(pwd)/data.db:/app/data.db meshextract
   ```

   Once running, open `http://localhost:5000` in a browser to filter and view the stored node data.

The provided `templates/index.html` page allows filtering by node ID, date range, hop count and whether the data came via MQTT.
