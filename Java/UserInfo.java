package WordyBot;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import main.java.com.github.jreddit.user.Comment;
import main.java.com.github.jreddit.user.User;


public class UserInfo{
	
	private static String username;
    private static Integer wordCount;
     
    public UserInfo(String username) {
        this.username = username;
        this.wordCount = 0;
    }
    public static String main(String[] args) throws Exception {
    	
    	// Get common list. 
    	List<String> common = null; 
 		try {
 			common = common_words();
 		} catch (FileNotFoundException e) {
 			e.printStackTrace();
 		}
 		
    	// Comments limit changed to 1000 at source. 
    	List<Comment> comments = User.comments(username); 
    	// Initialize the total_collection of words as empty "dictionary." 
    	Map<String, Integer> total_collection = new LinkedHashMap<String, Integer>();
    	
    	for (Comment c : comments) {
    		String comment = c.getComment(); 
    		List<String> body = Arrays.asList(comment.split(" "));
    		wordCount = wordCount + body.size();
    		
    		for (String s : body) {
     			s = s.toLowerCase();
     			if (common.contains(s)){
     				continue; 
     			}
     			else { 
     				add_to_dictionary(s, total_collection);	
     			}
     		}
    	}
 		
 		
 		
 		List<Map.Entry<String, Integer>> entries = 
 				new ArrayList<Map.Entry<String, Integer>>(total_collection.entrySet());
 		
 		// Sort total_collections 
 		sort_map(entries);
 		
 		// Top ten list 
 		List<Map.Entry<String, Integer>> top = top_list(entries, 10);
 		String topmsg = "";
 		for (Map.Entry<String, Integer> e : top) {
 			topmsg = topmsg + "**" + e.getKey() + "**" + ": " + e.getValue() + "\n\n";
 		}
 		String msg = "Hello " + username + ". After careful analysis of your " + wordCount + " word comment history I have collected your top 10 most non-common words used." + "\n\n" + "Out of " + total_collection.keySet().size() + " unique words, these are your top ten: \n\n" + topmsg;
    
 		return msg; 
    }
    
    public static String getUser() {
        return username;
    }
    
    public static Integer getwordCount() {
        return wordCount;
    }
    public static ArrayList<String> common_words() throws FileNotFoundException {

		Scanner s = new Scanner(new File("/home/carneo/workspace/jReddit/src/WordyBot/common.txt"));
		ArrayList<String> list = new ArrayList<String>();
		while (s.hasNext()){
		    list.add(s.next());
		}
		s.close();
	    
		return list;
    }
    public static List<Map.Entry<String, Integer>> top_list(List<Map.Entry<String, Integer>> list, Integer num) { 
		// List must be sorted. 
		try {
			return list.subList(0, num);
		} catch (IndexOutOfBoundsException e) {
			return list.subList(0, list.size()); 
		}
		
	}
    public static void sort_map(List<Map.Entry<String, Integer>> entries) {
		
		// Sort entries in descending order. 
		Collections.sort(entries, new Comparator<Map.Entry<String, Integer>>() {
			  public int compare(Map.Entry<String, Integer> a, Map.Entry<String, Integer> b){
				  
			    return b.getValue().compareTo(a.getValue());
			  }
			});
			Map<String, Integer> sortedMap = new LinkedHashMap<String, Integer>();
			// Put all entries from entries in sortedMap 
			for (Map.Entry<String, Integer> entry : entries) {
			  sortedMap.put(entry.getKey(), entry.getValue());
		}
	}
    
    public static void add_to_dictionary(String word, Map<String, Integer> collection) {
    	
    	if (word.matches("[A-Za-z]+")) {
			if (collection.containsKey(word)) {
			   collection.put(word, collection.get(word) + 1); 
			}
			else { 
				collection.put(word, 1);
			}	
    	}
	}
}
