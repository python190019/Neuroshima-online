import React from "react";
import "./Hexagon.css";

type HexagonProps = {
    x: number;
    y: number;
    size?: number;
    color?: string;
    rotation?: number;
    onClick?: () => void;
    children?: React.ReactNode;
};

const Hexagon: React.FC<HexagonProps> = ({
    x,
    y,
    size = 100,
    color = "#4CAF50",
    rotation = 0,
    onClick,
    children,
}) => {
    const height = size * 0.866;

    return (
        <div
            className="hexagon"
            // onClick={onClick}
            onClick={() => console.log("Clicked hex:", { x, y })}
        style={{
            width: size,
            height: height,
            backgroundColor: color,
            position: "absolute",
            left: x,
            top: y,
            transform: `rotate(${rotation}deg) scale(1) translate(350%, 50%)`,    // potem do zmiany w celu
         }}                                                                       // wysrodkowania, na razie
                                                                                 // dopasowane do consoli
        >
        < div className="hexagon-content">{children}</div>
         </div>
    );
};

export default Hexagon;