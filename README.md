# Recommendation System

This project implements a **hybrid recommendation system** that combines **Collaborative Filtering**, **Content-Based Filtering**, and **Alternating Least Squares (ALS)** to provide personalized product recommendations to users. The system is designed to be scalable and easily deployable.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Algorithms](#algorithms)
5. [Data](#data)
6. [Setup and Installation](#setup-and-installation)
7. [Usage](#usage)
8. [Output](#output)
9. [Contributing](#contributing)
10. [License](#license)

---

## Overview

The recommendation system is built to provide personalized product recommendations to users based on their past interactions and item metadata. It combines:
- **Collaborative Filtering**: Uses user-item interactions to find similar users or items.
- **Content-Based Filtering**: Uses item metadata (e.g., descriptions, categories) to recommend similar items.
- **ALS (Alternating Least Squares)**: A matrix factorization algorithm for collaborative filtering.

The system is implemented in Python using **PySpark** for scalability and **Scikit-learn** for content-based filtering.

---

## Features

- **Hybrid Recommendations**: Combines collaborative and content-based filtering for better accuracy.
- **Scalable**: Uses PySpark for distributed computing, making it suitable for large datasets.
- **User-Friendly Output**: Displays recommendations with item details (name, category, description) in a clean, tabular format.
- **Customizable**: Supports tuning of hyperparameters for ALS and other algorithms.

---

## Technologies Used

- **Python**: Primary programming language.
- **PySpark**: For distributed computing and ALS implementation.
- **Scikit-learn**: For content-based filtering (TF-IDF and cosine similarity).
- **Pandas** and **NumPy**: For data manipulation.
- **Tabulate**: For pretty-printing tables in the console.

---

## Algorithms

### 1. Collaborative Filtering with ALS
- Uses Alternating Least Squares (ALS) to factorize the user-item interaction matrix.
- Predicts missing ratings and recommends items with the highest predicted ratings.

### 2. Content-Based Filtering
- Uses TF-IDF to vectorize item descriptions.
- Computes cosine similarity between items to recommend similar products.

### 3. Hybrid Recommendations
- Combines recommendations from collaborative filtering and content-based filtering.
- Ensures diverse and personalized recommendations.
### 4. Real-Time Processing
- Utilizes Apache Kafka for streaming user interactions.
### 5. Cloud Integration
- Incorporates Google Cloud Recommendations AI for managed recommendations.
### 6. Advanced Embeddings
- Uses Sentence-BERT for semantic understanding of item descriptions.
### 7. Evaluation and Monitoring
- Includes Precision@K, Recall@K, NDCG, and MLflow for logging experiment parameters and tracking.
---

## Data

The system uses two datasets:
1. **`user_item_interactions.csv`**:
   - Contains user-item interactions (e.g., ratings).
   - Columns: `user_id`, `item_id`, `rating`.

2. **`item_metadata.csv`**:
   - Contains metadata for items (e.g., descriptions, categories).
   - Columns: `item_id`, `category`, `description`.

<mark>Dummy datasets are generated for testing. Replace them with real data for production use.</mark>

---

## Setup and Installation

### Prerequisites
- Python>=3.9
- Java>=8 (required for PySpark)
- pyspark>=3.3.0
- scikit-learn>=1.0.0
- numpy>=1.21.0
- pandas>=1.3.0
- sentence-transformers>=2.2.0
- kafka-python>=2.0.0
- mlflow>=1.0.0
- tabulate>=0.8.0
---

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recommendation-system.git
   cd recommendation-system
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Download and install Apache Spark
   - Set the SPARK_HOME environment variable:
   ```bash
   export SPARK_HOME=/path/to/spark
   export PATH=$SPARK_HOME/bin:$PATH
4. Setting Up Kafka Locally
   - Download Kafka from the [official website](https://kafka.apache.org/downloads).
   - Extract the downloaded file:
   ```bash
   tar -xzf kafka_2.13-3.2.1.tgz
   cd kafka_2.13-3.2.1
   ```
   - Start Zookeeper:
   ```bash
   .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
   ```
   - Start Kafka Broker:
   ```bash
   .\bin\windows\kafka-server-start.bat .\config\server.properties
   ```
   - Create a Topic:
   ```bash
   .\bin\windows\kafka-topics.bat --create --topic recommendations --bootstrap-server localhost:9092 --partitions 1 --      replication-factor 1
   ```
5. Run the script:
   ```bash
   python main.py
---

## Usage
The script generates recommendations and displays them in the console. Here's how to interpret the output:

1. Collaborative Filtering Recommendations:
   - Displays top recommendations for each user based on their past interactions.
   - Includes item details (ID, category, description) and predicted ratings.

2. Content-Based Recommendations:
   - Displays items similar to a given item based on their descriptions.
   - Includes item details (ID, category, description).

3. Hybrid Recommendations:
   - Combines collaborative and content-based recommendations.
   - Displays a diverse set of recommendations for a given user and item.
---

## Output
### Example Outputs
- Collaborative Filtering Recommendations
  ```bash
  ======================================================================
  Collaborative Filtering Recommendations:
  ======================================================================

  User 1 Recommendations:
  +---------+-----------+----------------------+-------------------+
  | item_id |  category |     description      | predicted_rating  |
  +---------+-----------+----------------------+-------------------+
  |   12    | Electronics | Description for item 12 |       4.5       |
  |   25    | Books      | Description for item 25 |       4.3       |
  |   34    | Clothing   | Description for item 34 |       4.2       |
  |   45    | Home       | Description for item 45 |       4.1       |
  |   18    | Sports     | Description for item 18 |       4.0       |
  +---------+-----------+----------------------+-------------------+
  ...
  ======================================================================
- Content-Based Recommendations
  ```bash
  ======================================================================
  Content-Based Recommendations for Item 1:
  ======================================================================
  +---------+-----------+----------------------+
  | item_id |  category |     description      |
  +---------+-----------+----------------------+
  |   12    | Electronics | Description for item 12 |
  |   25    | Books      | Description for item 25 |
  |   34    | Clothing   | Description for item 34 |
  |   45    | Home       | Description for item 45 |
  |   18    | Sports     | Description for item 18 |
  +---------+-----------+----------------------+
  ======================================================================
- Hybrid Recommendations
  ```bash
  ======================================================================
  Hybrid Recommendations for User 1 and Item 1:
  ======================================================================
  +---------+-----------+----------------------+
  | item_id |  category |     description      |
  +---------+-----------+----------------------+
  |   12    | Electronics | Description for item 12 |
  |   25    | Books      | Description for item 25 |
  |   34    | Clothing   | Description for item 34 |
  |   45    | Home       | Description for item 45 |
  |   18    | Sports     | Description for item 18 |
  |    7    | Electronics | Description for item 7  |
  |   56    | Clothing   | Description for item 56 |
  |   23    | Books      | Description for item 23 |
  |   89    | Home       | Description for item 89 |
  |   14    | Sports     | Description for item 14 |
  +---------+-----------+----------------------+
  ======================================================================
- Kafka Consumer Output
```bash
{
  "item_id": 12,
  "category": "Electronics",
  "description": "Description for item 12"
}
{
  "item_id": 25,
  "category": "Books",
  "description": "Description for item 25"
}
{
  "item_id": 34,
  "category": "Clothing",
  "description": "Description for item 34"
}
...
```
- MLflow Tracking Output
```bash
INFO:mlflow:=== Run (ID: abc123) ===
INFO:mlflow:Parameters:
  num_users: 100
  num_items: 50
INFO:mlflow:Metrics:
  precision@10: 0.85
INFO:mlflow:Model saved at: /path/to/als_model
```
---

### Summary of outputs:
1. Collaborative Filtering: Displays top recommendations for each user with predicted ratings.
2. Content-Based Filtering: Shows items similar to a given item based on descriptions.
3. Hybrid Recommendations: Combines collaborative and content-based recommendations.
4. Kafka Producer: Logs successful message sending to Kafka.
5. Kafka Consumer: Displays recommendations in real-time.
6. MLflow Tracking: Logs experiment parameters, metrics, and model artifacts.
---

## Contributing
### Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
5. Open a pull request.
---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
---

## Acknowledgments
- Apache Spark for providing the ALS implementation.
- Scikit-learn for content-based filtering tools.
- Tabulate for pretty-printing tables in the console.
