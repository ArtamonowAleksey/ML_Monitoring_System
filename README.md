# House-Prices-Airflow-XGBoost-Superset
---
### Цель данного проекта - Попрактиковаться в разворачивание Docker,обучение ML моделей,объединение всех действий в оркестратор Airflow.
---
Пояснения к диаграмме:
1. Data Generator - Создает синтетические данные на основе модели **SDV** и **House Prices** датасета
2. Data Transform - Используются различные преобразователи данных: **MinMaxScaler**,**OrdinalEncoder**,**SimpleImputer**,которые были получены во время обучения самой модели **XGBoost**
3. XGBRegressor - Обученная модель **XGBoost** на датасете **House Prices**
---
- Рабочие файлы находятся в папке [**Airflow_Docker**](https://github.com/ArtamonowAleksey/House-Prices-Airflow-Superset/tree/main/Airflow_Docker)
- Обучения модели и различные артефакты в папке [**Training Models And Test**](https://github.com/ArtamonowAleksey/House-Prices-Airflow-Superset/tree/main/Training%20Models%20And%20Test)

![Slide 16_9 - 1 (1)](https://github.com/user-attachments/assets/241e054c-5203-4e60-944a-b922f04db5c2)

---
### Следующие шаги по проекту
1. Добавить новый генератор синтетических данных
2. Добавить проверки на входящие данные
3. Добавить **Kafka**
4. Подключить **Streamleet** для управления входящим потоком данных
   - Генераций кол-ва входящих данных
   - Генерация аномальных данных
   - Генерация данных на которых не обучалась модель
5. Добавить аллерты в **телеграмм** по данным
6. Расширить **EDA** по модели
7. Добавить автоматическое переобучение модели
