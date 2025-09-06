import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Car, MessageSquare, BarChart3, AlertTriangle, Shield, Zap, Users, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Shield className="h-12 w-12 text-primary mr-3" />
            <h1 className="text-4xl font-bold text-foreground">InsureWiz</h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Your intelligent insurance companion. Validate vehicles, get AI-powered advice, compare policies, and detect
            fraud - all in one modern platform.
          </p>
        </div>

        {/* Main Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Link href="/validator">
            <Card className="group hover:shadow-lg transition-all duration-300 cursor-pointer border-border h-full">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">
                  <Car className="h-8 w-8 text-primary" />
                </div>
                <CardTitle className="text-lg">Vehicle Validator</CardTitle>
                <CardDescription>
                  Real-time validation and auto-correction for vehicle data with confidence scoring
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Start Validation
                </Button>
              </CardContent>
            </Card>
          </Link>

          <Link href="/advisor">
            <Card className="group hover:shadow-lg transition-all duration-300 cursor-pointer border-border h-full">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4 p-3 bg-secondary/10 rounded-full w-fit">
                  <MessageSquare className="h-8 w-8 text-secondary" />
                </div>
                <CardTitle className="text-lg">AI Advisor</CardTitle>
                <CardDescription>
                  Get personalized insurance advice in plain English with multilingual support
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Ask Questions
                </Button>
              </CardContent>
            </Card>
          </Link>

          <Link href="/compare">
            <Card className="group hover:shadow-lg transition-all duration-300 cursor-pointer border-border h-full">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4 p-3 bg-chart-1/10 rounded-full w-fit">
                  <BarChart3 className="h-8 w-8 text-chart-1" />
                </div>
                <CardTitle className="text-lg">Smart Compare</CardTitle>
                <CardDescription>
                  Side-by-side policy comparison with intelligent filtering and recommendations
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Compare Policies
                </Button>
              </CardContent>
            </Card>
          </Link>

          <Link href="/claims">
            <Card className="group hover:shadow-lg transition-all duration-300 cursor-pointer border-border h-full">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4 p-3 bg-destructive/10 rounded-full w-fit">
                  <AlertTriangle className="h-8 w-8 text-destructive" />
                </div>
                <CardTitle className="text-lg">Fraud Checker</CardTitle>
                <CardDescription>Advanced claim analysis to detect suspicious patterns and prevent fraud</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Check Claims
                </Button>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="text-center p-6 bg-card rounded-lg border">
            <div className="flex items-center justify-center mb-2">
              <Users className="h-8 w-8 text-primary mr-2" />
              <span className="text-3xl font-bold text-foreground">50K+</span>
            </div>
            <p className="text-muted-foreground">Active Users</p>
          </div>

          <div className="text-center p-6 bg-card rounded-lg border">
            <div className="flex items-center justify-center mb-2">
              <Zap className="h-8 w-8 text-secondary mr-2" />
              <span className="text-3xl font-bold text-foreground">99.9%</span>
            </div>
            <p className="text-muted-foreground">Accuracy Rate</p>
          </div>

          <div className="text-center p-6 bg-card rounded-lg border">
            <div className="flex items-center justify-center mb-2">
              <TrendingUp className="h-8 w-8 text-chart-1 mr-2" />
              <span className="text-3xl font-bold text-foreground">$2M+</span>
            </div>
            <p className="text-muted-foreground">Fraud Prevented</p>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-gradient-to-r from-primary/5 to-secondary/5 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-foreground mb-4">Ready to revolutionize your insurance experience?</h2>
          <p className="text-muted-foreground mb-6 max-w-xl mx-auto">
            Join thousands of users who trust InsureWiz for smarter, faster, and more reliable insurance solutions.
          </p>
          <Link href="/validator">
            <Button size="lg" className="mr-4">
              Get Started
            </Button>
          </Link>
          <Link href="/advisor">
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </Link>
        </div>
      </main>
    </div>
  )
}
