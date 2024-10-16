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

