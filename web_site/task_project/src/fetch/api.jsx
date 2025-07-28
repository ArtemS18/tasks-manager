import axios from "axios"
import qs from 'qs'

class Api{
    constructor(base_url){
        this.base_url = base_url
    }
    fetchAuthoData(username, password){
        return axios.post(
            `${this.base_url}/auth/token`,
            qs.stringify({ username, password }),
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        ).then((resp) => {
            if (resp.status == 200){
                return {success: true, ...resp.data}
            }
        }).catch((e)=> {
            console.log(e.response)
            if (e.response){
                 return {
                    success: false,
                    message: e.response.data || "Server error",
                    statuse: e.status
                 }
            }
        })
    }

}

export const api = new Api('http://localhost:8082')