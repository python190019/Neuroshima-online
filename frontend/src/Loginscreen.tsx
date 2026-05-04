import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { Login } from "./features/auth/Login";

type LoginScreenProps = {
    onSwitchToRegister: () => void;
};

export default function LoginScreen({onSwitchToRegister} : LoginScreenProps){
    let url = "http://localhost:8080/api/auth/login";
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
            <Button onClick={() => Login(name, password, url)} zawartosc="Login"></Button>
            <DisplayText zawartosc="You don't have an account?"></DisplayText>
            <Button onClick={onSwitchToRegister} zawartosc="Register"></Button>
        </div>
    )
}