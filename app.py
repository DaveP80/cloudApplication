from flask import Flask, render_template, request
from requests_html import HTMLSession
import asyncio
import re

application = Flask(__name__)

@application.route('/',methods=['GET', 'POST'])
def home():
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    if request.method == 'POST':

        checklist = ['java', 'Javascript', 'python', 'Python', 'Java', 'javascript']
                
        language=request.form['language']
        search_query = request.form['search_query']
        if language in checklist:
            pass
        else:
            return render_template('index.html',result={"invalid language selection"})

        regex = rf"(?i){language}(.*)"
        if re.match(regex, search_query):
            return render_template('index.html',result={"invalid search query"})
                    
        query_input = language + " " + search_query
        
        session1 = HTMLSession()
        url = f"https://www.youtube.com/results?search_query={query_input}&sp=CAMSBggDEAEYAg%253D%253D"
        response = session1.get(url)
        list_results = []
        list_results2 = []
        list_results3 = []
        urltemplate = "https://www.youtube.com/watch?v="
        regexquery = re.compile("(watchEndpoint\":{\"videoId\":\")\w\w\w\w\w\w\w\w\w\w\w")
        for var in re.finditer(regexquery, response.text):
            list_results.append(var.group())
        for var2 in list_results:
            list_results2.append(var2[-11:])
        if len(list_results2)<1:
            return render_template('index.html',result="no matching videos")    
        for i in range(len(list_results2)):
            if list_results2[i] not in list_results2[i + 1:]:
                list_results3.append(urltemplate+list_results2[i])
        if len(list_results3)<10:
            return render_template('index.html',result=list_results3)

        jsonresponse = list_results3[0:10]
        emptystr = ""

        for i in jsonresponse:
            emptystr += (i + '\n')
            
        return render_template('index.html',result=emptystr) 

    return render_template('index.html',result="most recent on youtube")

if __name__ == '__main__':
    application.run('0.0.0.0',5000)