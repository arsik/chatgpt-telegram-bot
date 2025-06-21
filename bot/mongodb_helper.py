import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


class MongoDBHelper:
    """
    Helper class for MongoDB operations related to user management and subscriptions.
    """
    
    def __init__(self, config: dict):
        """
        Initialize MongoDB connection.
        :param config: Configuration dictionary containing MongoDB settings
        """
        self.config = config
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self):
        """
        Establish connection to MongoDB.
        """
        try:
            mongodb_uri = self.config.get('mongodb_uri', 'mongodb://localhost:27017/')
            database_name = self.config.get('mongodb_database', 'chatbot')
            
            self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            
            logging.info(f"Successfully connected to MongoDB database: {database_name}")
            
        except ConnectionFailure as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error connecting to MongoDB: {e}")
            raise
    
    def close_connection(self):
        """
        Close MongoDB connection.
        """
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed")
            