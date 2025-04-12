from src.dev_pilot.ui.streamlit_ui.streamlit_app import load_app as load_streamlit_app
from src.dev_pilot.api.fastapi_app import load_app as load_fastapi_app


if __name__=="__main__":
    load_streamlit_app() ## Streamlit UI App
    # load_fastapi_app() ## FastAPI App