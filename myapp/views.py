from django.shortcuts import render
from django.shortcuts import HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
topics = [
    {'id' : 1, 'title' : 'routing', 'body' : 'Routing is ..'}
    , {'id' : 2, 'title' : 'view', 'body' : 'view is ..'}
    , {'id' : 3, 'title' : 'Model', 'body' : 'Model is ..'}
]

def olTemplate() :
    global topics
    ol = ''
    for topic in topics :
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return ol

def controlTemplate() :
    controls = ''
    controls += '<ul>'
    controls += '<li><a href="/create/">create</a></li>'
    controls += '</ul>'
    return controls

def HTMLTemplate(articleTag) :
    olTag = olTemplate()
    contorlTag = controlTemplate()
    html = f'''
        <html>
            <body>
                <h1><a href="/">Django</a></h1>
                <ol>{olTag}</ol>
                {articleTag}
                <br>
                <hr>
                {contorlTag}
                
            </body>
        </html>
    '''
    return html

def index(request) :
    #return HttpResponse('Welcome myapp view py' + '<hr> <h2>Random</h2>' + str(random.random()))
    article = '''<h2>Welcome</h2>
                Hello, Django'''
    html = HTMLTemplate(article)
    return HttpResponse(html)

#  def 의 두번째 값으로 id 값을 활용할 수 있음
def read(request, id) :
    # return HttpResponse('read' + id)
    global topics
    article = ''
    for topic in topics :
        if topic['id'] == int(id) :
            article = f'''<h2>{topic["title"]}</h2>
                            {topic["body"]}
                        '''
    html = HTMLTemplate(article)
    return HttpResponse(html)
    
@csrf_exempt
def create(request) :
    # return HttpResponse('create')
    article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit" value="create button"></p>
        </form>
    '''
    html  = HTMLTemplate(article)
    return HttpResponse(html)
