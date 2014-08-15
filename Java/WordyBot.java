package WordyBot;

import java.util.List;	
import java.util.Scanner;

import main.java.com.github.jreddit.captcha.Captcha;
import main.java.com.github.jreddit.captcha.CaptchaDownloader;
import main.java.com.github.jreddit.message.Message;
import main.java.com.github.jreddit.message.Messages;
import main.java.com.github.jreddit.message.MessageType;
import main.java.com.github.jreddit.user.User;
import main.java.com.github.jreddit.utils.restclient.HttpRestClient;
import main.java.com.github.jreddit.utils.restclient.RestClient;

public class WordyBot {
	

	public static void main( String[] args ) throws Exception {
		// Set up
		MessageType type = MessageType.UNREAD;
        RestClient restClient = new HttpRestClient();
        restClient.setUserAgent("WordyBot written by /u/vicstudent.");
    	User u = new User(restClient, "...", "...");
    	u.connect();
    	
    	Messages m = new Messages(restClient);
    	List<Message> unread = m.getMessages(u, 25, type);
		
    	for (Message c : unread) {
    		UserInfo user = new UserInfo(c.getAuthor()); 
    		String msg = user.main(args);
    		
    		// Captcha validation is necessary. 
    		Captcha cap = new Captcha(restClient, new CaptchaDownloader());
    		String iden = cap.newCaptcha(u);
    		CaptchaDownloader.getCaptchaImage(iden);
    		Scanner userInputScanner = new Scanner(System.in);
    		System.out.print("Enter captcha: ");
    		String input = userInputScanner.nextLine();
    		
    		new Messages(restClient).compose(u, c.getAuthor(), "WordyBot", msg, iden, input);
    	}	
	}
}
