/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.tika.parser.ner;

import org.apache.tika.Tika;
import org.apache.tika.config.TikaConfig;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ner.opennlp.OpenNLPNERecogniser;
import org.apache.tika.parser.ner.regex.RegexNERecogniser;
import org.json.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.junit.Test;

import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.nio.charset.Charset;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

import static org.junit.Assume.assumeTrue;

/**
 *Test case for {@link NamedEntityParser}
 */
public class NamedEntityParserTest{

    public static final String CONFIG_FILE = "tika-config.xml";

    @Test
    public void testParse() throws Exception {

        //test config is added to resources directory
        TikaConfig config = new TikaConfig(getClass().getResourceAsStream(CONFIG_FILE));
        Tika tika = new Tika(config);
        
        JSONParser parser = new JSONParser();
        String text="";
        
        HashMap<Integer,String> hmap = new HashMap<Integer,String>();
        HashMap<String,HashMap<Integer,String>> outerhmap = new HashMap<String,HashMap<Integer,String>>();
        
        int index=0;
        //Input Directory Path
        String inputDirPath = "/Users/AravindMac/Desktop/polardata_json_grobid/application_pdf";
        int count = 0;
        try {
 
        	File root = new File(inputDirPath);
        	File[] listDir = root.listFiles();
            for(File filename : listDir){
            	
	        	if(!filename.getName().equals(".DS_Store") && count < 3573){
	        		count+=1;
	        		System.out.println(count);
	        				
	        		String absoluteFilename = filename.getAbsolutePath().toString();
	        		
	        	//	System.out.println(absoluteFilename);
	        		 //Read the json file, parse and retrieve the text present in the content field.
		        	   
		            Object obj = parser.parse(new FileReader(absoluteFilename));
		            
		            BufferedWriter bw = new BufferedWriter(new FileWriter(new File(absoluteFilename)));
		                
		            JSONObject jsonObject = (JSONObject) obj;
		            text = (String) jsonObject.get("content");
		            
		            Metadata md = new Metadata();
		            tika.parse(new ByteArrayInputStream(text.getBytes()), md);
		            
		            //Parse the content and retrieve the values tagged as the NER entities
		            HashSet<String> set = new HashSet<String>();
		            set.addAll(Arrays.asList(md.getValues("X-Parsed-By")));
		            
		            // Store values tagged as NER_PERSON
		            set.clear();
		            set.addAll(Arrays.asList(md.getValues("NER_PERSON")));
		            
		            hmap = new HashMap<Integer,String>();
		            index=0;
		            
		            for(Iterator<String> i = set.iterator();i.hasNext();){
		            	String f = i.next();
		            	hmap.put(index,f);
		            	index++;
		            }
		            
		            if(!hmap.isEmpty()){
		            	outerhmap.put("PERSON", hmap);
		            }
		            
		            // Store values tagged as NER_LOCATION
		            set.clear();
		            set.addAll(Arrays.asList(md.getValues("NER_LOCATION")));
		            hmap = new HashMap<Integer,String>();
		            index=0;
		            
		            for(Iterator<String> i = set.iterator();i.hasNext();){
		            	String f = i.next();
		            	hmap.put(index,f);
		            	index++;
		            }
		            
		            if(!hmap.isEmpty()){
		            	outerhmap.put("LOCATION", hmap);	
		            }
		            
		            //Store values tagged as NER_ORGANIZATION
		            set.clear();
		            set.addAll(Arrays.asList(md.getValues("NER_ORGANIZATION")));
		            
		            hmap = new HashMap<Integer,String>();
		            index=0;
		            
		            for(Iterator<String> i = set.iterator();i.hasNext();){
		            	String f = i.next();
		            	hmap.put(index,f);
		            	index++;
		            }
		            
		            if(!hmap.isEmpty()){
		            	outerhmap.put("ORGANIZATION", hmap);
		            }
		            
		            // Store values tagged as NER_DATE
		            set.clear();
		            set.addAll(Arrays.asList(md.getValues("NER_DATE")));
		            
		            hmap = new HashMap<Integer,String>();
		            index=0;
		            
		            for(Iterator<String> i = set.iterator();i.hasNext();){
		            	String f = i.next();
		            	hmap.put(index,f);
		            	index++;
		            }

		            if(!hmap.isEmpty()){
		            	outerhmap.put("DATE", hmap);
		            }
		            
		            JSONArray array = new JSONArray();
					array.put(outerhmap);
					if(!outerhmap.isEmpty()){
						jsonObject.put("OpenNLP", array);		//Add the NER entities to the json under NER key as a JSON array.
					}
					
		            System.out.println(jsonObject);
		            
		            bw.write(jsonObject.toJSONString());	//Stringify thr JSON and write it back to the file 
		            bw.close();
		            
	        		}
	        	}
        	} catch (Exception e) {
        			e.printStackTrace();
        		}
        
    }

    /*@Test
    public void testNerChain() throws Exception {
        String classNames = OpenNLPNERecogniser.class.getName()
                + "," + RegexNERecogniser.class.getName();
        System.setProperty(NamedEntityParser.SYS_PROP_NER_IMPL, classNames);
        TikaConfig config = new TikaConfig(getClass().getResourceAsStream(CONFIG_FILE));
        Tika tika = new Tika(config);
        String text = "University of Southern California (USC), is located in Los Angeles ." +
                " Campus is busy from monday to saturday";
        Metadata md = new Metadata();
        tika.parse(new ByteArrayInputStream(text.getBytes(Charset.defaultCharset())), md);
        HashSet<String> keys = new HashSet<String>(Arrays.asList(md.getValues("NER_WEEK_DAY")));
        System.out.println(keys);
        assumeTrue(keys.contains("monday"));
        
        keys.clear();
        keys.addAll(Arrays.asList(md.getValues("NER_LOCATION")));
        System.out.println(keys);
        assumeTrue(keys.contains("Los Angeles"));
        
     }*/
}