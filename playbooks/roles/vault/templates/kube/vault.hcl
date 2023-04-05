api_addr = "http://127.0.0.1:8200"
disable_mlock = true

{% if vault_raft_storage == false %}
storage "file" {
    path = "/vault/data"
}
{% else %}
storage "raft" {
    path = "/vault/data"
    node_id = "raft_node_1"
}
{% endif%}

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
