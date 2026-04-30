import React from "react";
import Hexagon from "./components/Hexagon";

async function cos(name : string) {
  console.log(name);
}

export default function HexTest(){
    return (
        <div>
            <Hexagon x={100} y={100} size={120} rotation={30} color="#2196F3">
                Hex
            </Hexagon>
        </div>
    )
}