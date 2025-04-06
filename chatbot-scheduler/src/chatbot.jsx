import { useState, useRef, useEffect } from "react";
import IU_Logo from "./assets/IU Logo.png";
import Robit from "./assets/Robit.png";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { chooseDegreeOffInterests } from "./assets/parseMajors";
import { marked } from "marked";

const ai = new GoogleGenerativeAI("AIzaSyDaFG2DfySbZothZJf-q9Sjapgc67WRW1g");

export default function ChatbotInterface() {
  const [chatBranchState, setChatBranchState] = useState('Initial State');
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi there! I'm your Scheduling Assistant 🤖\n I’m here to help remove the stress of forging your academic journey! Whether you're exploring majors and minors that match your interests, or wanting to schedule your semester based off of interests, as an AI assistant, I've got you covered. Let’s make planning your future a breeze! Just tell me whether you want to explore minors, explore majors, or schedule for next semester! 🎓📅", sender: "bot" },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsTyping(true);

    const botText = await getBotResponse(inputValue);

    const botMessage = {
      id: messages.length + 2,
      text: botText,
      sender: "bot",
    };

    setMessages((prev) => [...prev, botMessage]);
    setIsTyping(false);
  };

  async function sendTextToServer({ text, state }) {
    try {
        const response = await fetch("https://gshores.pythonanywhere.com/process", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            credentials: "include",  // ✅ ADD THIS LINE
            body: JSON.stringify({ text, state })
          });
  
      if (!response.ok) {
        throw new Error("Server error");
      }
  
      const data = await response.json();
      return { text: data.result };
    } catch (err) {
      console.error("Backend error:", err);
      return { text: "⚠️ Something went wrong with the server." };
    }
  }

  const getBotResponse = async (input) => {
  try {
    const botResponse = await sendTextToServer({ text: input, state: chatBranchState });

    console.log("Bot response:", botResponse); // Should show: { result: [text, state] }

    setChatBranchState(botResponse.text.state);

    return botResponse.text.text;
  } catch (err) {
    console.error("Error fetching Gemini response:", err);
    return "Sorry, I had trouble processing that. Try again!";
  }
};


  return (
    <div className="flex flex-col h-screen bg-[#660000] p-4">
      <img src={IU_Logo} alt="IU Logo" className="h-12 w-auto mb-4 mx-auto" />

      <div className="flex-1 bg-white rounded-lg shadow-md mb-4 overflow-y-auto flex flex-col">
        <div className="flex items-center space-x-4 p-4 border-b border-gray-300">
          <img
            src={Robit}
            alt="IU Assistant"
            className="h-10 w-10 rounded-full object-cover"
          />
          <div>
            <h2 className="text-base font-semibold text-gray-800">
              EduAdvisorAI
            </h2>
            <p className="text-xs text-gray-500">Online</p>
          </div>
        </div>

        <div className="flex flex-col space-y-4 p-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
  className={`max-w-[70%] rounded-lg px-4 py-2 ${
    message.sender === "user"
      ? "bg-[#990000] text-white rounded-br-none"
      : "bg-gray-200 text-gray-800 rounded-bl-none"
  }`}
  dangerouslySetInnerHTML={{ __html: marked.parse(message.text) }}
></div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 rounded-lg rounded-bl-none px-4 py-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0.4s" }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border bg-gray-100 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="bg-[#990000] hover:bg-[#660000] text-white px-4 py-2 rounded-lg transition-colors border-gray-100 border-[.5px]"
        >
          Send
        </button>
      </form>
    </div>
  );
}
