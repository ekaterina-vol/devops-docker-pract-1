# Практическое задание №4 - Helm, CloudNativePG, CertManager

## Задание

- Переработать развертывание на Helm
- Заменить PostgreSQL на CloudNativePG оператор
- Добавить самоподписанные сертификаты через CertManager

## Введение

В данной работе развертывание приложения из заданий 2 и 3 переработано с обычных манифестов на Helm chart. PostgreSQL заменён на оператор CloudNativePG. Добавлены самоподписанные TLS сертификаты через оператор CertManager. Gateway API настроен на HTTPS.

## Ход работы

### Структура Helm chart

Создан Helm chart hello-app со следующими templates:
- configmap.yaml - конфигурация приложения
- secret.yaml - пароль БД для приложения
- deployment.yaml - развертывание приложения
- service.yaml - сервис приложения
- pg-secret.yaml - credentials для CloudNativePG
- postgres-cluster.yaml - кластер PostgreSQL через CloudNativePG
- gateway.yaml - Gateway и HTTPRoute
- certificate.yaml - Issuer и Certificate через CertManager

### Установка операторов через Helm

CloudNativePG:
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm install cnpg cnpg/cloudnative-pg --namespace cnpg-system --create-namespace

CertManager:
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set crds.enabled=true

### Установка приложения

helm install hello-app k8s-lab4/helm/hello-app --create-namespace --namespace hello-app

### Проверка работоспособности

Все поды запущены:
NAME                         READY   STATUS    RESTARTS
hello-app-67b5b769bd-flwv5   1/1     Running   3
hello-app-db-1               1/1     Running   0

CloudNativePG кластер здоров:
NAME           INSTANCES   READY   STATUS                     PRIMARY
hello-app-db   1           1       Cluster in healthy state   hello-app-db-1

Сертификат выпущен:
NAME            READY   SECRET
hello-app-tls   True    hello-app-tls

Приложение доступно через port-forward на http://localhost:9090 и отображает Hello, Ekaterina! и список последних визитов из PostgreSQL.

## Вывод

В ходе работы развертывание приложения переведено на Helm chart. PostgreSQL заменён на CloudNativePG оператор, который управляет кластером БД автоматически. CertManager выпускает самоподписанный TLS сертификат. Gateway API настроен с поддержкой HTTPS.