FROM python:3.10
ADD ./requirements.txt .
COPY ./exile_tools_poc /app
RUN pip install -r requirements.txt
CMD cd exile_tools_poc && ./manage.py runserver