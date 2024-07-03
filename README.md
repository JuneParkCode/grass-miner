# GRASS MINER

Selenium based grass (app.getgrass.io) miner.

## How to run?

- I recommend to use docker-compose
    - set environments in `docker-compose.yaml` first, and `docker compose up -d`

## Configuration

### Environments

- **All environment variable values must be set.**
- `GRASS_USER`
    - login id of app.grass.io
- `GRASS_PASSWORD`
    - login password of app.grass.io
- `GRASS_CRX_NAME`
    - extension crx file name in `./data`
        - **Example**
      ```
      data
      └── grass-4.20.2.crx
      ```
        - `GRASS_CRX_NAME=grass-4.20.2.crx`
- `GRASS_CRX_EXTENSION_ID`
    - Grass chrome extension id
    - for example,  `4.20.2` version extension id is
        - `lkbnfiajjmbhnfledhphioinpickokdi`
    - You could get details at `chrome://extensions` with developer mode

## Set extension file

To support community node extension, this app needs crx file.

### Link

- [get from app.getgrass.io](https://app.getgrass.io/dashboard/store/item/extension)
- [direct link (4.20.2, Linux)](https://files.getgrass.io/file/grass-extension-upgrades/extension-latest/grass-community-node-linux-4.20.2.zip)
- You have to unzip the file.

### sh

``` bash
$ curl -o ./data/grass.zip https://files.getgrass.io/file/grass-extension-upgrades/extension-latest/grass-community-node-linux-4.20.2.zip
$ unzip ./data/grass.zip -d .
```

### without docker

The extension file must be located in `./data` directory.

```
.
├── data
│   └── grass-4.20.2.crx <-- MUST BE HERE
├── Dockerfile
├── README.md
├── api.py
├── docker-compose.yaml
├── grass.py
├── main.py
├── prometheus.py
└── requirements.txt

```

### with docker

If you use docker files in this repository, you can map the volume to `/app/data`

#### docker compose example

```docker-compose
version: "3.8"
services:
  grass:
    build: .
    container_name: grass-miner
    restart: on-failure:1
    environment:
      - GRASS_USER=${USER_NAME}
      - GRASS_PASSWORD=${PASSWORD}
      - GRASS_CRX_NAME=${CRX_FILE_NAME}
      - GRASS_CRX_EXTENSION_ID=${EXTENSION_ID}
    ports:
      - "8000:80"
    volumes:
      - ./data:/app/data << NOTE!
```

## API

To check the status of a node, you can get the 'network quality' and 'epoch earning' values through the API.

### Prometheus

- It supports prometheus metric.
    - `grass_network_quality`
        - Gauge
    - `grass_node_earnings`
        - Gauge
    - `grass_time_connected`
        - Gauge
        - converted in minutes.
- `/metrics`

```
... some python metrics...

# HELP grass_network_quality Grass node network quality metrics
# TYPE grass_network_quality gauge
grass_network_quality{ip="ip_address",node_name="grass node name"} {network quality}
# HELP grass_node_earnings Grass node earnings metrics
# TYPE grass_node_earnings gauge
grass_node_earnings{ip="ip_address",node_name="grass node name"} {node epoch earning}
# HELP grass_time_connected Grass node time connected metrics
# TYPE grass_time_connected gauge
grass_time_connected{ip="ip_address",node_name="grass node name"} {time in min}
```

### JSON

- To get metrics in json, request `GET /status`

**RESPONSE**

```json
{
  "time_connected": 95228.0,
  "network_quality": 100.0,
  "node_earnings": 159.47
}
```