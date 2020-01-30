#!/bin/bash
gunicorn app:server --bind=:8050 --workers=5 --threads=3