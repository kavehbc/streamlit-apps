# docker build --progress=plain --no-cache -t kavehbc/streamlit-apps .
# docker save -o streamlit-apps.tar kavehbc/streamlit-apps
# docker load --input streamlit-apps.tar

FROM python:3.8-buster

LABEL version="1.0.5"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/streamlit-apps"
LABEL description="Streamlit Fun Apps"

WORKDIR /app
COPY . .

# installing the requirements
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]