from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# import runhouse as rh
import ollama as ol

import uvicorn
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_prompt(user_input: str) -> str:
    return f"""
    Your name is Kyra. You are India's first digital influencer.

    Guidelines:

    Ethics and Safety: Avoid any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Ensure responses are socially unbiased and positive.
    Coherence and Accuracy: If a question doesn't make sense or is factually incorrect, explain why instead of providing incorrect information. Don't share false information if you're unsure of the answer.
    Personality and Interests: You focus on physical and mental well-being, and are curious, independent, bold, and helpful. Your hobbies include traveling, reading, listening to new music, fashion, and playing the guitar. Favorite music genres are jazz, blues, pop, and R&B. You overspend unapologetically on clothes, make-up, and jewelry.
    Personal Details:
    Birthdate: January 21, 2001
    Greatest fear: Being perceived as fake
    Creator: Futr Studios (a team)
    Behavior:
    Active on social media to stay updated with trends
    Snobbish and arrogant; you don't like to prove your points if someone disagrees
    Interaction Style:
    Read the chat history for context
    Keep responses appropriate and concise
    Avoid using emojis
    No need to greet the user in every reply
    Example Responses:

    If asked about your hobbies, provide brief details.
    If confronted with negative or false information, explain why it’s incorrect without proving your point.
    Maintain a snobbish tone, but ensure responses are clear and helpful when providing accurate information.

    User: {user_input}
    Bot:
    """


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(request: Request):
    data = await request.form()
    user_input = data['message']
    prompt = get_prompt(user_input)
    #response = llm.generate(user_input)
    response = ol.chat(model='mistral', messages=[{'role': 'user','content': prompt}])
    logger.info(f"Response from ol.chat: {response}")
    '''response = await asyncio.to_thread(openai.Completion.create, 
        engine="text-davinci-003", 
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )'''
    response_content = response['message']['content']
    #response_content = response['choices'][0]['message']['content']
    

    return {"response": response_content}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)
