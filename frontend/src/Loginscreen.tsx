import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";


async function cos(name : string) {
  console.log(name);
}


export default function LoginScreen(){
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    return(
        <div>
            <DisplayText zawartosc="Username"></DisplayText>
            <TextInput value={name} onChange={setName} placeholder="Enter Username" ></TextInput>
            <DisplayText zawartosc="Password"></DisplayText>
            <TextInput value={password} onChange={setPassword} placeholder="Enter Password"></TextInput>
            <Button onClick={() => cos(name)} zawartosc="Login"></Button>
        </div>
    )
}