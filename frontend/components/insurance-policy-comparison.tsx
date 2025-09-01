"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Check, X, Star, Shield, DollarSign, Users, MapPin, Calendar } from "lucide-react"

interface PolicyFeature {
  name: string
  included: boolean
  details?: string
}

interface InsurancePolicy {
  id: string
  name: string
  provider: string
  monthlyPrice: number
  yearlyPrice: number
  rating: number
  bestFor: string[]
  coverage: {
    liability: string
    collision: string
    comprehensive: string
    uninsured: string
  }
  features: PolicyFeature[]
  popular?: boolean
  recommended?: boolean
}

const samplePolicies: InsurancePolicy[] = [
  {
    id: "1",
    name: "Basic Shield",
    provider: "InsureWiz",
    monthlyPrice: 89,
    yearlyPrice: 1068,
    rating: 4.2,
    bestFor: ["Budget-conscious", "Older vehicles", "Minimal coverage"],
    coverage: {
      liability: "50/100/25",
      collision: "$1,000 deductible",
      comprehensive: "$1,000 deductible",
      uninsured: "50/100",
    },
    features: [
      { name: "24/7 Claims Support", included: true },
      { name: "Roadside Assistance", included: false },
      { name: "Rental Car Coverage", included: false },
      { name: "Gap Coverage", included: false },
      { name: "New Car Replacement", included: false },
    ],
  },
  {
    id: "2",
    name: "SafeGuard Plus",
    provider: "InsureWiz",
    monthlyPrice: 124,
    yearlyPrice: 1488,
    rating: 4.6,
    bestFor: ["Most drivers", "Good value", "Balanced coverage"],
    coverage: {
      liability: "100/300/100",
      collision: "$500 deductible",
      comprehensive: "$500 deductible",
      uninsured: "100/300",
    },
    features: [
      { name: "24/7 Claims Support", included: true },
      { name: "Roadside Assistance", included: true },
      { name: "Rental Car Coverage", included: true, details: "Up to $30/day" },
      { name: "Gap Coverage", included: false },
      { name: "New Car Replacement", included: false },
    ],
    popular: true,
  },
  {
    id: "3",
    name: "Premium Shield",
    provider: "InsureWiz",
    monthlyPrice: 167,
    yearlyPrice: 2004,
    rating: 4.8,
    bestFor: ["New vehicles", "Maximum protection", "Peace of mind"],
    coverage: {
      liability: "250/500/250",
      collision: "$250 deductible",
      comprehensive: "$250 deductible",
      uninsured: "250/500",
    },
    features: [
      { name: "24/7 Claims Support", included: true },
      { name: "Roadside Assistance", included: true },
      { name: "Rental Car Coverage", included: true, details: "Up to $50/day" },
      { name: "Gap Coverage", included: true },
      { name: "New Car Replacement", included: true },
    ],
    recommended: true,
  },
]

export function InsurancePolicyComparison() {
  const [policies] = useState<InsurancePolicy[]>(samplePolicies)
  const [filteredPolicies, setFilteredPolicies] = useState<InsurancePolicy[]>(samplePolicies)
  const [filters, setFilters] = useState({
    age: "",
    carValue: "",
    location: "",
    maxPrice: "",
  })

  const applyFilters = () => {
    let filtered = [...policies]

    if (filters.maxPrice) {
      const maxPrice = Number.parseInt(filters.maxPrice)
      filtered = filtered.filter((policy) => policy.monthlyPrice <= maxPrice)
    }

    // Simulate age-based filtering
    if (filters.age) {
      if (filters.age === "under-25") {
        // Young drivers might prefer basic coverage
        filtered = filtered.sort((a, b) => a.monthlyPrice - b.monthlyPrice)
      } else if (filters.age === "over-50") {
        // Older drivers might prefer comprehensive coverage
        filtered = filtered.sort((a, b) => b.rating - a.rating)
      }
    }

    setFilteredPolicies(filtered)
  }

  const resetFilters = () => {
    setFilters({ age: "", carValue: "", location: "", maxPrice: "" })
    setFilteredPolicies(policies)
  }

  return (
    <div className="space-y-6">
      {/* Filters Section */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle className="flex items-center text-lg">
            <Shield className="h-5 w-5 text-primary mr-2" />
            Filter Policies
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label htmlFor="age" className="flex items-center text-sm">
                <Calendar className="h-4 w-4 mr-1" />
                Age Group
              </Label>
              <Select value={filters.age} onValueChange={(value) => setFilters({ ...filters, age: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select age" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="under-25">Under 25</SelectItem>
                  <SelectItem value="25-50">25-50</SelectItem>
                  <SelectItem value="over-50">Over 50</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="carValue" className="flex items-center text-sm">
                <DollarSign className="h-4 w-4 mr-1" />
                Car Value
              </Label>
              <Select value={filters.carValue} onValueChange={(value) => setFilters({ ...filters, carValue: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select value" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="under-10k">Under $10k</SelectItem>
                  <SelectItem value="10k-30k">$10k - $30k</SelectItem>
                  <SelectItem value="over-30k">Over $30k</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="location" className="flex items-center text-sm">
                <MapPin className="h-4 w-4 mr-1" />
                Location
              </Label>
              <Select value={filters.location} onValueChange={(value) => setFilters({ ...filters, location: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select location" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="urban">Urban</SelectItem>
                  <SelectItem value="suburban">Suburban</SelectItem>
                  <SelectItem value="rural">Rural</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="maxPrice" className="text-sm">
                Max Monthly Price
              </Label>
              <Input
                id="maxPrice"
                type="number"
                placeholder="$150"
                value={filters.maxPrice}
                onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value })}
              />
            </div>
          </div>

          <div className="flex justify-end space-x-2 mt-4">
            <Button variant="outline" onClick={resetFilters}>
              Reset
            </Button>
            <Button onClick={applyFilters}>Apply Filters</Button>
          </div>
        </CardContent>
      </Card>

      {/* Comparison Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {filteredPolicies.map((policy) => (
          <Card
            key={policy.id}
            className={`relative border-border hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 ${
              policy.recommended ? "ring-2 ring-primary" : ""
            }`}
          >
            {policy.popular && (
              <Badge className="absolute -top-2 left-4 bg-secondary text-secondary-foreground">Most Popular</Badge>
            )}
            {policy.recommended && (
              <Badge className="absolute -top-2 right-4 bg-primary text-primary-foreground">Recommended</Badge>
            )}

            <CardHeader className="text-center pb-4">
              <CardTitle className="text-xl">{policy.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{policy.provider}</p>
              <div className="flex items-center justify-center space-x-1 mt-2">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`h-4 w-4 ${
                      i < Math.floor(policy.rating) ? "text-yellow-400 fill-current" : "text-gray-300"
                    }`}
                  />
                ))}
                <span className="text-sm text-muted-foreground ml-1">({policy.rating})</span>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              {/* Pricing */}
              <div className="text-center p-4 bg-muted/50 rounded-lg">
                <div className="text-3xl font-bold text-foreground">${policy.monthlyPrice}</div>
                <div className="text-sm text-muted-foreground">per month</div>
                <div className="text-xs text-muted-foreground">${policy.yearlyPrice}/year</div>
              </div>

              {/* Best For */}
              <div>
                <h4 className="font-medium text-sm mb-2 flex items-center">
                  <Users className="h-4 w-4 mr-1" />
                  Best For
                </h4>
                <div className="flex flex-wrap gap-1">
                  {policy.bestFor.map((item, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {item}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Coverage */}
              <div>
                <h4 className="font-medium text-sm mb-2">Coverage Limits</h4>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Liability:</span>
                    <span>{policy.coverage.liability}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Collision:</span>
                    <span>{policy.coverage.collision}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Comprehensive:</span>
                    <span>{policy.coverage.comprehensive}</span>
                  </div>
                </div>
              </div>

              {/* Features */}
              <div>
                <h4 className="font-medium text-sm mb-2">Features</h4>
                <div className="space-y-2">
                  {policy.features.map((feature, index) => (
                    <div key={index} className="flex items-center justify-between text-xs">
                      <span className="flex items-center">
                        {feature.included ? (
                          <Check className="h-3 w-3 text-green-500 mr-1" />
                        ) : (
                          <X className="h-3 w-3 text-red-500 mr-1" />
                        )}
                        {feature.name}
                      </span>
                      {feature.details && <span className="text-muted-foreground">{feature.details}</span>}
                    </div>
                  ))}
                </div>
              </div>

              <Button className="w-full mt-4" variant={policy.recommended ? "default" : "outline"}>
                Get Quote
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredPolicies.length === 0 && (
        <Card className="border-border">
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No policies match your current filters. Try adjusting your criteria.
            </p>
            <Button variant="outline" onClick={resetFilters} className="mt-4 bg-transparent">
              Reset Filters
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
