import React from 'react';

const ChatHistory = ({ messages, onClearHistory }) => {
  if (!messages || messages.length === 0) {
    return (
      <div className="chat-history empty">
        <p>No messages in history</p>
      </div>
    );
  }

  return (
    <div className="chat-history">
      <div className="chat-history-header">
        <h3>Chat History</h3>
        {onClearHistory && (
          <button onClick={onClearHistory} className="clear-history-button">
            Clear History
          </button>
        )}
      </div>
      <div className="chat-history-messages">
        {messages.map((message) => (
          <div key={message.id} className={`history-message ${message.role}`}>
            <div className="history-message-header">
              <span className="message-role">{message.role}</span>
              <span className="message-time">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div className="history-message-content">
              {message.content}
            </div>
            {message.sources && message.sources.length > 0 && (
              <div className="history-message-sources">
                Sources: {message.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatHistory;