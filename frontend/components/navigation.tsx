"use client"

import { usePathname } from "next/navigation"
import Link from "next/link"
import { Shield, Car, MessageSquare, BarChart3, AlertTriangle, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"

const navItems = [
  { name: "Home", href: "/", icon: Home },
  { name: "Validator", href: "/validator", icon: Car },
  { name: "Advisor", href: "/advisor", icon: MessageSquare },
  { name: "Compare", href: "/compare", icon: BarChart3 },
  { name: "Claims", href: "/claims", icon: AlertTriangle },
]

export function Navigation() {
  const pathname = usePathname()
  
  const getActiveItem = () => {
    const currentItem = navItems.find(item => item.href === pathname)
    return currentItem ? currentItem.name : "Home"
  }

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
          <Shield className="h-8 w-8 text-primary" />
          <span className="text-xl font-bold text-foreground">InsureWiz</span>
        </Link>

        <div className="flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = getActiveItem() === item.name
            return (
              <Button
                key={item.name}
                variant={isActive ? "default" : "ghost"}
                size="sm"
                className="flex items-center space-x-2 rounded-lg transition-all duration-200"
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
