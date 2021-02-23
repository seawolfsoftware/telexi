export default class APIService {


    static UpdatePressevent(pressevent_id, body){

        return fetch(`https://telexi.seawolfsoftware.io/api/v1/${pressevent_id}/`,
        {
            'method': 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body:JSON.stringify(body)
        }).then(resp => resp.json())

    }

    static InsertPressevent(body){
        return fetch(`https://telexi.seawolfsoftware.io/api/v1/`,
                    {
            'method': 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body:JSON.stringify(body)
    }).then(resp => resp.json())
}
}
