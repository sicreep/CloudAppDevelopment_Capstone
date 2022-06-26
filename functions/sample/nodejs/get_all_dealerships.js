const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    
    cloudant.setServiceUrl(params.COUCH_URL);
    
    selector = {
        // empty for all dealerships
    };

    try {
        let docList = await cloudant.postFind({
            db: 'dealerships',
            selector: selector,
            fields: ["id","city","state","st","address","zip","lat","long"],
        });
        return { "dealerships" : docList.result };

    } catch (error) {
        return { error: error.description };
    }
}