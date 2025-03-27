import React from "react";

export const MessageBubble = ({ message }) => {
    const isUser = message.role === "user";
    return (
        <div className={`message-bubble ${isUser ? "user" : "assistant"}`}>
            {message.content}
        </div>
    );
};
