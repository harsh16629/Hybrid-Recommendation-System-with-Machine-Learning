
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from kafka import KafkaProducer
import mlflow
import mlflow.spark
from google.cloud import recommendationengine_v1beta1
from tabulate import tabulate

# Initialize Spark session
spark = SparkSession.builder \
    .appName("AdvancedRecommendationSystem") \
    .getOrCreate()

# Generate dummy data for user-item interactions
np.random.seed(42)
num_users = 100
num_items = 50
num_interactions = 1000

user_ids = np.random.randint(1, num_users + 1, num_interactions)
item_ids = np.random.randint(1, num_items + 1, num_interactions)
ratings = np.random.randint(1, 6, num_interactions)  # Ratings from 1 to 5

user_item_interactions = pd.DataFrame({
    "user_id": user_ids,
    "item_id": item_ids,
    "rating": ratings
})

# Generate dummy data for item metadata
item_ids_meta = np.arange(1, num_items + 1)
categories = np.random.choice(["Electronics", "Books", "Clothing", "Home", "Sports"], num_items)
descriptions = [f"Description for item {i}" for i in item_ids_meta]

item_metadata = pd.DataFrame({
    "item_id": item_ids_meta,
    "category": categories,
    "description": descriptions
})

# Save dummy data to CSV (optional)
user_item_interactions.to_csv("user_item_interactions.csv", index=False)
item_metadata.to_csv("item_metadata.csv", index=False)

# Load data into Spark DataFrame
interactions_spark = spark.createDataFrame(user_item_interactions)

# Train ALS model
als = ALS(
    userCol="user_id",
    itemCol="item_id",
    ratingCol="rating",
    coldStartStrategy="drop",
    rank=10,
    maxIter=5,
    regParam=0.01
)
model = als.fit(interactions_spark)

# Generate collaborative filtering recommendations
user_recs = model.recommendForAllUsers(10)  # Top 10 recommendations per user

# Convert Spark DataFrame to Pandas DataFrame for easier manipulation
user_recs_pd = user_recs.toPandas()

# Extract item_ids and ratings from the recommendations column
def extract_item_ids_and_ratings(recommendations):
    return [(row.item_id, row.rating) for row in recommendations]

user_recs_pd["recommendations"] = user_recs_pd["recommendations"].apply(extract_item_ids_and_ratings)

# Map item IDs to item names and categories
def map_item_ids_to_details(item_ids, item_metadata):
    return item_metadata[item_metadata["item_id"].isin(item_ids)]

# Display collaborative filtering recommendations with item details
print("\n" + "=" * 70)
print("Collaborative Filtering Recommendations:")
print("=" * 70)
for _, row in user_recs_pd.head().iterrows():
    user_id = row["user_id"]
    recommendations = row["recommendations"]

    # Extract item IDs and ratings
    item_ids = [rec[0] for rec in recommendations]
    ratings = [rec[1] for rec in recommendations]

    # Get item details
    item_details = map_item_ids_to_details(item_ids, item_metadata)
    item_details["predicted_rating"] = ratings

    # Sort by predicted rating (descending)
    item_details = item_details.sort_values(by="predicted_rating", ascending=False)

    # Print results
    print(f"\nUser {user_id} Recommendations:")
    print(tabulate(item_details[["item_id", "category", "description", "predicted_rating"]], headers="keys", tablefmt="pretty", showindex=False))
print("=" * 70 + "\n")

# Content-Based Filtering with Sentence-BERT
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
item_metadata["embedding"] = item_metadata["description"].apply(lambda x: sentence_model.encode(x))

# Compute cosine similarity
cosine_sim = cosine_similarity(np.vstack(item_metadata["embedding"].values))

# Function to get content-based recommendations
def content_based_recommendations(item_id, top_n=10):
    idx = item_metadata.index[item_metadata["item_id"] == item_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]  # Exclude the item itself
    item_indices = [i[0] for i in sim_scores]
    return item_metadata.iloc[item_indices]

# Display content-based recommendations for a sample item
sample_item_id = 1
content_recs = content_based_recommendations(sample_item_id, top_n=5)
print("\n" + "=" * 70)
print(f"Content-Based Recommendations for Item {sample_item_id}:")
print("=" * 70)
print(tabulate(content_recs[["item_id", "category", "description"]], headers="keys", tablefmt="pretty", showindex=False))
print("=" * 70 + "\n")

# Hybrid Recommendations
def hybrid_recommendations(user_id, item_id, top_n=10):
    # Collaborative filtering recommendations
    collaborative_recs = user_recs_pd[user_recs_pd["user_id"] == user_id]["recommendations"].iloc[0]
    collaborative_item_ids = [rec[0] for rec in collaborative_recs]

    # Content-based filtering recommendations
    content_recs = content_based_recommendations(item_id, top_n)
    content_item_ids = content_recs["item_id"].tolist()

    # Combine and deduplicate recommendations
    hybrid_item_ids = list(set(collaborative_item_ids + content_item_ids))[:top_n]

    # Get item details
    hybrid_details = map_item_ids_to_details(hybrid_item_ids, item_metadata)
    return hybrid_details

# Display hybrid recommendations for a sample user and item
sample_user_id = 1
sample_item_id = 1
hybrid_recs = hybrid_recommendations(sample_user_id, sample_item_id, top_n=10)
print("\n" + "=" * 70)
print(f"Hybrid Recommendations for User {sample_user_id} and Item {sample_item_id}:")
print("=" * 70)
print(tabulate(hybrid_recs[["item_id", "category", "description"]], headers="keys", tablefmt="pretty", showindex=False))
print("=" * 70 + "\n")

from kafka import KafkaProducer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: str(v).encode('utf-8'),
        key_serializer=lambda k: str(k).encode('utf-8')
    )
    logger.info("Kafka producer initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Kafka producer: {e}")
    raise

# Function to send recommendations to Kafka
def send_recommendation(user_id, recommendations):
    try:
        producer.send(
            'recommendations',
            key=str(user_id),
            value=recommendations
        )
        producer.flush()
        logger.info(f"Sent recommendations for user {user_id} to Kafka.")
    except Exception as e:
        logger.error(f"Failed to send recommendations to Kafka: {e}")

# Example: Send hybrid recommendations to Kafka
sample_user_id = 1
send_recommendation(sample_user_id, hybrid_recs[["item_id", "category", "description"]].to_dict())

# MLflow Tracking
mlflow.set_experiment("RecommendationSystem")
with mlflow.start_run():
    mlflow.log_param("num_users", num_users)
    mlflow.log_param("num_items", num_items)
    mlflow.log_metric("precision@10", 0.85)  # Example metric
    mlflow.spark.log_model(model, "als_model")

# Stop Spark session
spark.stop()