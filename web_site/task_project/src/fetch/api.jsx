import axios from "axios"
import qs from 'qs'

class Api{
    constructor(base_url){
        this.base_url = base_url
    }
    updateTgId(token, tgId) {
    return axios.patch(
        `${this.base_url}/internal/users/me/tg_id`,
        { 'tg_id': tgId },
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    ).then((resp) => {
        console.log(resp);
        if (resp.statusText == "OK") {
            return { success: true, ...resp.data };
        } else {
            return { success: false, message: "Unexpected response", status: resp.status };
        }
    }).catch((e) => {
        console.log(e);
        if (e.response) {
            return {
                success: false,
                message: e.response.data || "Server error",
                status: e.response.status
            };
        } else {
            return {
                success: false,
                message: "Network or unknown error",
                status: null
            };
        }
    });
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
                    status: e.status
                 }
            }
        })
    }

    fetchRegData(name, password, login){
        return axios.post(
            `${this.base_url}/auth/reg`,
            { name, password, login},
            { headers: { 'Content-Type': 'application/json' } }
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
                    status: e.status
                 }
            }
        })
    }

    fetchConfirmData(confirm_token, password){
        return axios.post(
            `${this.base_url}/auth/confirm`,
            { confirm_token, password},
            { headers: { 'Content-Type': 'application/json' } }
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
                    status: e.status
                 }
            }
        })
    }

}

export const api = new Api('http://localhost:8080', )