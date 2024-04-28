import wikipedia
from openai import OpenAI
from flask import Flask, render_template, request, redirect, url_for
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

# creates an instance of a flask web application
app = Flask(__name__)

# decorates the 'home' function to let the app know when the url has [domain name]/, the app calls 'home'
@app.route("/", methods = ["get"])
# defines the pages that will be on the website
def home():
    if request.method == "get":
        # return redirect("/summary")
        userInput = request.form.get("fconcept")
        AIoutput = userSearchToAIResponse(userInput)
        return render_template("summary.html", content=AIoutput)
    return render_template("index.html")
    # commented out so it doesnt use money by calling chatgpt api each time
    # return userSearchToAIResponse("meringue")

# @app.route("/summary", methods = ["get"])
# def summary():
#     if request.method == "get":
#         return redirect("/")
#     userInput = request.form.get("fconcept")
#     AIoutput = userSearchToAIResponse(userInput)
#     return render_template("summary.html", content=AIoutput)

#runs the app
if __name__ == "__main__":
    app.run(debug=True)

# flask input form
# python env files

    # print(response.choices[0].message.content)


    
# userSearchToAIResponse("gibbs free energy")

