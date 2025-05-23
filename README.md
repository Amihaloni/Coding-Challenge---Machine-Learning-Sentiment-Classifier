# Coding-Challenge---Machine-Learning-Sentiment-Classifier
This is a sentiment classification on reddit comments to identify positive or negative sentiments

## What is in the Repository
The data processing techniques are stored in the file `.\Coding-Challenge---Machine-Learning-Sentiment-Classifier\DataProcessing.ipynb`

The Modelling techniques included tfidf with base models and using transformers, all can be found in the 
`.\Coding-Challenge---Machine-Learning-Sentiment-Classifier\Models.ipynb`

The output of the data processing notebook are two cleaned files for two different types of modelling approach both the files have been downloaded and put in the repository named : crypto_data_base.csv and crypto_data_transformer.csv, as the name suggests the files have been used accordingly for the model development.

Further the model parameters the weights and tokenizer are all saved in the `model_params/` folder please be aware to download these to use the api as the model is loaded using this.

There is a requiremnts.txt if you wish to replicate the model development locally, for using just the api use `requirements_api.txt`

Recommendation is to use Google Colab for easier Replication

## How to run the api script
I used Fastapi thinking about the scalability and future uses in order ot run the script follow the steps:

1. Download the github repo locally, wither using clone or using zip download followed by extracting the file (make sure the names of folders are not changes as api directly depends on it)

2. Open command prompt or powershell and change the directory to where the repo is 

    The directory should look like `Machine-Learning-Sentiment-Classifier>` 

3. With CommandPrompt open and directory changed run the following:
    Conda:  
    `conda create -n your_env_name`
            
    `conda activate your_env_name`
            
    `pip install -r requirements_api.txt`
    
    `uvicorn api_server:app --reload`

    venv:   
    `python -m venv myenv`
    
    `myenv\Scripts\activate`      on windows
    or
    `source myenv/bin/activate`   On Linux/macOS
            
    `pip install -r requirements_api.txt`
            
    `uvicorn api_server:app --reload`

4. Your terminal will show :
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [15196] using WatchFiles
    INFO:     Started server process [16608]
    INFO:     Waiting for application startup.

5. cntrl + click on the link and you will see a welcome message once the startup process is done.

6. In order to check the api predict functionality make sure the application return the print tokenizer and model loaded successfully

    Go to the link and add `/docs` it will reditect you to `localhost:8000/docs#/default/predict_sentiment_predict_post`.

    Go to POST section and click on try

    Change the Request body "string" with your own comment and hit execute you will see a prediction shortly.

## How to use the API 
Make sure the number 4 step in the above how to run the api is done already.

1. Using CURL
   
    ```
    curl -X 'POST' \
    'http://127.0.0.1:8000/predict' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "comment": "I just invested in Bitcoin, hope it goes up!"}'
        ```
