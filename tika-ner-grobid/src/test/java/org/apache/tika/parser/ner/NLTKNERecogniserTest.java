/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright owlocationNameEntitieship.
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
import org.apache.tika.parser.ner.NamedEntityParser;
import org.apache.tika.parser.ner.nltk.NLTKNERecogniser;
import org.json.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.junit.Test;

import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import static org.junit.Assert.assertTrue;

public class NLTKNERecogniserTest {
    @Test
    public void testGetEntityTypes() throws Exception {
        System.setProperty(NamedEntityParser.SYS_PROP_NER_IMPL, NLTKNERecogniser.class.getName());
        Tika tika = new Tika(new TikaConfig(NamedEntityParser.class.getResourceAsStream("tika-config.xml")));
        
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
            	
	        	if(!filename.getName().equals(".DS_Store") && count < 3239){
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
		            
		            // Store values tagged as NER_NAMES
		            set.addAll(Arrays.asList(md.getValues("NER_NAMES")));
		            
		            hmap = new HashMap<Integer,String>();
		            index=0;
		            
		            for(Iterator<String> i = set.iterator();i.hasNext();){
		            	String f = i.next();
		            	hmap.put(index,f);
		            	index++;
		            }
		            
		            if(!hmap.isEmpty()){
		            	outerhmap.put("NAMES", hmap);
		            }
		            
		            JSONArray array = new JSONArray();
					array.put(outerhmap);
					
					if(!outerhmap.isEmpty()){
						jsonObject.put("NLTK", array);		//Add the NER entities to the json under NER key as a JSON array.
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
}
