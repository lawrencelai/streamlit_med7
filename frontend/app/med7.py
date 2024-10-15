import json

import requests
import streamlit as st
from st_ner_annotate import st_ner_annotate

st.title('Streamlit: Med7 Annotation Site')


def call_api(option, text):
    with st.spinner("waiting"):
        payload = {"type": option, "text": text}
        r = requests.post('http://streamlit_med7-backend-1/analyse', json=payload)
        return r.json()


def main():
    col1, col2 = st.columns(2)
    with col1:
        with st.form("data_form"):
            text = st.text_area(
                "Text to analyze",
                "A patient was prescribed Magnesium hydroxide 400mg/5ml suspension PO of total 30ml bid for the next 5 days.",
                height=300
            )

            option = st.radio(
                "Model?",
                ("med7", "random"),
                horizontal=True, label_visibility="hidden"
            )

            submitted = st.form_submit_button("Submit")
            if submitted:  # Make button a condition.
                st.cache_data.clear()
                if option == "random":
                    st.warning("Random Model is not support yet!")
                else:
                    st.session_state.org_anno = json.loads(call_api(option, text))

    with col2:
        if 'org_anno' in st.session_state:
            entities = st_ner_annotate(["DRUG"], text, st.session_state.org_anno, "42")
            listX = []
            listY = []

            for i in st.session_state.org_anno:
                listX.append(str(i['start']) + str(i['end']))

            for j in entities:
                listY.append(str(j['start']) + str(j['end']))

            tpos = len(set(listX).intersection(listY))

            if len(listY) < len(listX):
                fpos = len(set(listX).union(listY) - set(listX).intersection(listY))
            else:
                fpos = 0

            st.header(f'True Positive :blue[{tpos}]')
            st.header(f'False Positive :red[{fpos}]')
            st.header(f' document precision :blue[{tpos / (tpos + fpos) if (tpos + fpos) else 0}]')


if __name__ == '__main__':
    main()
