import wordy_bot as wb

class Total_Submission(wb.User_Information):
    def reply_top_words_used(self):
        def add(word, collection):
            if word.lower() in wb.common:
                pass
            else: 
                if word.lower() in collection:
                    collection[word.lower()] += 1
                else:
                    collection[word.lower()] = 1            
        def _add_to_dictionary(word, collection):
            word = ''.join(ch for ch in word if ch not in wb.punc) # removes any other significant punctuation
            if not word.isalpha():
                pass 
            else:
                add(word, collection)  
                
        new_collection = {}
        for c in self.get_comments():
            body = c.body.strip().split()
            self.word_count += len(body)
            for word in body:
                if word.lower() in wb.common:
                    pass                
                elif any([word.endswith(p) for p in wb.punc]): # checks for ending punctuation.
                    _add_to_dictionary(word[:-1], new_collection)
                else:  
                    _add_to_dictionary(word, new_collection)
                     
        return new_collection
    
if __name__ == "__main__":
    total_collection = {}
    total_word_count = 0
    url = 'http://www.reddit.com/r/learnprogramming/comments/232hzi/just_created_my_first_reddit_bot_post_in_this/'
    comments = wb.Submissions.select() # Get all entries. 
    
    for comment in comments:
        c = wb.r.get_submission(url + comment.subid)
        # Fixed this: was previous just getting the author of the 
        # submission, not the comment. 
        # When you get_submission, it will reload the submission with
        # the single comment.
        cmt = c.comments[0] 
        T = Total_Submission(cmt.author.name, cmt)
        u_words = T.reply_top_words_used()
        total_word_count += T.word_count
        for w, v in u_words.items():
            if w in total_collection:
                total_collection[w] += v
            else: 
                total_collection[w] = v 
        
        print(comment.subid)
    info = wb.collections.Counter(total_collection).most_common(10) 
    #wb.r.send_message('...')
    print info 
