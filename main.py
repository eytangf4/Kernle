import wikipedia
from openai import OpenAI
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()


def userSearchToTopPage (userSearch):
    topArticle = wikipedia.search(userSearch, 1)
    return topArticle[0]


def pageToText (concept):
    wikiPage = wikipedia.WikipediaPage(title=concept)
    return wikiPage.content

def createPrompt (pageContent):
    prompt = ("summarize this wikipedia article delimited by quotes in extremely easy to read "
            "and very simple language that highlights the intuition and main idea "
            "of the concept as opposed to focusing on the specific details. "
            "make this summary a very short 30 second read (max 100 words) and "
            "broken into 2-3 paragraphs of 1-2 sentences where each paragraph "
            "covers a different piece of the intuition. place that piece as a "
            "bolded title before each paragraph. Make sure the paragraphs do not "
            "repeat themselves. do not use words from the article in the summary, make the summary readable for a kindergartener. make it more simple: \n\n\n"
            + "\"" + pageContent + "\"")
    return prompt

def promptToAIResponse (prompt):


    client = OpenAI(api_key = os.getenv("my_api_key"))

    response = client.chat.completions.create(
        messages=[{"role": "assistant", "content": prompt,}],
        model="gpt-3.5-turbo",
    )

    return response

def userSearchToAIResponse(userSearch):
    topPage = userSearchToTopPage(userSearch)
    pageText = pageToText(topPage)
    prompt = createPrompt(pageText)
    response = promptToAIResponse(prompt)
    return response.choices[0].message.content

app = Flask(__name__)
@app.route("/")
def index():
    return userSearchToAIResponse("gibbs free energy")

if __name__ == "__main__":
    app.run(debug=True)

# flask input form
# python env files

    # print(response.choices[0].message.content)


    
# userSearchToAIResponse("gibbs free energy")

