FROM python:3.10
ADD ./exile_tools_poc .
RUN pip install -r requirements.txt
CMD cd exile_tools_poc && ./manage.py runserver