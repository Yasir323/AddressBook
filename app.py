import logging
from logging.handlers import TimedRotatingFileHandler

import uvicorn
from fastapi import FastAPI
from address_book.routes import address_book_route

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a daily rotating file handler
handler = TimedRotatingFileHandler('app.log', when='midnight', interval=1, backupCount=7, encoding='utf-8')
handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

app = FastAPI()
app.include_router(address_book_route, prefix="/api/v1/addressBook")

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level=logging.INFO)
