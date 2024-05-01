# Source

From https://github.com/grafana/tempo/

## OpenTelemetry Collector
This example highlights setting up the OpenTelemetry Collector in a simple tracing pipeline.

1. First start up the stack.

```console
docker compose up -d
```


2. If you're interested you can see the wal/blocks as they are being created.

```console
ls tempo-data/
```

3. Navigate to [Grafana](http://localhost:3000/explore) select the Tempo data source and use the "Search"
tab to find traces. Also notice that you can query Tempo metrics from the Prometheus data source setup in
Grafana.

4. To stop the setup use -

```console
docker compose down -v
```
