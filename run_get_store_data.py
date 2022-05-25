
from pymongo import MongoClient
import get_facebook_data 
import nlp_utils
import sys
import logging,  logging.config
import csv

if nlp_utils.check_file("./config/logging.ini"):
    logging.config.fileConfig('./config/logging.ini', disable_existing_loggers=False)
    logger=logging.getLogger('run_rsam')


def main():

    """
    Get data from twitter of facebook and store it in CSV or MONGODB
    """
    if len(sys.argv)==1:         
        is_error=True
    else:
        try:
            run_parameters = nlp_utils.read_parameters(sys.argv[1])
        
        except Exception as e:
            logging.error("Error reading configuration sets in file: %s" %str(e))
            raise Exception("Error reading configuration sets in file: %s" %str(e))

        try:
            data_source = run_parameters['RUN_MODE']['data_source']
            output = run_parameters['RUN_MODE']['output']
            mode = run_parameters['RUN_MODE']['mode']
            account_name = run_parameters['ACCOUNT_INFO']['account_name']
            mongo_file = run_parameters['MONGODB']['db_server_file']
            mongo_info = nlp_utils.read_json_file(mongo_file)
            mongo_id = run_parameters['MONGODB']['mongo_id']
            
        except Exception as e:
            logger.error("Error reading RUN_MODE parameter: %s" %e)
        
        if data_source == "FACEBOOK":

            token_file = run_parameters['TOKEN_FILE']['facebook_token_file']
            token_info = nlp_utils.read_json_file(token_file)
            token = token_info[account_name]['token']
            fb_api = get_facebook_data.get_facebook_api(token)
            fields = run_parameters['FACEBOOK']['fields']
            limit = run_parameters['FACEBOOK']['limit']
            store_path = run_parameters['STORE']['data_path']
            ##AGREGAR OPCION DE PREPROCESAR MSGS ANTES DE GUARDAS
            if mode == 'SINGLE':
                logging.info("SINGLE mode")
                facebook_post_id = sys.argv[2]
                post_messages = get_facebook_data.download_facebook_messages(facebook_post_id,fb_api,fields,limit)
                
            elif mode == 'LIST':
                logging.info("LIST mode")
                post_list_file = sys.argv[2]
                with open(post_list_file,newline='') as csvfile:
                    csv_reader = csv.read(csvfile,delimiter='|')
                    for row in csv_reader:
                        if row:
                            fb_id=row[0]
                            post_messages = get_facebook_data.download_facebook_messages(fb_id,fb_api,fields,limit)
            
            if output == 'CSV':
                get_facebook_data.store_on_disk(store_path,post_messages)
            
            elif output == 'MONGODB':
                mongo_host = mongo_info[mongo_id]['host']
                mongo_port = mongo_info[mongo_id]['port']
                mongo_DB_name = mongo_info[mongo_id]['DB_name']
                mongo_user = mongo_info[mongo_id]['user']
                mongo_pass = mongo_info[mongo_id]['pass']
                

                try:
                    client = MongoClient("mongodb://%s:%s@%s:%s/%s" %(mongo_user,mongo_pass,
                                                        mongo_host,mongo_port, mongo_DB_name
                                                                ))
                    db = client['fb_messages']

                    ##Crear la base de datos fb_messages
                    #nodb = cliente["fb_messages"]
                    ##Crear una collection
                    #Collection = nodb["post_messages"]
                    print(client)
                    print(db)
                except Exception as e:
                    print("Error in create mongodb_client: %s" %str(e))    



        elif data_source == "TWITTER":
            #DO TWT STUFF
            # get twt token
            # get twt api
            token_file = run_parameters['TOKEN_FILE']['twitter_token_file']
            token = nlp_utils.read_json_file(token_file)


    

main()