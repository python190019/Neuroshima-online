import { useState } from "react";
import LoginScreen from "./Loginscreen";
import RegisterScreen from "./Registerscreen";

export default function App() {
  const [screen, setScreen] = useState<"login" | "register">("login");
  function SwitchToLogin(){
    setScreen("login");
  }
  function SwitchToRegister(){
    setScreen("register");
  }

  return (
    <div>
      {screen === "login" ? (
      <LoginScreen onSwitchToRegister={SwitchToRegister} />
    ) : (
      <RegisterScreen onSwitchToLogin={SwitchToLogin} />
    )}
    </div>
  );
}