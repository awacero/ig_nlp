
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


def store_in_mongodb(mongodb_client):

    try:
        pass

    except Exception as e:


        pass


