FROM python:latest

EXPOSE 8000

WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

LABEL authors="Andrii"

# Run the app
#CMD python manage.py runserver 0.0.0.0:8000

# to create image use:
# docker build -t dish_ordering-app .

# to create container use:
# docker run -it --rm --name dish_ordering-running-app dish_ordering-app
