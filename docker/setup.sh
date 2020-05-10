#!/bin/bash

export PORT=${PORT:-'8501'}

mkdir -p ~/.streamlit/
echo -e "\
[general]\\n\
email = \"restless_project@hotmail.es\"\n\
" > ~/.streamlit/credentials.toml
echo -e "\
[server]\n\
headless=true\n\
enableCORS=false\n\
port=$PORT\n\
" > ~/.streamlit/config.toml
