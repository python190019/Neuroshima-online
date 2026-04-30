type DisplayTextProps = {
    zawartosc : string;
};

export default function DisplayText({
    zawartosc
}:DisplayTextProps){
    return <p>{zawartosc}</p>
}