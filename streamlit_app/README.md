# ITEA Dashboard

Interactive dashboard for the ITEA Framework v1.45 (Triple Exposure to Automation Index).

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repo (or add to `Aval22/ITEA`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select the repo and `app.py` as the main file
5. Deploy

## Local development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files

- `app.py` — Main Streamlit application
- `itea_data.csv` — 1,016 occupations with 8 indicators
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — Theme configuration
