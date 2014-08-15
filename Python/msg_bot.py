import reddit_analysis 
while True : 
    unread = [c for c in r.get_unread()]
    
    for u in unread: 
        u.mark_as_read()
        user = User_Analysis(u.author.name)
        body = u.body 
        body = body.replace(')',"")
        query = body.split('(') 
    
        if query[0] == "top_words":  
            if len(query) == 1: 
                r.send_message(user.user.username, "Data",str(user.top_words())) 
                print("sent")
            else: 
                size = 10
                extra_words = []
                subreddit_filter = False
                stop_check = True
                
                params = query[1].split(',')
                for i in params: 
                    s = i.split('=')
                    if s[0] == "size":
                        size = int(s[1])
                    elif s[0] == " stop_check": 
                        if s[1] == "False":
                            stop_check = False
                    elif s[0] == " extra_words":
                        s1 = s[1][1:-1]
                        s1 = s1.split(',')
                        extra_words = s1
                    elif s[0] == " subreddit_filter":
                        subreddit_filter = s[1]                    
                    
                msg = str(user.top_words(size=size, 
                                     extra_words=extra_words,
                                     subreddit_filter=subreddit_filter,
                                     stop_check=stop_check))
                r.send_message(user.user.username, "Data",msg) 
                print("sent")
                
        elif query[0] == "avg_karma_p_comment":
            r.send_message(user.user.username, "Data",str(user.avg_karma_p_comment()))
            print("sent")
        elif query[0] == "subreddit_recommendation":
            if len(query) == 1: 
                r.send_message(user.user.username, "Data",str(user.subreddit_recommendation()))      
                print("sent")
            else: 
                r.send_message(user.user.username, "Data",str(user.subreddit_recommendation(query[1].split())))     
                print("sent")
        elif query[0] == "avg_comment_length":
            r.send_message(user.user.username, "Data",str(user.avg_comment_length()))              
            print("sent")
        elif query[0] == "sub_reddit_activity":
            r.send_message(user.user.username, "Data",str(user.subreddit_activity()))
            print("sent")
            
        elif query[0] == "liked_content":
            r.send_message(user.user.username, "Data",str(user.liked_content()))
            print("sent")     
        
        elif query[0] == "disliked_content":
            r.send_message(user.user.username, "Data",str(user.disliked_content()))
            print("sent")  
            
        elif query[0] == "get_stop_count":
            r.send_message(user.user.username, "Data",str(user.get_stop_count()))
            print("sent")   
            
        elif query[0] == "get_earliest_comment":
            r.send_message(user.user.username, "Data",str(user.get_earliest_comment()))
            print("sent")      
            
        elif query[0] == "get_best_comment":
            r.send_message(user.user.username, "Data",str(user.get_best_comment()))
            print("sent")
