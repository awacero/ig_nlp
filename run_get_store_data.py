

import nlp_utils
import sys
import logging,  logging.config


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
            output = run_parameters['RUN_MODE']['output']
            data_source = run_parameters['RUN_MODE']['data_source']
            account_name = run_parameters['ACCOUNT_INFO']['account_name']
            
            print(output,data_source,account_name)
            
        except Exception as e:
            logger.error("Error reading RUN_MODE parameter: %s" %e)
        
        ##ADD RECOVER LIST OF EVENTS OPTION FOR BOTH FB AND TWT 

        if data_source == "FACEBOOK":
            #DO FB STUFF
            # get fb token
            # get twt api 
            token_file = run_parameters['TOKEN_FILE']['facebook_token_file']
            token = nlp_utils.read_json_file(token_file)
            print(token)
            pass
        elif data_source == "TWITTER":
            #DO TWT STUFF
            # get twt token
            # get twt api

            pass


main()