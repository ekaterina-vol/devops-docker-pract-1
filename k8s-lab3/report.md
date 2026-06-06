# Практическое задание №3 - PostgreSQL и Gateway API в K8s

## Задание

- Доработать приложение для работы с PostgreSQL
- Развернуть PostgreSQL в K8s через StatefulSet + Volume
- Перевести приложение на Gateway API вместо Ingress

## Введение

В данной работе приложение из задания №2 доработано: добавлена работа с базой данных PostgreSQL. Приложение сохраняет время каждого визита в БД и отображает последние 10 визитов на странице. PostgreSQL развёрнут через StatefulSet с персистентным хранилищем. Вместо Ingress использован Gateway API с NGINX Gateway Fabric.

## Ход работы

### Доработка приложения

Приложение на Python дополнено:
- подключением к PostgreSQL через библиотеку psycopg2
- созданием таблицы visits при старте
- записью времени каждого визита в БД
- отображением последних 10 визитов на HTML-странице

### PostgreSQL в Kubernetes

Для развёртывания PostgreSQL использованы:

postgres-secret.yml - хранит credentials (DB, USER, PASSWORD) в зашифрованном виде

postgres-service.yml - ClusterIP сервис для доступа к БД внутри кластера

postgres-statefulset.yml - StatefulSet с одной репликой и PersistentVolumeClaim на 1Gi для хранения данных

### Gateway API

Вместо Ingress использован Gateway API. Установлен NGINX Gateway Fabric. Созданы три ресурса:

GatewayClass - определяет контроллер nginx
Gateway - слушает порт 80
HTTPRoute - маршрутизирует трафик на hello-app-service

### Проверка работоспособности

Все поды запущены:
NAME                         READY   STATUS    RESTARTS
hello-app-6d5954fc55-jlzqb   1/1     Running   3
postgres-0                   1/1     Running   0

Gateway настроен:
NAME            CLASS   ADDRESS   PROGRAMMED
hello-gateway   nginx             True

Приложение доступно через port-forward на http://localhost:9090 и отображает Hello, Ekaterina! и список последних визитов из PostgreSQL.

## Вывод

В ходе работы приложение доработано для работы с PostgreSQL. База данных развёрнута через StatefulSet с персистентным хранилищем. Вместо Ingress настроен Gateway API через NGINX Gateway Fabric. Приложение корректно сохраняет и отображает данные из БД.