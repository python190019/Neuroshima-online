import { useState } from "react";
import LoginScreen from "./Loginscreen";
import HexTest from "./HexTest";

function App() {
  const [name, setName] = useState("");
  return (
    // LoginScreen()
    HexTest()
  );
}

export default App;