FROM python:3.13

WORKDIR /wikicards

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "bot.py"]