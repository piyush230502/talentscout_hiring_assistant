FROM python:3.9.23

WORKDIR /app

COPY . . 
 
RUN pip install -r requirements.txt

CMD ["python", "streamlit run app.py"]