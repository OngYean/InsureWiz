"use client"

import { useState } from "react"
import Link from "next/link"
import { Shield, Car, MessageSquare, BarChart3, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"

const navItems = [
  { name: "Validator", href: "/validator", icon: Car },
  { name: "Advisor", href: "/advisor", icon: MessageSquare },
  { name: "Compare", href: "/compare", icon: BarChart3 },
  { name: "Claims", href: "/claims", icon: AlertTriangle },
]

export function Navigation() {
  const [activeItem, setActiveItem] = useState("Validator")

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center space-x-2">
          <Shield className="h-8 w-8 text-primary" />
          <span className="text-xl font-bold text-foreground">InsureWiz</span>
        </div>

        <div className="flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <Button
                key={item.name}
                variant={activeItem === item.name ? "default" : "ghost"}
                size="sm"
                className="flex items-center space-x-2 rounded-lg transition-all duration-200"
                onClick={() => setActiveItem(item.name)}
                asChild
              >
                <Link href={item.href}>
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              </Button>
            )
          })}
          <div className="ml-2 pl-2 border-l border-border">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  )
}
