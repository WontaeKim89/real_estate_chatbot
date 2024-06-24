import base
import subprocess
from vector_db.es_settings import index_dataframe_to_elasticsearch

def run_streamlit():
    subprocess.call("streamlit run ./run_streamlit.py", shell=True)

if __name__ == "__main__":
    index_dataframe_to_elasticsearch()
    run_streamlit()