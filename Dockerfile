FROM python:3.8

# Create a folder /app if it doesn't exist,
# the /app folder is the current working directory
WORKDIR /app

# Copy necessary files to our app
COPY ./app /app

COPY ./requirements.txt /app

COPY ./models /app/models

# Set MODEL_DIR env variable
ENV MIN_MAX_PATH /app/models/minmaxscaler_cycle1.joblib
ENV ONE_HOT_PATH /app/models/onehotencoder_cycle1.joblib
ENV MODEL_PATH /app/models/model_cycle1.joblib

# Port will be exposed, for documentation only
EXPOSE 30000

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
