import React from "react";
import Hexagon from "./components/Hexagon";
import GetWindowSize from "./GetScreenSize";

async function cos(name : string) {
  console.log(name);
}

export default function HexTest(){
    const { width, height } = GetWindowSize();
    const ScreenWidth = width;
    const ScreenHeight = height;

    const CenterX = ScreenWidth / 2;
    const CenterY = ScreenHeight / 2;

    const Size = height / 10;


    const Items = [];

    for(let q = -2; q <= 2; q++){
        const rMin = Math.max(-2, -q - 2);
        const rMax = Math.min(2, -q + 2);

        for(let r = rMin; r <= rMax; r++){

            const X = Size * (Math.sqrt(3) * q + Math.sqrt(3)/2 * r);
            const Y = Size * (3/2 * r);
            const FinalX = X + CenterX;
            const FinalY = Y + CenterY;
            Items.push(
            <Hexagon x={X} y={Y} size={Size * 2 - 5} rotation={30} color="#2196F3" />     // w razie czego do
            )                                                                               // zamiany na Final
        }
    }

    return (
        <div>
            {Items}
        </div>
    )
}