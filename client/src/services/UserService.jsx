import axiosService from './AxiosService.jsx';


class AdService {

    getUser(id){
        return axiosService.getRestClient().get(`${process.env.REACT_APP_DETAIL}${id}`)
    }

    createUser(data){
        return axiosService.getRestClient().post(`${process.env.REACT_APP_NEW}`, data)
    }
    
    updateUser(data){
        return axiosService.getRestClient().put(`${process.env.REACT_APP_EDIT}${data.id}`, data)
    }

    deleteUser(id){
        return axiosService.getRestClient().delete(`${process.env.REACT_APP_REMOVE}${id}`)
    }

    logoutUser(){
        return axiosService.getRestClient().get("/logout", {withCredentials: true});
    }


}

export default new AdService();
