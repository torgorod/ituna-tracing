from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import config

config = config.get_config()

resource = Resource(attributes={
    "service.name": "ituna-tracing"
})

otlp_exporter = OTLPSpanExporter(
    endpoint=f"http://{config.get('jaeger-exporter', 'host')}:{config.get('jaeger-exporter', 'port')}/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(span_processor)

trace.set_tracer_provider(tracer_provider)


def get_tracer(name):
    return trace.get_tracer(name)
