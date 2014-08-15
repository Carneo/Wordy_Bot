import time, os, collections
import praw
from peewee import * 
 
import pyimgur
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
#REDDIT
r = praw.Reddit('WordyBot, written by /u/vicstudent')
r.login(username='...', password='...')

#MYSQL
db = MySQLDatabase('...', host='localhost', user='...', passwd='...')

punc = ". , ! ? ' ; :".split()
 
common = ['id', 'a', 'i', 'your', 'around', 'want', 'know', 'much', 'like', 'really', 'get', 'people', 'would', 'use', 'one', 'all', 'just', 'being', 'over', 'both', 'through', 'yourselves', "it's", 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 'may', 'must', 'might', 'could', 'shall', 'eye', 'person', 'year', 'way', 'thing', 'man', 'world', 'week', 'work', 'place', 'woman', 'company', 'number', 'group', 'problem', 'fact', 'accordingly', 'allows', 'also', 'amongst', 'anybody', 'think', 'become', 'cant', 'cannot', 'considering', 'consider', "couldn't", 'despite', "didn't", 'appropriate', 'certainly', 'come', 'changes', 'comes', 'contains', 'described', 'definitely', 'alone', 'believe', 'first', 'four', 'gets', 'fifth', 'given', 'gives', 'go', 'getting', 'good', 'feel', 'say', 'make', 'time', 'lot', 'thats', 'theres', 'dont', 'ive', 'im', 'its']
    
class User_Information(object):
    def __init__(self, user_name, comment=None):
        self.user = r.get_redditor(user_name)
        self.comment = comment
        self.comments = self.user.get_comments(self, limit=None) # Max reddit comment limit is 1000.
        self.img = 'myfig.png'
        self.word_count = 0
    
    def get_user(self):
        return self.user
 
    def get_comment(self):
        return self.comment
 
    def get_comments(self):
        return self.comments
 
    def get_img(self):
        return self.img 
    
    def get_word_count(self):
        return self.word_count
        
    def uploadImage(self):
        img = self.get_img()
        im = pyimgur.Imgur('...')
        ui = im.upload_image(img)
        os.remove(img)
       
        return ui.link    
   
    def reply_top_words_used(self):
        def graph_data(data):
            words = []
            occurence = []
            
            for i in data:
                words.append(i[0])
                occurence.append(i[1])
            
            
            y_pos = np.arange(len(words))
            performance = np.arange(10)
            
            plt.barh(y_pos, occurence, align='center', alpha=0.4)
            plt.yticks(y_pos, words)
            plt.xlabel('Performance')
            plt.title('Your top ten used words!')
             
            plt.savefig('myfig')
            plt.clf()     
            plt.close() 
            
        def add(word, collection):
            wordl = word.lower()
            if wordl in common:
                pass
            else: 
                if wordl in collection:
                    collection[wordl] += 1
                else:
                    collection[wordl] = 1   
                    
        def _add_to_dictionary(word, collection):
            word = ''.join(ch for ch in word if ch not in punc) # removes any other significant punctuation
            if not word.isalpha():
                pass 
            else:
                add(word, collection)
                
        new_collection = {}
        for c in self.get_comments():
            body = c.body.strip().split()
            self.word_count += len(body)
            for word in body:
                if word.lower() in common:
                    pass                
                elif any([word.endswith(p) for p in punc]): # checks for ending punctuation.
                    _add_to_dictionary(word[:-1], new_collection)
                else:  
                    _add_to_dictionary(word, new_collection)
                     
                       
        # Put top amount of words in a
        top_list = collections.Counter(new_collection).most_common(10)
       
        graph_data(top_list)
       
        imgur = self.uploadImage()
        msg = "Hello, **%s**. After careful analysis of your **%s** word comment history I have collected your top 10 most non-common words used.\n\nOut of **%s** unique words, here is a **[graph](%s)** of your top used words." % (self.get_user(),self.get_word_count(),
                                                                                                                                                                                                                          len(new_collection),imgur)
        comment = self.get_comment()                                                                                                                                                                                          
        #comment.reply(msg)
        print(msg)

##### DATABASE ##### 
class Submissions(Model):
    ''' Database of checked submissions. Thanks to /u/Phteven_j for the help. 
    The purpose of this is to reduce all the extra work if your bot dies.
    You will have access to a database of all the ids you have visited to refer to.
    
    If you're running Linux, follow these instructions:
          sudo apt-get install python-mysqldb
          sudo apt-get install mysql-server
          
          Create a database: 
          
          mysql -u root -p
          mysql> create database redditbot
    
    ''' 
    subid = TextField()
    
    class Meta:
        database = db 
        
db.connect() 
Submissions.create_table(True)

def is_added(comment_id):   
    try:
        submissions = Submissions.get(Submissions.subid == comment_id)
        return True 
    except:
        return False

def add_entry(comment_id): 
    if not is_added(comment_id):
        print "Adding %s" % comment_id
        Submissions(subid=comment_id).save()

def flush_db():    
    subs = Submissions.select()
    for sub in subs:
        sub.delete_instance()
        
def add_done(comment_id):
    already_done.append(comment_id)
    add_entry(comment_id)
    
def is_done(comment_id):
    return comment_id in already_done or is_added(comment_id)
        
if __name__ == "__main__":
    # There are two approaches you can take to the bot.
    
    # Quick and easy: check your unread mail. 
    # This method has proven to be far superior to the below. 
    # It's much more efficient as it addresses comments quicker, 
    # if the bot dies its no issue, just rerun. 
    # It also avoids having to even use an "already_done" type of 
    # checker. 
    subid = '232hzi'
    while True:
        comments = [c for c in r.get_unread()]
        #already_done = []
        for comment in comments:
            #if not is_done(comment.id): Your choice if you want to store data or not. 
                try:
                    if comment.is_root and comment.submission.id == subid:
                        U = User_Information(comment.author.name, comment)
                        U.reply_top_words_used()
                        #add_done(comment.id)
                        comment.mark_as_read()
                    else: 
                        print 'Not bot-worthy'
                except AttributeError: 
                   print 'Check your PMs'
                   comment.mark_as_read()
                else:
                    continue
        time.sleep(100)

    # Traditional way: analyze the threa.d 
    already_done = []
    while True:
        submission =  r.get_submission('http://www.reddit.com/r/learnprogramming/comments/232hzi/just_created_my_first_reddit_bot_post_in_this/')
        submission.replace_more_comments(limit=None, threshold=0)
        comments = submission.comments
 
        for comment in comments:
            try: 
                if not is_done(comment.id): 
                #if len(comment.replies) > 0:
                    add_done(comment.id)
                else: 
                #elif len(comment.replies) == 0: 
                    U = User_Information(comment.author.name, comment)
                    U.reply_top_words_used()
                   
                    add_done(comment.id) 
            except: 
                continue 
        time.sleep(30)
