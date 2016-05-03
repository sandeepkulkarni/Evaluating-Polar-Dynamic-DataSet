package org.apache.tika.parser.ner.grobid;

import java.util.Map;
import java.util.Set;

import org.apache.tika.parser.ner.NERecogniser;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.io.IOException;
import java.net.URLEncoder;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Properties;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.apache.cxf.jaxrs.client.WebClient;

public class GrobidNERecogniser implements NERecogniser{

	private static final Logger LOG = LoggerFactory.getLogger(GrobidNERecogniser.class);
    private static boolean available = false;
    private static final String GROBID_REST_HOST = "http://localhost:8080";
    private String restHostUrlStr;
	
    /*
     * Useful Entities from Grobid NER 
     */
    public static final Set<String> ENTITY_TYPES = new HashSet<String>(){{
        add("MEASUREMENT_NUMBERS");
        add("MEASUREMENT_UNITS");
        add("MEASUREMENTS");
        add("NORMALIZED_MEASUREMENTS");
    }};


    public GrobidNERecogniser(){
        try {

	            String restHostUrlStr="";
	            try {
	                restHostUrlStr = readRestUrl();
	            } catch (IOException e) {
	                e.printStackTrace();
	            }

	            if (restHostUrlStr == null || restHostUrlStr.equals("")) {
	                this.restHostUrlStr = GROBID_REST_HOST;
	            } else {
	                this.restHostUrlStr = restHostUrlStr;
	            }

	            Response response = WebClient.create(restHostUrlStr).accept(MediaType.APPLICATION_JSON).get();
	            int responseCode = response.getStatus();
	            if(responseCode == 200){
	                available = true;
	            }
	            else{
	                LOG.info("Grobid REST Server is not running");
	            }
	
        	}
        	catch (Exception e) {
            	LOG.info(e.getMessage(), e);
        	}
    }

    /**
     * Reads the GROBID REST URL from the properties file
     * returns the GROBID REST URL
     */
    private static String readRestUrl() throws IOException {
    	Properties grobidProperties = new Properties();
        grobidProperties.load(GrobidNERecogniser.class.getClassLoader().getResourceAsStream("GrobidServer.properties"));
        return grobidProperties.getProperty("grobid.server.url");
    }
    
    /**
     * Reads the GROBID REST Endpoint from the properties file
     * returns the GROBID REST Endpoint
     */
    private static String readRestEndpoint() throws IOException {
    	Properties grobidProperties = new Properties();
        grobidProperties.load(GrobidNERecogniser.class.getClassLoader().getResourceAsStream("GrobidServer.properties"));
        return grobidProperties.getProperty("grobid.endpoint.text");
    }

    /**
     * @return {@code true} if server endpoint is available.
     * returns {@code false} if server endpoint is not avaliable for service.
     */
    public boolean isAvailable() {
        return available;
    }

    /**
     * Gets set of entity types recognised by this recogniser
     * @return set of entity classes/types
     */
    public Set<String> getEntityTypes() {
        return ENTITY_TYPES;
    }

    /**
     * Converts JSON Object to JSON Array 
     * @return a JSON array
     */
    public JSONArray convertToJSONArray(JSONObject obj, String key){
    	JSONArray jsonArray = new JSONArray();
    	try{
    		jsonArray = (JSONArray) obj.get(key);
    	}
    	catch(Exception e){
    	   	LOG.info(e.getMessage(), e);
        }
    	return jsonArray;
    }
    
    /**
     * Parses a JSON String and converts it to a JSON Object 
     * @return a JSON Object
     */
    public JSONObject convertToJSONObject(String jsonString){
    	JSONParser parser = new JSONParser();
    	JSONObject jsonObject = new JSONObject();
    	try{
    		jsonObject = (JSONObject) parser.parse(jsonString);
    	}
    	catch(Exception e){
    	   	LOG.info(e.getMessage(), e);
        }
		return jsonObject;
    }
    /**
     * recognises names of entities in the text
     * @param text text which possibly contains names
     * @return map of entity type -> set of names
     */
    public Map<String, Set<String>> recognise(String text) {
       
    	Map<String, Set<String>> entities = new HashMap<String,Set<String>>();
        Set<String> measurementNumberSet = new HashSet<String>();
        Set<String> unitSet = new HashSet<String>();
        Set<String> measurementSet = new HashSet<String>();
        Set<String> normalizedMeasurementSet = new HashSet<String>();
        
        try {
            //String url = restHostUrlStr + readRestEndpoint()+ "?text=" + URLEncoder.encode(text,"UTF-8");
            //Response response = WebClient.create(url).accept(MediaType.APPLICATION_JSON).get();
            String url = restHostUrlStr + readRestEndpoint();
            Response response = WebClient.create(url).accept(MediaType.APPLICATION_JSON).post("text=" + text);
            int responseCode = response.getStatus();
            System.out.println(responseCode);
            
            if (responseCode == 200) {
                String result = response.readEntity(String.class);
                JSONObject jsonObject = convertToJSONObject(result);
                JSONArray measurements = convertToJSONArray(jsonObject, "measurements");
                for(int i=0; i<measurements.size(); i++){
                	
                	StringBuffer measurementString = new StringBuffer();
                	StringBuffer normalizedMeasurementString = new StringBuffer();
                	
                	JSONObject quantity = (JSONObject) convertToJSONObject(measurements.get(i).toString()).get("quantity");
                	
                	if(quantity.containsKey("rawValue")){
                		String measurementNumber = (String) convertToJSONObject(quantity.toString()).get("rawValue");
                		measurementString.append(measurementNumber);
                    	measurementString.append(" ");
                    	measurementNumberSet.add(measurementNumber);
                	}
                	
                	if(quantity.containsKey("normalizedQuantity")){
                		Long normalizedMeasurementNumber = (Long) convertToJSONObject(quantity.toString()).get("normalizedQuantity");
                		normalizedMeasurementString.append(normalizedMeasurementNumber.toString());
                    	normalizedMeasurementString.append(" ");
                	}
                	
                	JSONObject jsonObj = (JSONObject) convertToJSONObject(quantity.toString());
                	
                	if(jsonObj.containsKey("rawUnit")){
                		JSONObject rawUnit = (JSONObject) jsonObj.get("rawUnit");
                		String unitName = (String) convertToJSONObject(rawUnit.toString()).get("name");
                		unitSet.add(unitName);
                		measurementString.append(unitName);
                	}
                	
                	if(jsonObj.containsKey("normalizedUnit")){
                		JSONObject normalizedUnit = (JSONObject) jsonObj.get("normalizedUnit");
                		String normalizedUnitName = (String) convertToJSONObject(normalizedUnit.toString()).get("name");
                		normalizedMeasurementString.append(normalizedUnitName);
                	}
                	
                	if(!measurementString.toString().equals("")){
                    	measurementSet.add(measurementString.toString());
                	}
                	
                	if(!normalizedMeasurementString.toString().equals("")){
                		normalizedMeasurementSet.add(normalizedMeasurementString.toString());
                	}
                	
                }
                entities.put("MEASUREMENT_NUMBERS",measurementNumberSet);
                entities.put("MEASUREMENT_UNITS",unitSet); 
                entities.put("MEASUREMENTS",measurementSet);
                entities.put("NORMALIZED_MEASUREMENTS",normalizedMeasurementSet);
                
            }
        }
        catch (Exception e) {
            LOG.info(e.getMessage(), e);
            
        }
        ENTITY_TYPES.clear();
        ENTITY_TYPES.addAll(entities.keySet());
        return entities;
    }
    
    public static void main(String[] args){
    	String text = " The French Republican Calendar's days consisted of ten hours of a hundred minutes of a hundred seconds, which marked a deviation from the duodecimal system used in many other devices by many cultures. The system was later abolished in 1806.[30]";
    	GrobidNERecogniser g = new GrobidNERecogniser();
    	Map<String, Set<String>> entities = new HashMap<String,Set<String>>();
    	entities = g.recognise(text);
    	System.out.println(entities);
    }
}


	