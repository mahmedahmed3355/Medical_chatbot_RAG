from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "medical_rag_http_requests_total",
    "Total HTTP requests handled by the Medical RAG application",
    ["method", "endpoint", "status"],
)


REQUEST_LATENCY = Histogram(
    "medical_rag_http_request_duration_seconds",
    "HTTP request latency in seconds for the Medical RAG application",
    ["method", "endpoint"],
)
