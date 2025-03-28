import { useState, useEffect, useRef } from "react";
import { MessageBubble } from "./MessageBubble";
import "./../styles/chatbot.css";

export const Chatbot = ({ messages, setMessages }) => {
    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [theme, setTheme] = useState("light"); // Light theme by default
    const messagesEndRef = useRef(null);  // Ref to scroll to the bottom

    // Handle theme switching
    const toggleTheme = () => {
        setTheme(theme === "light" ? "dark" : "light");
    };

    // Auto scroll to the bottom whenever new messages are added
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);  // Runs every time messages change

    useEffect(() => {
        document.body.className = theme + "-theme";  // Apply theme globally
    }, [theme]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const newMessages = [...messages, { role: "user", content: input }];
        setMessages(newMessages);
        setInput("");
        setIsTyping(true);

        try {
            const response = await fetch("/api/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: input, chat_history: newMessages }),
            });

            const reader = response.body.getReader();
            let result = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = new TextDecoder("utf-8").decode(value);
                result += chunk;

                // Progressive response updates
                setMessages([...newMessages, { role: "assistant", content: result }]);
            }
        } catch (error) {
            console.error("Error fetching response:", error);
        } finally {
            setIsTyping(false);
        }
    };

    // Handle the Enter key press
    const handleKeyPress = (e) => {
        if (e.key === "Enter") {
            e.preventDefault();  // Prevent the default behavior (like a line break)
            sendMessage();       // Trigger sendMessage when Enter is pressed
        }
    };

    return (
        <div className="chat-container">
            {/* Contact Name (MY BUDDY) with Avatar */}
            <div className="contact-info">
                <div className="avatar">
                    <img src="icon.png" alt="Buddy Avatar" /> {}
                </div>
                <div className="contact-name">MY BUDDY</div> {/* Updated Contact Name */}
            </div>

            {/* Theme Toggle Button */}
            <button className="theme-switcher" onClick={toggleTheme}>
                {theme === "light" ? "🌙" : "☀️"}
            </button>

            <div className="messages">
                {messages.map((msg, index) => (
                    <MessageBubble key={index} message={msg} />
                ))}
                {isTyping && <div className="typing-indicator">MY BUDDY is typing...</div>}
                <div ref={messagesEndRef} /> {/* Scroll target */}
            </div>

            <div className="input-container">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}  // Listen for Enter key press
                    placeholder="Hi I am your friend..."
                    className="input-field"
                />
                <button onClick={sendMessage} className="send-button">Send</button>
            </div>
        </div>
    );
};
