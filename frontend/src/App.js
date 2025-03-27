import { useState } from "react";
import { Chatbot } from "./components/Chatbot";

function App() {
    const [messages, setMessages] = useState([]);
    return <Chatbot messages={messages} setMessages={setMessages} />;
}

export default App;
