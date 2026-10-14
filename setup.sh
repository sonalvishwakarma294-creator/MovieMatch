mkdir -p ~/.streamlit/

echo "\
[server]\nheadless = true
port = $PORT
enableCORS = false

[browser]
gatherUsageStats = false
" > ~/.streamlit/config.toml

# Optional: create credentials file if needed
# echo "\
# [general]\n# email = \"\"\n# " > ~/.streamlit/credentials.toml
