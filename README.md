# Hybrid Recommendation System with Machine Learning

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

This is a simple build for a hybrid recommendation system that combines collaborative filtering, content-based filtering, and real-time processing to deliver personalized product recommendations. The system is designed to handle large datasets using PySpark and provides interpretable, user-friendly outputs. It integrates Apache Kafka for real-time streaming of recommendations and uses Sentence-BERT for advanced semantic understanding of item descriptions. The system is modular, scalable, and ready for deployment in real-world applications like e-commerce or streaming platforms.

---

## Features

- **Hybrid Recommendations:** Combines collaborative and content-based filtering for diverse and accurate suggestions.
- **Real-Time Processing:** Uses Apache Kafka to stream recommendations in real-time.
- **Scalability:** Leverages PySpark for distributed computing, making it suitable for large datasets.
- **Advanced Embeddings:** Uses Sentence-BERT for semantic understanding of item descriptions.
- **User-Friendly Output:** Displays recommendations with item details (name, category, description) in a clean, tabular format.
- **Experiment Tracking:** Uses MLflow to log parameters, metrics, and model artifacts for reproducibility.

---

## Technologies Used

- **Python:** Primary programming language.
- **PySpark:** For distributed computing and ALS implementation.
- **Scikit-learn:** For content-based filtering (TF-IDF and cosine similarity).
- **Sentence-BERT:** For advanced semantic understanding of item descriptions.
- **Apache Kafka:** For real-time streaming of recommendations.
- **MLflow:** For experiment tracking and model management.
- **Pandas and NumPy:** For data manipulation.
- **Tabulate:** For pretty-printing tables in the console.

---

## Algorithms

### 1. Collaborative Filtering with ALS
- Uses Alternating Least Squares (ALS) to factorize the user-item interaction matrix.
- Predicts missing ratings and recommends items with the highest predicted ratings.

### 2. Content-Based Filtering
- Uses TF-IDF to vectorize item descriptions.
- Computes cosine similarity between items to recommend similar products.
- For advanced semantic understanding, Sentence-BERT embeddings are used to compute item similarities.

### 3. Hybrid Recommendations
- Combines recommendations from collaborative filtering and content-based filtering.
- Ensures diverse and personalized recommendations.
### 4. Real-Time Processing
- Apache Kafka is used to stream user-item interactions and recommendations in real-time.
- Real-time recommendations are streamed to the Kafka topic for further processing or consumption.
### 5. Evaluation and Monitoring
- Metrics: Precision@K, Recall@K, and NDCG (Normalized Discounted Cumulative Gain) are used to evaluate recommendation quality.
- MLflow: Tracks experiments, logs parameters, metrics, and model artifacts for reproducibility.
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
- Python 3.9 or higher.
- Java 8 or higher (required for PySpark).
- Kafka and Zookeeper (for real-time processing).
---

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recommendation-system.git
   cd recommendation-system
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Setting Up Kafka Locally
   - Download Kafka from the [official website](https://kafka.apache.org/downloads).
   - Extract the downloaded .tgz file using a tool like 7-Zip or any other archive manager.
   - For example, extract it to a directory like:
     ```bash
     C:\kafka

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
     
4. Real-Time Processing:
- Sends recommendations to the Kafka recommendations topic for real-time streaming.
- Use a Kafka consumer to listen to the topic and process recommendations in real-time.
  
5. Experiment Tracking:
- Use MLflow to track experiments, log parameters, metrics, and model artifacts
---

## Output
### Example Outputs
1. Collaborative Filtering Recommendations

| item_id | category     | description               | predicted_rating |
|---------|--------------|---------------------------|-----------------:|
| 12      | Electronics  | Description for item 12   | 4.5              |
| 25      | Books        | Description for item 25   | 4.3              |
| 34      | Clothing     | Description for item 34   | 4.2              |
| 45      | Home         | Description for item 45   | 4.1              |
| 18      | Sports       | Description for item 18   | 4.0              |

2. Content-Based Recommendations
#### Content-Based Recommendations for Item 1:
  
| item_id | category     | description               |
|---------|--------------|---------------------------|
| 12      | Electronics  | Description for item 12   |
| 25      | Books        | Description for item 25   |
| 34      | Clothing     | Description for item 34   |
| 45      | Home         | Description for item 45   |
| 18      | Sports       | Description for item 18   |

 3. Hybrid Recommendations
#### Hybrid Recommendations for User 1 and Item 1:

| item_id | category     | description               |
|---------|--------------|---------------------------|
| 12      | Electronics  | Description for item 12   |
| 25      | Books        | Description for item 25   |
| 34      | Clothing     | Description for item 34   |
| 45      | Home         | Description for item 45   |
| 18      | Sports       | Description for item 18   |
| 7       | Electronics  | Description for item 7    |
| 56      | Clothing     | Description for item 56   |
| 23      | Books        | Description for item 23   |
| 89      | Home         | Description for item 89   |
| 14      | Sports       | Description for item 14   |

- Kafka Consumer Output
```json
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
