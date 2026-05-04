import styles from "./modules/Button.module.css";
// import type { ReactNode } from "react";

type WlasPrzycisku = {
    zawartosc : React.ReactNode;
    onClick? : () => void;
    type? : "button" | "submit" | "reset";
    variant? : "primary";
};

export default function Button({zawartosc, 
    onClick, 
    type = "button", 
    variant = "primary",
}:WlasPrzycisku){
    return <button className={styles.primaryButton} type={type} onClick={onClick}>
        {zawartosc}
    </button>
}