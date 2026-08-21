from app.application import app


def test_request_id_is_generated():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_existing_request_id_is_preserved():
    client = app.test_client()

    request_id = "test-request-id-123"

    response = client.get(
        "/health",
        headers={
            "X-Request-ID": request_id,
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


def test_metrics_endpoint_returns_prometheus_metrics():
    client = app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"medical_rag_http_requests_total" in response.data
    assert b"medical_rag_http_request_duration_seconds" in response.data


def test_health_request_is_recorded_in_metrics():
    client = app.test_client()

    client.get("/health")

    response = client.get("/metrics")

    assert response.status_code == 200

    metrics_text = response.data.decode()

    assert "medical_rag_http_requests_total" in metrics_text
