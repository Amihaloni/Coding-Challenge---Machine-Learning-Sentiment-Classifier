import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import re
import os
import demoji

model_path= './model_params'
len_model = 450

app = FastAPI(
    title="Sentiment Model API",
    description="A simple API that use NLP model to predict the sentiment of the text",
    version="0.1",
)

tokenizer = None
model = None
device = None
# What should happen when we start
@app.on_event("startup")
async def startup_event():
    global tokenizer, model, device
    print(f"Attempting to load model and tokenizer from: {model_path}")
    if not os.path.exists(model_path):
        print(f"FATAL ERROR: Model directory not found at {model_path}. API cannot start effectively.")
        return
    try:
        tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
        model = DistilBertForSequenceClassification.from_pretrained(model_path)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()
        print("Model and tokenizer loaded successfully.")
    except:
        print("FATAL ERROR: Failed to load model and tokenizer. API cannot start effectively.")
        tokenizer=None
        model=None

# The same text processing functions as before in training
def clean_text(text):
    text = demoji.replace_with_desc(text,sep=' ')
    text = text.lower()
    # removes punctuation.
    text = re.sub(r'[^a-z0-9\s_$.]', '', text)
    # to remove /n from the system
    text = text.replace("\n"," ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Taken from internet for return responses
class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    comment: str
    processed_comment: str
    predicted_sentiment: str

# Lets build endpoints for the system where the application gets directed to 
@app.get("/", summary="Root endpoint", description="Returns a welcome message")
async def read_root():
    return {"message": "Welcome to the Crypto Sentiment Classifier"}

@app.post("/predict", response_model=SentimentResponse, summary="Predicts sentiment of a commentl")
async def predict_sentiment(request: CommentRequest):
    """
    Predicts the sentiment of a given Reddit comment.
    """
    global tokenizer, model, device

    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model or Tokenizer not loaded. API is not working.")

    if not request.comment or request.comment.strip() == "":
        raise HTTPException(status_code=400, detail="Comment cannot be blank.")

    try:
        # Preprocess the input comment
        processed_comment_text = clean_text(request.comment)

        inputs = tokenizer(
            processed_comment_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=len_model
        )

        inputs = {k: v.to(device) for k, v in inputs.items()} # device change

        #prediction
        with torch.no_grad():
            logits = model(**inputs).logits
        
        predicted_class_id = torch.argmax(logits, dim=1).item()

        sentiment_label = "Positive" if predicted_class_id == 1 else "Negative"
        return SentimentResponse(
            comment=request.comment,
            processed_comment=processed_comment_text,
            predicted_sentiment=sentiment_label
        )
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
