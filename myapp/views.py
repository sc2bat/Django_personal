from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
import random
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
topics = [
    {'id' : 1, 'title' : 'routing', 'body' : 'Routing is ..'}
    , {'id' : 2, 'title' : 'view', 'body' : 'view is ..'}
    , {'id' : 3, 'title' : 'Model', 'body' : 'Model is ..'}
]
nextId = len(topics)

def olTemplate() :
    global topics
    ol = ''
    for topic in topics :
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return ol

def controlTemplate(id=None) :
    controls = ''
    controls += '<ul>'
    controls += '<li><a href="/create/">create</a></li>'
    if id is not None : 
        controls += f'<li><a href="/update/{id}">update</a></li>'
        controls += '<li>'
        controls += '<form action="/delete/" method="POST">'
        controls += f'<input type="hidden" name="id" value={id}>'
        controls += '<input type="submit" value="delete">'
        controls += '</form>'
        controls += '<li>'
    controls += '</ul>'
    return controls

def HTMLTemplate(articleTag, id=None) :
    global topics
    olTag = olTemplate()
    contorlTag = controlTemplate(id)
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
    html = HTMLTemplate(article, id)
    return HttpResponse(html)
    
@csrf_exempt
def create(request) :
    global nextId
    # return HttpResponse('create')
    #print('request.method', request.method)
    if request.method == 'GET' :
            
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create button"></p>
            </form>
        '''
        html  = HTMLTemplate(article)
        return HttpResponse(html)
    elif request.method == 'POST' :
        #print(request.POST) # <QueryDict: {'title': ['ERERE'], 'body': ['EERER']}>
        title = request.POST['title']
        body = request.POST['body']
        nextId += 1
        newTopic = {
                'id' : nextId
                ,'title' : title
                , 'body' : body
                ,
            }
        topics.append(newTopic)
        url = '/read/' + str(nextId)
        return redirect(url)

@csrf_exempt
def delete(request) :
    global topics
    print('=====================')
    print(request.method)
    print('=====================')
    if request.method == 'POST' :
        id = request.POST['id']
        newTopics = []
        for topic in topics :
            if topic['id'] != int(id) :
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

@csrf_exempt
def update(request, id) :
    global topics
    if request.method == 'POST' :
        for topic in topics :
            if topic['id'] == int(id) :
                topic['title'] = request.POST['title']
                topic['body'] = request.POST['body']
                break
        return redirect(f'/read/{id}/')
    elif request.method == 'GET' :
        u_id = id
        u_title = ''
        u_body = ''
        for topic in topics :
            if topic['id'] == int(id) :
                u_id = topic['id']
                u_title = topic['title']
                u_body = topic['body']
                break
        article = f'''
            <form action="/update/{u_id}/" method="POST">
                <p><input type="hidden" name="id" value={u_id}></p>
                <p><input type="text" name="title" placeholder="title" value={u_title}></p>
                <p><textarea name="body" placeholder="body">{u_body}</textarea></p>
                <p><input type="submit" value="update button"></p>
            </form>
        '''
        html  = HTMLTemplate(article)
        return HttpResponse(html)
