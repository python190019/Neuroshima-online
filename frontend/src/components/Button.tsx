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
    return <button type={type} onClick={onClick}>
        {zawartosc}
    </button>
}