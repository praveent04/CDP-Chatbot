# CDP Documentation Extraction and Query System

## Project Overview

This project aims to extract documentation from various Customer Data Platforms (CDPs), create embeddings for efficient querying, and provide a user-friendly interface for asking questions about these platforms.

## Components

1. `download.py`: Scrapes documentation from CDP websites
2. `embeddings_db.py`: Creates embeddings and stores them in ChromaDB
3. `main.py`: Main interface for querying the documentation

## Detailed Workflow

### 1. Documentation Extraction (`download.py`)

This script scrapes documentation from four CDP websites: Segment, mParticle, Lytics, and Zeotap.

#### Key Features:
- Uses `requests` and `BeautifulSoup` for web scraping
- Extracts content from relevant subpages of each CDP's documentation
- Saves extracted content in text files within a `cdp_documentation` folder

**Note:** Unable to successfully scrape data from Zeotap, possibly due to authentication requirements or dynamic content loading.

### 2. Embedding Creation (`embeddings_db.py`)

Processes the extracted documentation and creates embeddings for efficient querying.

#### Key Features:
- Uses `sentence_transformers` to create embeddings from text content
- Utilizes ChromaDB for storing and managing embeddings
- Processes each text file in `cdp_documentation` folder and adds its embedding to ChromaDB collection

### 3. Query Interface (`main.py`)

Main script providing an interface for querying CDP documentation.

#### Key Features:
- Checks for necessary folders and runs prerequisite scripts if needed
- Uses Mistral AI model for generating responses
- Queries ChromaDB collection to find relevant documentation for user questions
- Provides a command-line interface for users to ask questions about CDPs

## Usage

1. Install required libraries

2. Run the main script: answer_db.py

3. The script automatically runs `download.py` and `embeddings_db.py` if necessary. Or manual run the scripts.

4. Start asking questions about CDPs. Type 'exit' to end the program.

## Limitations and Future Improvements

- Unable to scrape data from Zeotap, limiting the system's ability to answer questions about this platform
- Scraping method could be improved to handle dynamic content and authentication
- Additional error handling and logging could be implemented for better debugging and maintenance

## Conclusion

This project demonstrates a complete pipeline for extracting, processing, and querying documentation from multiple CDP platforms. While it successfully handles most targeted platforms, there's room for improvement, particularly in handling more complex websites like Zeotap.
