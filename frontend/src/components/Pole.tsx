import imgPath from "../assets/inne/pole.png"
import styles from "./modules/Pole.module.css"

type PoleProps = {
    id : number;
    x : number;
    y : number;
    onClick? : (id:number) => void;
};

export default function Pole({id, x, y, onClick} : PoleProps){
    return <img
    src={imgPath}
    alt="Pole"
    className={styles.pole}
    style={{
        left: `${x}px`,
        top: `${y}px`,
    }}
    onClick={() => onClick?.(id)}
    > </img>
}