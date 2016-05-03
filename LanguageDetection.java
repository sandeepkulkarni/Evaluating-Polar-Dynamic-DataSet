package org.apache.tika.parser.ner.grobid;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import org.apache.tika.language.LanguageIdentifier;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class LanguageDetection {
	public static void main(String[] args){
		//Input Directory Path
	    String inputDirPath = "/Users/AravindMac/Desktop/polardata_json/text_html_train_final";
	    File root = new File(inputDirPath);
	    File[] listDir = root.listFiles();
	    int count = 0;
	    //Iterate through all the files listed in the directory path passed as input
	    for(File filename : listDir){
	        try {
	        		count+=1;
	        		System.out.println(count);
	        		if(!filename.getName().equals(".DS_Store")){
	        			String absoluteFilename = filename.getAbsolutePath().toString();
	        			JSONParser parser = new JSONParser();
	        			String text="";
	        			//Parse the file
	        			Object obj = parser.parse(new FileReader(absoluteFilename));
		            
		        	    BufferedWriter bw = new BufferedWriter(new FileWriter(new File(absoluteFilename)));

		        	    //Read the json file, parse and retrieve the text present in the content field.

		        	    JSONObject jsonObject = (JSONObject) obj;
		        	    text = (String) jsonObject.get("content");

		        	    //Use the language identifier to identify the language of the text
		        	    LanguageIdentifier identifier = new LanguageIdentifier(text);
		        	    System.out.println(identifier.getLanguage());
		        	    
		        	    jsonObject.put("Language",identifier.getLanguage());
		        	    System.out.println(jsonObject.toJSONString());
		        	    bw.write(jsonObject.toJSONString());	//Stringify the JSON and write it back to the file with the language
		        	    bw.close();
	    
	        			}
	        }
	        catch(Exception ex){
	        	ex.printStackTrace();
	        	continue;
	        }
	    }
	}
}
