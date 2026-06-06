# Практическое задание №2 - Развертывание базового приложения в K8s

## Задание

- Развернуть и настроить K8S
- Подготовить простое REST приложение
- Развернуть приложение, настроив сборку образа в hub.docker.com
- Для настройки использовать Deployment, ConfigMap, Service, Ingress
- Проверить работоспособность

## Введение

Целью практической работы является развертывание базового веб-приложения в кластере Kubernetes с использованием ключевых объектов: Deployment, ConfigMap, Service и Ingress. Приложение написано на Python, читает переменную NAME из ConfigMap и отображает её на HTML-странице. Образ опубликован на Docker Hub. Для локального развертывания использован Kind (Kubernetes in Docker), встроенный в Docker Desktop.

## Ход работы

### Приложение

Написано веб-приложение на Python (app.py), которое читает переменную окружения NAME и возвращает HTML-страницу с её значением в теге h1. Создан Dockerfile для сборки образа на базе python:3.11-slim.

### Сборка и публикация образа

Образ собран и опубликован на Docker Hub командами:

docker build -t ekaterinavol/k8s-hello-app:latest ./k8s-lab/app
docker push ekaterinavol/k8s-hello-app:latest

Образ доступен по адресу: https://hub.docker.com/r/ekaterinavol/k8s-hello-app

### Манифесты

configmap.yml - хранит переменную NAME=Hello, которую приложение читает из окружения.

deployment.yml - запускает контейнер и подключает ConfigMap как переменную окружения.

service.yml - ClusterIP сервис на порту 80, направляет трафик на порт 8080 контейнера.

ingress.yml - внешний доступ через hello-app.local с использованием nginx ingress controller.

### Применение манифестов

kubectl apply -f k8s-lab/k8s/configmap.yml
kubectl apply -f k8s-lab/k8s/deployment.yml
kubectl apply -f k8s-lab/k8s/service.yml
kubectl apply -f k8s-lab/k8s/ingress.yml

### Проверка работоспособности

Все поды запущены:
NAME                         READY   STATUS    RESTARTS   AGE
hello-app-5d77798854-h55sq   1/1     Running   0          2d19h

Сервис создан:
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
hello-app-service   ClusterIP   10.96.160.111   none          80/TCP    2d19h

Ingress настроен и получил адрес:
NAME                CLASS   HOSTS             ADDRESS      PORTS   AGE
hello-app-ingress   nginx   hello-app.local   172.18.0.2   80      2d19h

Проверка через port-forward:
kubectl port-forward service/hello-app-service 9090:80

Приложение доступно по адресу http://localhost:9090 и отображает страницу с текстом Hello, полученным из ConfigMap.

## Вывод

В ходе практической работы было развернуто REST-приложение на Python в кластере Kubernetes (Kind, встроенный в Docker Desktop). Приложение упаковано в Docker-образ и опубликовано на Docker Hub. Созданы и применены манифесты Deployment, ConfigMap, Service и Ingress. Проверка через port-forward подтвердила корректную работу: HTML-страница отображает значение переменной NAME из ConfigMap.