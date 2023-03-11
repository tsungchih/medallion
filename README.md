# Medallion

A layered data design pattern is a modern data architecture for building ETL/ELT data pipelines comprised of multiple stages so that each stage processes the data and improves the quality of the data progressively. Compared to the imperative way how data engineers build ETL/ELT data pipelines in the last decade, layered data architecture could be of great help in improving data quality steadily and progressively, and reducing data silos while project-specific teams are autonomously producing various data products.

This project is aimed at implementing a technical solution based on layered data architecture by means of [Dagster](https://dagster.io), a cloud-native data orchestrator with integrated lineage, observability, and a declarative programming model. 

