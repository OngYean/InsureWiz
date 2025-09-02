"use client"

import type React from "react"

import { useState, useRef, useEffect, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Send, Mic, Bot, User, Sparkles, AlertCircle, Loader2, ChevronDown, Maximize2, Minimize2, Download, History, RefreshCw } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  content: string
  sender: "user" | "ai"
  timestamp: Date
  typing?: boolean
}

interface ChatResponse {
  response: string
}

// Function to convert markdown to readable text
const formatMessageContent = (content: string): string => {
  return content
    // Remove markdown bold syntax and replace with clean text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    // Remove markdown italic syntax
    .replace(/\*(.*?)\*/g, '$1')
    // Remove markdown code blocks
    .replace(/```([\s\S]*?)```/g, '$1')
    // Remove markdown inline code
    .replace(/`(.*?)`/g, '$1')
    // Remove markdown links but keep the text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    // Remove markdown headers
    .replace(/^#{1,6}\s+/gm, '')
    // Remove markdown list markers
    .replace(/^[\s]*[-*+]\s+/gm, '• ')
    // Remove markdown numbered list markers
    .replace(/^[\s]*\d+\.\s+/gm, '• ')
    // Clean up extra whitespace
    .replace(/\n\s*\n/g, '\n\n')
    .trim()
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
  const [isConnected, setIsConnected] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)
  const [showScrollButton, setShowScrollButton] = useState(false)
  const [showQuickActions, setShowQuickActions] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const messagesContainerRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  const scrollToBottom = useCallback((behavior: ScrollBehavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior })
  }, [])

  const handleScroll = useCallback(() => {
    if (messagesContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100
      setShowScrollButton(!isNearBottom)
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, scrollToBottom])

  useEffect(() => {
    const container = messagesContainerRef.current
    if (container) {
      container.addEventListener('scroll', handleScroll)
      return () => container.removeEventListener('scroll', handleScroll)
    }
  }, [handleScroll])

  // Check backend connection on component mount
  useEffect(() => {
    checkBackendConnection()
  }, [])

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      if (response.ok) {
        setIsConnected(true)
        toast({
          title: "Connected to AI Backend",
          description: "AI Insurance Advisor is ready to help!",
        })
      }
    } catch (error) {
      setIsConnected(false)
      toast({
        title: "Backend Connection Failed",
        description: "Please ensure the backend server is running on port 8000",
        variant: "destructive",
      })
    }
  }

  const sendMessageToAI = async (message: string): Promise<string> => {
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data: ChatResponse = await response.json()
      return data.response
    } catch (error) {
      console.error('Error sending message to AI:', error)
      throw new Error('Failed to get response from AI. Please check your backend connection.')
    }
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !isConnected) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsTyping(true)

    try {
      const aiResponse = await sendMessageToAI(inputValue)
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        sender: "ai",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, aiMessage])
    } catch (error) {
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error instanceof Error ? error.message : 'An error occurred while getting AI response.',
        sender: "ai",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
      
      toast({
        title: "AI Response Error",
        description: error instanceof Error ? error.message : 'Failed to get AI response',
        variant: "destructive",
      })
    } finally {
      setIsTyping(false)
    }
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

  const retryConnection = () => {
    checkBackendConnection()
  }

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  const clearChat = () => {
    setMessages([{
      id: "1",
      content:
        "Hello! I'm your AI Insurance Advisor. I'm here to help you understand insurance coverage, policies, and claims in simple terms. What would you like to know?",
      sender: "ai",
      timestamp: new Date(),
    }])
    toast({
      title: "Chat Cleared",
      description: "Starting fresh conversation",
    })
  }

  const downloadChat = () => {
    const chatContent = messages.map(msg => 
      `${msg.sender === 'ai' ? 'AI' : 'You'} (${formatTime(msg.timestamp)}): ${msg.content}`
    ).join('\n\n')
    
    const blob = new Blob([chatContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `insurance-chat-${new Date().toISOString().split('T')[0]}.txt`
    a.click()
    URL.revokeObjectURL(url)
    
    toast({
      title: "Chat Downloaded",
      description: "Your conversation has been saved",
    })
  }

  return (
    <Card className={cn(
      "flex flex-col border-border shadow-lg transition-all duration-300 ease-in-out relative overflow-hidden",
      isExpanded ? "h-[80vh]" : "h-[600px]",
      "hover:shadow-xl card-hover"
    )}>
      <CardHeader className="border-b bg-gradient-to-r from-primary/5 to-secondary/5 flex-shrink-0">
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center shadow-lg animate-pulse-glow">
                <Bot className="h-5 w-5 text-white" />
              </div>
              <div className={cn(
                "absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-background transition-all duration-300",
                isConnected ? "bg-green-500 animate-pulse" : "bg-red-500"
              )} />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">AI Insurance Advisor</h3>
              <p className="text-xs text-muted-foreground">Powered by advanced AI</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Badge 
              variant={isConnected ? "outline" : "destructive"} 
              className={cn(
                "transition-all duration-200",
                isConnected 
                  ? "text-green-600 border-green-600 bg-green-50 dark:bg-green-950/20" 
                  : "text-red-600 border-red-600 bg-red-50 dark:bg-red-950/20"
              )}
            >
              <div className={cn(
                "w-2 h-2 rounded-full mr-2 transition-all duration-200",
                isConnected ? "bg-green-600 animate-pulse" : "bg-red-600"
              )} />
              {isConnected ? "Online" : "Offline"}
            </Badge>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleExpand}
              className="h-8 w-8 p-0 hover:bg-muted/50 btn-hover"
            >
              {isExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
            </Button>
          </div>
        </CardTitle>
        
        {!isConnected && (
          <div className="flex items-center space-x-2 text-sm text-amber-600 bg-amber-50 dark:bg-amber-950/20 p-3 rounded-lg border border-amber-200 dark:border-amber-800 animate-fade-in-up">
            <AlertCircle className="h-4 w-4 flex-shrink-0" />
            <span className="flex-1">Backend not connected. Please ensure the server is running.</span>
            <Button size="sm" variant="outline" onClick={retryConnection} className="text-amber-700 border-amber-300 hover:bg-amber-100 dark:hover:bg-amber-900/20 btn-hover">
              <RefreshCw className="h-4 w-4 mr-1" />
              Retry
            </Button>
          </div>
        )}
      </CardHeader>

      <CardContent className="flex-1 flex flex-col p-0 min-h-0">
        {/* Messages Area - Now properly scrollable */}
        <div 
          ref={messagesContainerRef}
          className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-muted scrollbar-track-transparent min-h-0"
          style={{ maxHeight: 'calc(100% - 200px)' }}
        >
          {messages.map((message, index) => (
            <div
              key={message.id}
              className={cn(
                "flex items-start space-x-3 animate-in fade-in-0 slide-in-from-bottom-2 duration-300",
                message.sender === "user" ? "flex-row-reverse space-x-reverse" : "",
                index === messages.length - 1 ? "animate-in fade-in-0 slide-in-from-bottom-4 duration-500" : ""
              )}
            >
              <Avatar className={cn(
                "w-9 h-9 transition-all duration-200 hover:scale-110 ring-2 flex-shrink-0",
                message.sender === "ai" ? "ring-primary/20" : "ring-secondary/20"
              )}>
                <AvatarFallback
                  className={cn(
                    "text-sm font-medium transition-all duration-200",
                    message.sender === "ai"
                      ? "bg-gradient-to-br from-primary to-primary/80 text-primary-foreground"
                      : "bg-gradient-to-br from-secondary to-secondary/80 text-secondary-foreground"
                  )}
                >
                  {message.sender === "ai" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                </AvatarFallback>
              </Avatar>

              <div className={cn(
                "flex flex-col max-w-[85%] transition-all duration-200",
                message.sender === "user" ? "items-end" : "items-start"
              )}>
                <div
                  className={cn(
                    "rounded-2xl px-4 py-3 shadow-sm transition-all duration-200 hover:shadow-md message-bubble break-words",
                    message.sender === "user" 
                      ? "bg-gradient-to-br from-primary to-primary/90 text-primary-foreground" 
                      : "bg-gradient-to-br from-muted to-muted/80 text-muted-foreground border border-border/50"
                  )}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap overflow-hidden">
                    {message.sender === "ai" ? formatMessageContent(message.content) : message.content}
                  </p>
                </div>
                <span className="text-xs text-muted-foreground mt-2 opacity-70">
                  {formatTime(message.timestamp)}
                </span>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-start space-x-3 animate-in fade-in-0 slide-in-from-bottom-2 duration-300">
              <Avatar className="w-9 h-9 ring-2 ring-primary/20 flex-shrink-0">
                <AvatarFallback className="bg-gradient-to-br from-primary to-primary/80 text-primary-foreground">
                  <Bot className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
              <div className="bg-gradient-to-br from-muted to-muted/80 rounded-2xl px-4 py-3 border border-border/50">
                <div className="flex items-center space-x-2">
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="text-sm text-muted-foreground">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions Bar */}
        <div className="border-t border-border/50 bg-muted/30 px-4 py-2 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowQuickActions(!showQuickActions)}
                className="h-8 px-3 text-xs hover:bg-muted/50 btn-hover"
              >
                <History className="h-3 w-3 mr-1" />
                Actions
              </Button>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={clearChat}
                className="h-8 px-3 text-xs hover:bg-muted/50 btn-hover"
              >
                <RefreshCw className="h-3 w-3 mr-1" />
                Clear
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={downloadChat}
                className="h-8 px-3 text-xs hover:bg-muted/50 btn-hover"
              >
                <Download className="h-3 w-3 mr-1" />
                Save
              </Button>
            </div>
          </div>
        </div>

        {/* Scroll to bottom button */}
        {showScrollButton && (
          <div className="absolute bottom-28 right-6 z-10">
            <Button
              size="sm"
              variant="secondary"
              onClick={() => scrollToBottom()}
              className="h-10 w-10 p-0 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110 btn-hover"
            >
              <ChevronDown className="h-4 w-4" />
            </Button>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t bg-gradient-to-r from-muted/30 to-muted/50 p-4 flex-shrink-0">
          <div className="flex items-center space-x-3">
            <div className="flex-1 relative group">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={isConnected ? "Ask me anything about insurance..." : "Backend not connected..."}
                className={cn(
                  "pr-20 transition-all duration-200 border-border/50 focus:border-primary/50 focus:ring-primary/20 input-focus",
                  "placeholder:text-muted-foreground/60",
                  isConnected ? "bg-background" : "bg-muted/50"
                )}
                disabled={isTyping || !isConnected}
              />
              
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center space-x-1">
                <Button
                  size="sm"
                  variant="ghost"
                  className="h-8 w-8 p-0 opacity-60 hover:opacity-100 transition-all duration-200 hover:bg-muted/50 btn-hover"
                  disabled={isTyping || !isConnected}
                >
                  <Mic className="h-4 w-4 text-muted-foreground" />
                </Button>
              </div>
            </div>
            
            <Button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping || !isConnected}
              size="default"
              className={cn(
                "h-11 px-6 transition-all duration-200 font-medium btn-hover",
                "bg-gradient-to-r from-primary to-primary/90 hover:from-primary/90 hover:to-primary",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                "hover:shadow-lg hover:scale-105 active:scale-95"
              )}
            >
              {isTyping ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              <span className="ml-2 hidden sm:inline">Send</span>
            </Button>
          </div>
          
          <div className="mt-3 text-center">
            <p className="text-xs text-muted-foreground/70">
              {isConnected 
                ? "💡 AI responses are for informational purposes only. Consult with licensed agents for specific advice."
                : "⚠️ Please start the backend server to use the AI advisor."
              }
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
