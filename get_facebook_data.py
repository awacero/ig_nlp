
import facebook
import logging 
import json
import nlp_utils 
import json
import datetime
import os

def get_facebook_api(facebook_token):
    """
    Get facebook api
    """
    try:
        return facebook.GraphAPI(facebook_token)
        
    except Exception as e:
        logging.error("Error in get_facebook_api(): %s" %str(e))
        raise("Error in get_facebook_api(): %s" %str(e))
    

def download_facebook_messages(fb_post_id, facebook_api,fields,limit):
    """
    Recover messages from a post and extra information like user_id, comments_count, etc. 
    """
    ## agregar capacidad de paginacion
    ## Crear funciones de prueba. 

    if fields:
        fields = fields
    else:
        fields="message,comment_count,like_count,created_time,message_tags,user_likes,is_hidden,likes,id,from,reactions{type,username},shares"
    
    if limit:
        limit = limit
    else:
        limit = 100
    
    try:
        complete_message = facebook_api.get_connections(id=fb_post_id,
                                                    connection_name='comments',
                                                    filter = "stream",
                                                    limit = limit,
                                                    fields = fields                                                     
                                                    )                                
        return complete_message
    except Exception as e:
        logging.error("Error in download_messages_complete: %s" %str(e))


def store_on_disk(store_path,messages_dict):

    if not os.path.exists(store_path):
        os.mkdir(store_path)

    timestamp_id = int(datetime.datetime.now().timestamp())
    
    try:
        with open("%s/messages_%s.json" %(store_path,timestamp_id),"w") as json_file:
            json.dump(messages_dict,json_file)
    
    except Exception as e:
        logging.error("Error creating file: %s" %str(e))
        raise("Error creating file: %s" %str(e)) 

#store_folder="./fbcomments_json/"
#fb_api=get_facebook_api(token_file_path, fanpage_name)


"""
##STORE MULTIPLE EVENTS IN MONGODB 
import csv

with open("/home/wacero/BORRAR/evento_id_fb_id.txt",newline='') as csvfile:
    csv_reader=csv.reader(csvfile,delimiter='|')
    for row in csv_reader:
        if row:
            fb_post_id=row[1]
            event_id=row[0]
            print(row[0],row[1])
            post_messages=download_messages_complete(fb_post_id, fb_api)
            store_all(store_folder, event_id,post_messages)
            print(post_messages)
            store_in_mongo("%s/%s.json" %(store_folder,event_id),fb_post_id,event_id)
        

"""

"""
event_id="igepn2019adej"
fb_post_id="663267810512102_1111325215706357"
post_messages=download_messages_complete(fb_post_id, fb_api)

store_all(store_folder, event_id,post_messages)

print(post_messages)

store_in_mongo("%s/%s.json" %(store_folder,event_id),fb_post_id,event_id)
"""



