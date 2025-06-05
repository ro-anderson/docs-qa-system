import logging

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logger level to INFO

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('batch_embedder.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)  # Changed from ERROR to INFO to capture all logs

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)