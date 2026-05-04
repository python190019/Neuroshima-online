import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { Login } from "./features/auth/Login";
// import { Register } from "./features/auth/Register";

async function cos(name : string) {
  console.log(name);
}

export default function LoginScreen(){
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    return(
        <div>
            {/* <form>
                <input type="text">Login</input>

            </form> */}
            <DisplayText zawartosc="Username"></DisplayText>
            <TextInput value={name} onChange={setName} placeholder="Enter Username" ></TextInput>
            <DisplayText zawartosc="Password"></DisplayText>
            <TextInput value={password} onChange={setPassword} placeholder="Enter Password"></TextInput>
            <Button onClick={() => Login(name, password)} zawartosc="Login"></Button>
        </div>
    )
}