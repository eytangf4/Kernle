import wikipedia
from openai import OpenAI
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
# from transformers import AutoTokenizer, AutoModelForCausalLM
load_dotenv()

def userSearchToTopPage (userSearch):
    topArticle = wikipedia.search(userSearch, 1)
    return topArticle[0]

def pageToText (concept):
    wikiPage = wikipedia.WikipediaPage(title=concept)
    # using wikipedia.WikipediaPage as opposed to wikipedia.page since WikipediaPage
    # also contains data from a Wikipedia page but also uses property methods to filter data from the raw HTML.
    # this helps chatGPT to understand the page better
    # (I know this because I tried using both 'page' and 'WikipediaPage' and 'WikipediaPage' gave me clearer kernel summaries
    return wikiPage.content

def createPrompt (pageContent):
    prompt = ("summarize this wikipedia article delimited by quotes in extremely easy to read "
            "and very simple language that highlights the intuition and main idea "
            "of the concept as opposed to focusing on the specific details. "
            "make this summary a very short 30 second read (max 100 words) and "
            "broken into 2-3 paragraphs of 1-2 sentences where each paragraph "
            "covers a different piece of the intuition. place that piece as a "
            "bolded title before each paragraph. Make sure the paragraphs do not "
            "repeat themselves. do not use complicated words from the article in your summary. "
            "write your summary in language a kindergartener would understand. make it more simple: \n\n\n"
            + "\"" + pageContent + "\"")
    return prompt

def promptToAIResponse (prompt):
    # openai
    # setup api key
    client = OpenAI(api_key = os.getenv("openai_api_key"))

    # call the ai api

    # openai
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "assistant", "content": prompt,}],
    )

    # openai
    messageContent = response.choices[0].message.content.strip()

    # huggingface cohere
    # setup api key
    # model_id = "CohereForAI/c4ai-command-r-plus-4bit"
    # tokenizer = AutoTokenizer.from_pretrained(model_id)
    # model = AutoModelForCausalLM.from_pretrained(model_id)

    # messages = [{"role": "user", "content": prompt}]
    # input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    
    # gen_tokens = model.generate(
    #     input_ids, 
    #     max_new_tokens=100, 
    #     do_sample=True, 
    #     temperature=0.3,
    # )

    # messageContent = tokenizer.decode(gen_tokens[0])


    return messageContent

def userSearchToAIResponse(userSearch):
    topPage = userSearchToTopPage(userSearch)
    pageText = pageToText(topPage)
    prompt = createPrompt(pageText)
    response = promptToAIResponse(prompt)
    return response

TEMPLATE_DIR = os.path.abspath('/Users/eytangf/Kernle/templates')
STATIC_DIR = os.path.abspath('/Users/eytangf/Kernle/static/styles')

# creates an instance of a flask web application
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# decorates the 'home' function to let the app know when the url has [domain name]/, the app calls 'home'
# methods tells flask which methods this function is allowed to use, every method in the html file a func is 
# trying to render must be allowed here

@app.route("/", methods = ["get","post"])
# each 'def' defines a page that will be on the website
def home():
    return render_template("index.html")


@app.route("/summary", methods = ["get","post"])
def summary():
    userInput = request.form.get("fconcept")
    try:
        AIoutput = userSearchToAIResponse(userInput)
        return render_template("summary.html", content=AIoutput)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        return render_template("ambiguous.html", options=options, concept=userInput)

@app.route("/about", methods = ["get","post"])
def about():
    return render_template("about.html")

@app.route("/how-to-use", methods = ["get","post"])
def howToUse():
    return render_template("how-to-use.html")

@app.route("/contact", methods = ["get","post"])
def contact():
    return render_template("contact.html")

#runs the app
if __name__ == "__main__":
    app.run()