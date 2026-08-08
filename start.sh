#!/bin/bash
# Set PYTHONPATH to the current directory so absolute imports like 'email_module' work correctly
export PYTHONPATH=.

# Start the Flask OAuth server in the background
python email_module/oauth/server.py &

# Start the Streamlit app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.fileWatcherType none --server.enableCORS=false --server.enableXsrfProtection=false
