import pandas as pd
from PIL import Image
import base64
import json
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from streamlit.server.server import Server
from streamlit.report_thread import get_report_ctx
import asyncio

current_session_id = get_report_ctx().session_id
st_status = st.empty()
st_update_flag = False


def all_sessions():
    all_session_ids = []
    session_infos = Server.get_current()._session_info_by_id.values()
    for session_info in session_infos:
        all_session_ids.append(session_info.session.id)
    return all_session_ids


@st.cache(allow_output_mutation=True)
def whiteboard_data():
    return {"1": {}}


async def watch(selected_session_id):
    global st_status
    global st_update_flag
    while True:
        json_whiteboard = whiteboard_data()
        init_drawing = st.session_state.whiteboard.copy()

        if selected_session_id in json_whiteboard:
            cached_whiteboard = json_whiteboard[selected_session_id].copy()
            if init_drawing != cached_whiteboard and not st_update_flag:
                st_status.info("Update is available.")
                st_update_flag = True
                # st.experimental_rerun()
        _ = await asyncio.sleep(1)


def whiteboard():
    json_whiteboard = whiteboard_data()

    st.write(f"Your current Session ID: {current_session_id}")
    selected_session_id = st.selectbox("Session ID",
                                       options=all_sessions())

    if selected_session_id == current_session_id:

        # Specify canvas parameters in application
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("Stroke color hex: ")
        bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
        # bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
        dr_json = st.sidebar.file_uploader("Drawing JSON:", type=["json"])
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
        )
        realtime_update = st.sidebar.checkbox("Update in realtime", True)

        # Create a canvas component
        init_drawing = None
        if dr_json:
            dic_dr_json = json.loads(dr_json.read())
        else:
            dic_dr_json = None

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            # background_image=Image.open(bg_image) if bg_image else None,
            update_streamlit=realtime_update,
            height=500,
            drawing_mode=drawing_mode,
            initial_drawing=dic_dr_json,
            key="canvas",
        )

        if canvas_result.json_data is not None:
            json_whiteboard[selected_session_id] = canvas_result.json_data.copy()
            st.session_state.whiteboard = canvas_result.json_data.copy()
            # st.dataframe(pd.json_normalize(canvas_result.json_data["objects"]))

            encoded_data = json.dumps(canvas_result.json_data, indent=2).encode('utf-8')
            b64 = base64.b64encode(encoded_data).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="drawing.json">Download Drawing</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        if selected_session_id in json_whiteboard:
            init_drawing = json_whiteboard[selected_session_id].copy()
            st.session_state.whiteboard = init_drawing.copy()

            plh_temp = st.empty()
            with plh_temp:
                temp_canvas = st_canvas(initial_drawing=init_drawing, key="temp_canvas")

            st.image(temp_canvas.image_data)
            with plh_temp:
                st.empty()

            # st.write(json_whiteboard[selected_session_id])
            asyncio.run(watch(selected_session_id))


if __name__ == '__main__':
    whiteboard()
