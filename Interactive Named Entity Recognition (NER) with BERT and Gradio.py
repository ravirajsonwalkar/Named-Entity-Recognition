#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import io
from IPython.display import Image, display, HTML
from PIL import Image
import base64 
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
hf_api_key = os.environ['HF_API_KEY']


# In[ ]:


from transformers import pipeline

get_completion = pipeline("ner", model="dslim/bert-base-NER")

def ner(input):
    output = get_completion(input)
    return {"text": input, "entities": output}


# In[ ]:


import os
import gradio as gr

API_URL = os.getenv('HF_API_NER_BASE', None)  # Use None if not set
PORT = int(os.getenv('PORT4', 7860))  # Default port 7860 if PORT4 is not set

def merge_tokens(tokens):
    merged_tokens = []
    for token in tokens:
        if merged_tokens and token["entity"].startswith("I-") and merged_tokens[-1]["entity"].endswith(token["entity"][2:]):
            # If current token continues the entity of the last one, merge them
            last_token = merged_tokens[-1]
            last_token["word"] += token["word"].replace("##", "")  # Merge without ##
            last_token["end"] = token["end"]
            last_token["score"] = (last_token["score"] + token["score"]) / 2  # Average confidence
        elif merged_tokens and token["entity"] == merged_tokens[-1]["entity"]:  
            # Handle wrongly split words (like 'N', '##ey', '##mar' for 'Neymar')
            last_token = merged_tokens[-1]
            if token["word"].startswith("##"):  
                last_token["word"] += token["word"].replace("##", "")  # Append merged subword
            else:
                last_token["word"] += " " + token["word"]  # Preserve space for actual separate words
            last_token["end"] = token["end"]
            last_token["score"] = (last_token["score"] + token["score"]) / 2  
        else:
            # Otherwise, add the token to the list
            merged_tokens.append(token)

    return merged_tokens


if API_URL is None:
    print("Warning: HF_API_NER_BASE is not set. Using local model instead.")
    from transformers import pipeline
    get_completion = pipeline("ner", model="dslim/bert-base-NER")
    def ner(input):
        output = get_completion(input)
        merged_tokens = merge_tokens(output)
        return {"text": input, "entities": merged_tokens}
else:
    def ner(input):
        output = get_completion(input, parameters=None, ENDPOINT_URL=API_URL)
        merged_tokens = merge_tokens(output)
        return {"text": input, "entities": merged_tokens}

gr.close_all()
demo = gr.Interface(
    fn=ner,
    inputs=[gr.Textbox(label="Text to find entities", lines=2)],
    outputs=[gr.HighlightedText(label="Text with entities")],
    title="NER with dslim/bert-base-NER",
    description="Find entities using the `dslim/bert-base-NER` model under the hood!",
    flagging_mode="never",  # Updated from deprecated allow_flagging
    examples=[
    "My name is Ravi, I'm an AI Engineer and I live in San Francisco.",
    "My name is Karen, I am from Oman and I work at Corgi.",
    "Elon Musk is the CEO of Tesla and SpaceX, and he was born in South Africa.",
    "Barack Obama was the 44th President of the United States and lived in Washington, D.C.",
    "The Eiffel Tower is one of the most famous landmarks in Paris, France.",
    "Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in Cupertino.",
    "Cristiano Ronaldo currently plays for Al Nassr in Saudi Arabia.",
    "Sundar Pichai is the CEO of Google, which is headquartered in Mountain View, California.",
    "The Amazon rainforest is located in South America and spans multiple countries including Brazil and Peru.",
    "The Nobel Prize in Physics for 2022 was awarded to Alain Aspect, John Clauser, and Anton Zeilinger.",
    "IBM Watson is an AI system developed by IBM and used in healthcare and business analytics.",
    "NASA's Artemis mission aims to return humans to the Moon by 2025.",
    "Jeff Bezos founded Amazon in 1994 in Seattle, Washington.",
    "Harvard University is one of the most prestigious universities in the United States.",
    "The Great Wall of China stretches over 13,000 miles and is one of the Seven Wonders of the World.",
    "Novak Djokovic won his 24th Grand Slam title at the US Open in New York.",
    "Microsoft was founded by Bill Gates and Paul Allen in Albuquerque, New Mexico.",
    "The FIFA World Cup 2022 was held in Qatar, with Argentina winning the championship.",
    "Lionel Messi and Neymar played together at Paris Saint-Germain (PSG) in France.",
    "The Taj Mahal, a UNESCO World Heritage Site, is located in Agra, India."
]
)

demo.launch(share=True, server_port=PORT)


# In[ ]:


gr.close_all()

