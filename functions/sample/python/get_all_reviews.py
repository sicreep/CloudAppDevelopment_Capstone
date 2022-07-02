from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    if 'dealerId' in dict:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])

        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict['URL'])
    
        response = service.post_find(
            db='reviews',
            selector={'dealership': {'$eq': int(dict['dealerId'])}}
        ).get_result()

        if response['bookmark'] == 'nil':
            result = {
                'status' : 404,
                'message' : 'Error: Not found.'
            }
            return(result)

        result = {
            'reviews' : response
        }
        return(result)
        
    else:
        result = {
            'status' : 404,
            'message' : 'Error: Not found.'
        }
        return(result)
