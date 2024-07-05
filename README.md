# GRASS MINER

Selenium based grass (app.getgrass.io) miner.

## How to run?

- I recommend to use docker-compose
    - set environments in `docker-compose.yaml` first, and `docker compose up -d`

## NOTE

- The app.getgrass.io server might be unstable, causing the error. You can fix the problem by retrying to run the
  programme several times.

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
$ cd ./data
$ unzip grass.zip -d .
```

### without docker

The extension file must be located in `./data` directory.

```
.
├── data
│   └── grass-4.20.2.crx <-- MUST BE HERE
├── Dockerfile
└── ...

```

### with docker

If you use docker files in this repository, you can map the volume to `/app/data`

#### docker compose

use .env file. see .env.sample

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

# TYPE grass_network_quality gauge
grass_network_quality{ip="X.X.X.X",node_name="NODE_NAME"} 0.0
# HELP grass_node_earnings Grass node earnings metrics
# TYPE grass_node_earnings gauge
grass_node_earnings{ip="X.X.X.X",node_name="NODE_NAME"} 0.0
# HELP grass_time_connected Grass node time connected metrics
# TYPE grass_time_connected gauge
grass_time_connected{ip="X.X.X.X",node_name="NODE_NAME"} 0.0
```

### JSON

- To get metrics in json, request `GET /status`

**RESPONSE**

```json
{
  "node_name": "node_name",
  "time_connected": 12354.0,
  "network_quality": 100.0,
  "node_earnings": 1347.0
}
```

## Grafana

Sample Grafana dashboard example `/grafana/dashboard.json`
![SC 2024-07-05 at 12 42 23 PM](https://github.com/JuneParkCode/grass-miner/assets/81505228/1b656635-e29c-4836-916e-e4c254ab2ef6)
