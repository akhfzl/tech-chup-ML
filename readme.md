Step by step:
1. create environment with "py -m venv myenv"
2. activate your environment
3. install all dependencies with "pip install requirements.txt"
4. open cmd 2 tabs, because the apps are running on local
5. run "uvicorn api_py:app --host 0.0.0.0 --port 8000" for backend
6. run "streamlit run streamlite_py.py"