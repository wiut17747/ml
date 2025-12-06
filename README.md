# New York Housing Price Forecasting

Student ID: 00017747

## Setup (works on Mac/Windows/Linux)
```bash
python -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
pip install ipykernel
python -m ipykernel install --user --name=.venv
```
To launch dashboard locally, please run:  

streamlit run app.py

## Streamlit deployed link

https://ny00017747.streamlit.app

### Note 
Before running jupyter notebook, please install libomp lib first, using curl or homebrew on a mac.

```bash
brew install libomp
```