FROM python:3.9-slim AS builder
ARG PROJECT_NAME

COPY .. /${PROJECT_NAME}/
RUN pip install --upgrade pip build \
    && python -m build /${PROJECT_NAME}


FROM python:3.9-slim
ARG PROJECT_NAME

COPY --from=builder /${PROJECT_NAME}/dist/*.whl ./
RUN pip install --upgrade pip \
    && pip install ./*.whl \
    && rm -rf /root/.cache

EXPOSE 4266
