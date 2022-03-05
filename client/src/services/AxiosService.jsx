import axios from 'axios'


class AxiosService {


    constructor() {
        console.log("Axios Service is instantiated");
    }

    getRestClient() {
        if (!this.serviceInstance) {
            this.serviceInstance = axios.create({
            baseURL: 'http://localhost:5000/api',
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json'
            },
        });
        }
        return this.serviceInstance;
    }
}
    
    
    
export default (new AxiosService());