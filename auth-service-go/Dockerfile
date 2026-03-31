FROM golang:1.23-alpine

WORKDIR /app

# Копируем go.mod и go.sum
COPY go.mod go.sum ./
RUN go mod download

# Копируем весь код (включая cmd и internal)
COPY . .

# Компилируем, указывая путь к main.go в папке cmd
RUN go build -o main ./cmd/...

EXPOSE 8081

CMD ["./main"]