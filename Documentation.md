# RSS Feed Processing Project

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Implementation Logic and Design Choices](#3-implementation-logic-and-design-choices)
4. [Setup Instructions](#4-setup-instructions)
5. [Usage Guide](#5-usage-guide)
6. [Extensibility and Future Improvements](#6-extensibility-and-future-improvements)

## 1. Project Overview

This project implements an RSS feed processing system that collects news articles from various RSS feeds, categorizes them using natural language processing (NLP), and stores them in a database. The system uses Celery for task queue management, allowing for asynchronous and distributed processing of RSS feeds.

### Key Features:
- Fetches articles from multiple RSS feeds
- Categorizes articles using NLP
- Stores processed articles in a MySQL database
- Uses Celery for asynchronous task processing

## 2. System Architecture

The system follows a distributed architecture with the following main components:

1. **Main Script (main.py)**: Initiates the RSS feed processing tasks
2. **Celery Worker (celery_worker.py)**: Handles asynchronous tasks for feed processing and article classification
3. **RSS Parser (rss_parser.py)**: Fetches and parses RSS feeds
4. **NLP Classifier (nlp_classifier.py)**: Categorizes articles based on their content
5. **Database (database_setup.py)**: Defines the schema and handles storage of processed articles

## 3. Implementation Logic and Design Choices

### 3.1 Main Script (main.py)

**Implementation Logic:**
- Serves as the entry point for the application
- Initializes the database
- Queues RSS feed processing tasks

**Design Choices:**
- Separation of concerns: The main script only handles initialization and task queueing, delegating actual processing to worker tasks.
- Use of Celery's `delay()` method for asynchronous task execution, allowing for non-blocking operation.

### 3.2 Celery Task Queue (celery_worker.py)

**Implementation Logic:**
- Defines two main tasks: `process_feed` and `classify_and_store_article`
- `process_feed` fetches articles from a given RSS feed and queues individual article processing tasks
- `classify_and_store_article` classifies an article and stores it in the database

**Design Choices:**
- Task granularity: Separate tasks for feed processing and article processing allow for fine-grained parallelism and failure isolation.
- Use of Celery for distributed task processing, enabling scalability and fault tolerance.
- Asynchronous processing allows for efficient handling of slow network operations (RSS fetching) and CPU-intensive tasks (NLP classification).

### 3.3 RSS Parser (rss_parser.py)

**Implementation Logic:**
- Uses `feedparser` library to fetch and parse RSS feeds
- Extracts relevant information (title, content, publication date, URL) from feed entries

**Design Choices:**
- Use of `feedparser` for its robust handling of various RSS formats and edge cases.
- Extraction of a standardized set of fields from feed entries, ensuring consistency across different RSS sources.

### 3.4 NLP Classifier (nlp_classifier.py)

**Implementation Logic:**
- Uses spaCy for natural language processing
- Implements a simple keyword-based classification system

**Design Choices:**
- Use of spaCy for its efficiency and comprehensive NLP capabilities, even though the current implementation only uses basic features.
- Simple keyword matching for classification, chosen for its simplicity and speed. This design allows for easy extension to more sophisticated classification methods in the future.
- Predefined categories (Terrorism/protest, Natural Disasters, Positive/Uplifting, Others) chosen to demonstrate multi-class classification.

### 3.5 Database Storage (database_setup.py)

**Implementation Logic:**
- Uses SQLAlchemy ORM for database operations
- Defines a `NewsArticle` model representing the schema for stored articles

**Design Choices:**
- Use of SQLAlchemy ORM for its powerful abstraction capabilities and database-agnostic design.
- Choice of MySQL as the backend database for its robustness and widespread use in production environments.
- Schema design includes fields for all relevant article information and the classified category.
- Use of unique constraints on title and URL to prevent duplicate entries.

## 4. Setup Instructions

1. Ensure you have Python 3.7-3.9 installed.

2. Clone the project repository:
   ```
   git clone <repository-url>
   cd rss-feed-processor
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Download the spaCy English model:
   ```
   python -m spacy download en_core_web_sm
   ```

6. Set up MySQL:
   - Install MySQL if not already installed
   - Create a database named `rss_news`
   - Update the database connection string in `database_setup.py` with your MySQL credentials

7. Install and start Redis (required for Celery):
   - On Ubuntu: `sudo apt-get install redis-server`
   - On macOS with Homebrew: `brew install redis`
   - On Windows, download and install Redis from the official website

## 5. Usage Guide

1. Start the Redis server if it's not already running:
   - On most Unix-based systems: `redis-server`
   - On Windows, start the Redis service

2. Start the Celery worker:
   ```
   celery -A celery_worker worker --loglevel=info
   ```

3. In a new terminal window, activate the virtual environment and run the main script:
   ```
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   python main.py
   ```

4. The system will start processing the RSS feeds defined in `main.py`.

5. Monitor the Celery worker output to track the progress of feed processing and article classification.

6. To view the stored articles, you can use a MySQL client to query the `news_articles` table in the `rss_news` database.

## 6. Extensibility and Future Improvements

The current design allows for several avenues of extension:

- **Enhanced Classification**: Replace the simple keyword-based classifier with a more sophisticated machine learning model.
- **Additional Data Sources**: Integrate new types of data sources by implementing new parser modules and Celery tasks.
- **Data Enrichment**: Add tasks for entity recognition, sentiment analysis, or fetching full article content.
- **Web Interface**: Develop a web application for viewing processed articles and system stats.
- **Scheduled Processing**: Implement periodic tasks in Celery for automatic, scheduled RSS feed processing.
- **Improved Error Handling**: Implement comprehensive error handling and logging for better system resilience and debugging.
- **Testing**: Add unit tests and integration tests for improved reliability and easier maintenance.

To implement any of these improvements, you would typically:
1. Create a new module or modify existing ones to include the new functionality.
2. Update the Celery tasks in `celery_worker.py` to incorporate the new processing steps.
3. Modify the database schema in `database_setup.py` if new data fields are required.
4. Update the main script (`main.py`) if changes to the initialization or task queueing process are needed.

Remember to maintain the modular structure of the project, keeping concerns separated and ensuring that new components integrate well with the existing asynchronous processing architecture.