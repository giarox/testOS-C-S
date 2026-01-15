FROM python:3.11-slim

WORKDIR /app

COPY docs/ /app/

ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "python -m http.server ${PORT} --directory /app"]
