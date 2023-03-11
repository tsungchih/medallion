FROM python:3.9-slim AS builder

COPY .. /medallion-weather/
RUN pip install --upgrade pip build \
    && python -m build /medallion-weather


FROM python:3.9-slim

COPY --from=builder /medallion-weather/dist/*.whl ./
RUN pip install --upgrade pip \
    && pip install ./*.whl \
    && rm -rf /root/.cache

EXPOSE 4266
