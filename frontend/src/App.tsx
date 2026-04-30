import { useState } from "react";
import LoginScreen from "./Loginscreen";
function App() {
  const [name, setName] = useState("");
  return (
    LoginScreen()
  );
}

export default App;