type TextInputProps = {
    value: string;
    onChange: (newValue: string) => void;
    placeholder?: string;
};

export default function TextInput({
    value,
    onChange,
    placeholder = "Type here...",
}: TextInputProps) {
    return (
        <input
            type = "text"
            value = {value}
            onChange={(event) => onChange(event.target.value)}
            placeholder = {placeholder}
        />
    )
}