from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    if 'review' in dict:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
    
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict['URL'])
    
        if 'purchase' in dict['review']:
            if dict['review']['purchase'] == True:
                 review_doc = Document(
                    name = dict['review']['name'],
                    dealership = int(dict['review']['dealership']),
                    review = dict['review']['review'],
                    purchase = dict['review']['purchase'],
                    purchase_date = dict['review']['purchase_date'],
                    car_make = dict['review']['car_make'],
                    car_model = dict['review']['car_model'],
                    car_year = dict['review']['car_year']
                )
        else: 
            review_doc = Document(
                name = dict['review']['name'],
                dealership = int(dict['review']['dealership']),
                review = dict['review']['review'],
            )
    
        response = service.post_document(db='reviews', document=review_doc).get_result()

        if response['ok'] == True:
            return(response)
        else:
            result = {
                'status' : 500,
                'message' : 'Something went wrong.'
            }
            return(result)

    else:
        result = {
            'status' : 500,
            'message' : 'Something went wrong.'
        }
        return(result)
        