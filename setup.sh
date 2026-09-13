mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS =false\n\
headless = true\n\
\n\
<<<<<<< HEAD
" > ~/.streamlit/config.toml
=======
" > ~/.streamlit/config.toml
>>>>>>> cef88523e2c65bdf9c8914abd55d13c0ff11098b
