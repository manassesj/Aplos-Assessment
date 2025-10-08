#!/bin/bash
python3 src/generate_data.py
python3 src/etl_pipeline.py
python3 src/insights.py
