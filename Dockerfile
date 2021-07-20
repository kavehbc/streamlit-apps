# docker build --progress=plain --no-cache -t fun-apps .
# docker save -o fun-apps.tar fun-apps
# docker load --input fun-apps.tar

FROM python:3.8-buster

LABEL version="1.0.5"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/fun-games"
LABEL description="Streamlit Fun Apps"

WORKDIR /app
COPY . .

# installing the requirements
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]