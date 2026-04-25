import { useState } from "react";

async function register(username : string, password : string, url : string) {
    const response = await fetch(url, {
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
        },
        body : JSON.stringify({username, password})
    })
    const data = await response.json();
    if(!response.ok){
        throw new Error(data.error || "Registration failed");
    }
    return data;
}