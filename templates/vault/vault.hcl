api_addr = "http://127.0.0.1:8200"
disable_mlock = true

storage "file" {
  path = "/vault/data"
}

storage_destination "raft" {
    path = "/opt/vault/data"
    node_id = "raft_node_1"
}

listener "tcp" {
    address = "0.0.0.0:8200"
    #tls_cert_file = "/config/server.crt"
    #tls_key_file = "/config/server.key"
    tls_disable = 1
    scheme = "http"
    ui = true
}

telemetry {
  prometheus_retention_time = "90s"
  disable_hostname = true
  unauthenticated_metrics_access = true
}
