from flask import Flask, render_template
import os

def countDir(path):
    files = folders = 0
    for _, dirnames, filenames in os.walk(path):
      # ^ this idiom means "we won't be using this value"
        files += len(filenames)
        folders += len(dirnames)
    return folders,files


app = Flask(__name__,static_folder = "./statics")



@app.route('/')
def hello():
    return "<h1 dir = 'rtl'>דף מילוי מטופל</h1>"

@app.route('/blog')
def blog():
    return render_template('survey.html',criteria = getCriteria())
    # srcs = [{'source':'statics/prosak/ep1/a.png'}
    #        ,{'source':'statics/prosak/ep1/b.png'}]
    # episodes = [{'episodeNum':1,'srcs':srcs}]
    # return render_template('blog.html', episodes = episodes)


def getCriteria():
    f = open("statics/criteria", "r")
    data = [line for line in f]
    criteriaNames = [line.split() for line in data]
    criteria = []
    for i in range(len(criteriaNames)):
        if len(criteriaNames[i])==2:
            criteria.append({'name':criteriaNames[i][0],'type':criteriaNames[i][1]})
        else:
            if criteriaNames[i][1]=="options":
                options = {str(j):criteriaNames[i][j+2] for j in range(1,int(criteriaNames[i][2]))}
            criterion={'name': criteriaNames[i][0], 'type': criteriaNames[i][1],'optionsNumber':int(criteriaNames[i][2])}
            criteria.append({**options, **criterion})
    return criteria


def blogHelper():
    num_of_episodes = countDir('statics/prosak')[0]
    episodes = []
    for i in range(1,num_of_episodes+1):
        j = num_of_episodes+1-i
        episodes.append({'episodeNum':(j),'srcs':srcsHelper(j)})
    return episodes


def srcsHelper(num):
    numToWords = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f'}
    srcs = []
    num_of_srcs = countDir('statics/prosak/ep'+str(num))[1]
    for i in range(1,num_of_srcs+1):
        srcs.append({'source':'statics/prosak/ep'+str(num)+'/'+numToWords[i]+'.png'})
    print(srcs)
    return srcs
# def blogHelper():


@app.route('/blog/<string:blog_id>')
def blogspot(blog_id):
    return 'This is blog post number '+blog_id

if __name__ == '__main__':
    app.run()