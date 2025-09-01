"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Send, Mic, Bot, User, Sparkles } from "lucide-react"

interface Message {
  id: string
  content: string
  sender: "user" | "ai"
  timestamp: Date
  typing?: boolean
}

const sampleResponses: Record<string, string> = {
  comprehensive:
    "Comprehensive coverage protects your vehicle against damage from non-collision events like theft, vandalism, weather damage, or hitting an animal. It's different from collision coverage, which only covers damage from crashes. Think of comprehensive as protection from 'acts of nature' and other unexpected events.",

  collision:
    "Collision coverage pays for damage to your car when you hit another vehicle or object, or when another vehicle hits you. This includes accidents like rear-ending someone, hitting a tree, or rolling your car. It works regardless of who's at fault in the accident.",

  "how much":
    "The amount of car insurance you need depends on several factors: your state's minimum requirements, your car's value, your assets to protect, and your risk tolerance. Most experts recommend at least 100/300/100 coverage (100k bodily injury per person, 300k per accident, 100k property damage) plus comprehensive and collision if your car is worth more than $3,000.",

  premium:
    "Several factors affect your insurance premium: your driving record, age, location, type of car, credit score (in most states), coverage amounts, and deductibles. Young drivers and those with accidents or violations typically pay more. Living in areas with high crime or accident rates also increases costs.",

  claim:
    "To file a claim: 1) Contact your insurance company immediately (most have 24/7 claim hotlines), 2) Provide your policy number and details about the incident, 3) Take photos if safe to do so, 4) Get a police report if required, 5) Keep records of all communications. Your insurer will assign an adjuster to evaluate the damage and guide you through the process.",

  deductible:
    "A deductible is the amount you pay out-of-pocket before your insurance coverage kicks in. For example, with a $500 deductible, you pay the first $500 of repair costs, and insurance covers the rest. Higher deductibles mean lower premiums, but more out-of-pocket costs when you file a claim.",
}

export function InsuranceAdvisorChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your AI Insurance Advisor. I'm here to help you understand insurance coverage, policies, and claims in simple terms. What would you like to know?",
      sender: "ai",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const generateResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase()

    // Check for keywords in the message
    for (const [keyword, response] of Object.entries(sampleResponses)) {
      if (lowerMessage.includes(keyword)) {
        return response
      }
    }

    // Default responses for common patterns
    if (lowerMessage.includes("hello") || lowerMessage.includes("hi")) {
      return "Hello! I'm here to help you with any insurance questions you have. Feel free to ask about coverage types, claims, premiums, or anything else insurance-related."
    }

    if (lowerMessage.includes("thank")) {
      return "You're welcome! I'm always here to help with your insurance questions. Is there anything else you'd like to know?"
    }

    if (lowerMessage.includes("best") && lowerMessage.includes("insurance")) {
      return "The 'best' insurance depends on your specific needs, budget, and circumstances. I'd recommend comparing coverage options, deductibles, and customer service ratings. Would you like me to explain what to look for when comparing policies?"
    }

    // Generic helpful response
    return "That's a great question! While I don't have specific information about that topic in my current knowledge base, I'd recommend contacting your insurance agent or company directly for detailed guidance. Is there anything else about general insurance concepts I can help explain?"
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsTyping(true)

    // Simulate AI thinking time
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: generateResponse(inputValue),
        sender: "ai",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, aiResponse])
      setIsTyping(false)
    }, 1500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <Card className="h-[600px] flex flex-col border-border">
      <CardHeader className="border-b">
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center">
            <Bot className="h-6 w-6 text-primary mr-2" />
            AI Insurance Advisor
          </div>
          <Badge variant="outline" className="text-green-600 border-green-600">
            <div className="w-2 h-2 bg-green-600 rounded-full mr-1 animate-pulse" />
            Online
          </Badge>
        </CardTitle>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col p-0">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start space-x-3 ${
                message.sender === "user" ? "flex-row-reverse space-x-reverse" : ""
              }`}
            >
              <Avatar className="w-8 h-8">
                <AvatarFallback
                  className={
                    message.sender === "ai"
                      ? "bg-primary text-primary-foreground"
                      : "bg-secondary text-secondary-foreground"
                  }
                >
                  {message.sender === "ai" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                </AvatarFallback>
              </Avatar>

              <div className={`flex flex-col max-w-[80%] ${message.sender === "user" ? "items-end" : "items-start"}`}>
                <div
                  className={`rounded-lg px-4 py-2 ${
                    message.sender === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                </div>
                <span className="text-xs text-muted-foreground mt-1">{formatTime(message.timestamp)}</span>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-start space-x-3">
              <Avatar className="w-8 h-8">
                <AvatarFallback className="bg-primary text-primary-foreground">
                  <Bot className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
              <div className="bg-muted rounded-lg px-4 py-2">
                <div className="flex items-center space-x-1">
                  <Sparkles className="h-4 w-4 text-primary animate-pulse" />
                  <span className="text-sm text-muted-foreground">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t p-4">
          <div className="flex items-center space-x-2">
            <div className="flex-1 relative">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything about insurance..."
                className="pr-12"
                disabled={isTyping}
              />
              <Button
                size="sm"
                variant="ghost"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 p-0"
                disabled={isTyping}
              >
                <Mic className="h-4 w-4 text-muted-foreground" />
              </Button>
            </div>
            <Button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              size="sm"
              className="h-10 w-10 p-0"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-2 text-center">
            AI responses are for informational purposes only. Consult with licensed agents for specific advice.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
