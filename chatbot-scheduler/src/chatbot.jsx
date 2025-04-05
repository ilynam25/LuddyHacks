import { useState } from "react";
import IU_Logo from "./assets/IU Logo.png";
import Robit from "./assets/Robit.png";
import { GoogleGenerativeAI } from "@google/generative-ai";

const ai = new GoogleGenerativeAI("AIzaSyDaFG2DfySbZothZJf-q9Sjapgc67WRW1g");

export default function ChatbotInterface() {
  const [chatBranchState, setChatBranchState] = useState('Initial State');
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi there! I'm your Scheduling Assistant 🤖\n I’m here to help you plan your academic journey with ease! Whether you're looking for classes that fit your GenEd requirements, exploring majors and minors that match your interests, or wanting to learn more about a course’s average GPA—I’ve got you covered. I can also help you build your schedule based on your major and make sure everything fits together smoothly. Let’s make planning your future a breeze! 🎓📅", sender: "bot" },
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

  const getBotResponse = async (input) => {
    try {
        let model;
        let result = {};
        let text;
        switch(chatBranchState) {
            case 'Initial State':
                model = ai.getGenerativeModel({
                    model: "gemini-1.5-flash",
                    systemInstruction: `
                      You are a classifier. Return only a single number (and nothing else) based on the user's request:
                      Return 1 if they want help finding a single class.
                      Return 2 if they want help finding majors.
                      Return 3 if they want help finding minors.
                      Return 4 if they want to see information about a class, such as average GPA.
                      Return 5 if they want help scheduling a full semester of classes for their major.
                      Do not return 5 if they are only asking about scheduling an individual class.
                      If they imply multiple things, do 5.
                      Return -1 if they are asking about nothing related to the above, but only if absolutely not related.
                      Do not explain your answer. Do not include any text. Just return the number.
                    `
                  }); 
                  result = await model.generateContent([input]);
                  console.log("Gemini response:", result.response.text());
                  const responseText = result.response.text().trim();
                  switch (responseText) 
                  {
                    case '1':
                      text = "Great! I can help you find a single class. What are you looking for?";
                      setChatBranchState('Class Scheduling');
                      break;
                    case '2':
                      text = "Awesome! I can help you find majors. What are you interested in?";
                      setChatBranchState('Majors');
                      break;
                    case '3':
                      text = "Sure! I can help you find minors. What are you interested in?";
                      setChatBranchState('Minors');
                      break;
                    case '4':
                      text = "Sure! I can provide information about a class, such as average GPA. Which class are you interested in?";
                      setChatBranchState('Class Information');
                      break;
                    case '5':
                      text = "Sure! I can help you schedule a full semester of classes for your major. Which major are you interested in?";
                      setChatBranchState('Class Scheduling');
                      break;
                    case '-1':
                      text = "Sorry, I had trouble processing that. Try again!";
                      setChatBranchState('Initial State');
                      break;
                    default:
                      text = "Sorry, I had trouble processing that. Try again!";
                      setChatBranchState('Initial State');
                      break;
                  }
                  break;
            case 'Initial Clarification':
                text = "Sorry, I had trouble processing that. Try again!";
                setChatBranchState('Initial State');
                break;
            case 'Class Scheduling':
                chatBranchState = 'Final State';
                break;
            default:
                chatBranchState = 'Initial State';
        }

          
         /**
         const model = ai.getGenerativeModel({
            model: "gemini-1.5-flash",
            systemInstruction: 
            
          ` You are a classifier. You will return a strictly formatted list like in python of the following categories, Like this: [Data Science, Finance, Sports] nothing else.
          They will describe themselves and you will return at least 3 (More if possible) categories that aligns with their interests. MAKE SURE IT IS ONLY THESE CATEGORIES YOU RETURN AND STRICTLY FORMATTED
          if what they say is not at all related to themselves or interests return -1
          'Nutrition', 'South America', 'Pop Culture', 'Legal Issues', 'Teaching',
            'Journalism', 'Sustainability', 'Finance', 'Nature', 'Conflict Resolution',
            'Video Games', 'Math', 'Human Behavior', 'Literature', 'Crafts', 'Technology',
            'Movies', 'Fitness', 'Forensics', 'Central America', 'Language', 'Science',
            'Marketing', 'Asia', 'Fashion', 'Business', 'Music', 'Philosophy', 'History',
            'Internet', 'Children', 'Travel', 'Media', 'Photography', 'Design',
            'Environment', 'Food', 'Security', 'Religion', 'Sports', 'Healthcare',
            'Data Analysis', 'Helping People', 'Performance', 'North America', 'Animals',
            'Management', 'Programming', 'Art', 'Writing', 'Leadership', 'Culture',
            'Counseling', 'Rehabilitation', 'News', 'Human Rights', 'Communication',
            'Public Relations', 'Europe', 'International', 'Government', 'Gender and LGBTQ+',
            'Africa', 'Social Issues', 'Psychology', 'Engineering', 'Research',
          `});
           */
          /**
        const result = await model.generateContent([input]);
         */

        return text;
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
              IU Scheduling Assistant
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
              >
                {message.text}
              </div>
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
          className="bg-[#990000] hover:bg-[#660000] text-white px-4 py-2 rounded-lg transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  );
}
