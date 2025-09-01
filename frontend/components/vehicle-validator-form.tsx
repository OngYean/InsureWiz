"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { CheckCircle, AlertTriangle, Lightbulb, Car, Calendar, Tag, Hash } from "lucide-react"

interface ValidationResult {
  field: string
  isValid: boolean
  confidence: number
  suggestion?: string
  explanation: string
}

interface VehicleData {
  licensePlate: string
  brand: string
  model: string
  year: string
}

const carBrands = [
  "Toyota",
  "Honda",
  "Ford",
  "Chevrolet",
  "Nissan",
  "BMW",
  "Mercedes-Benz",
  "Audi",
  "Volkswagen",
  "Hyundai",
  "Kia",
  "Mazda",
  "Subaru",
  "Lexus",
  "Acura",
]

const carModels: Record<string, string[]> = {
  Toyota: ["Camry", "Corolla", "RAV4", "Highlander", "Prius", "Tacoma"],
  Honda: ["Civic", "Accord", "CR-V", "Pilot", "Fit", "Ridgeline"],
  Ford: ["F-150", "Escape", "Explorer", "Mustang", "Focus", "Edge"],
  BMW: ["3 Series", "5 Series", "X3", "X5", "i3", "Z4"],
  "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "A-Class", "S-Class"],
}

export function VehicleValidatorForm() {
  const [formData, setFormData] = useState<VehicleData>({
    licensePlate: "",
    brand: "",
    model: "",
    year: "",
  })

  const [validationResults, setValidationResults] = useState<ValidationResult[]>([])
  const [isValidating, setIsValidating] = useState(false)

  const validateField = (field: string, value: string): ValidationResult => {
    switch (field) {
      case "licensePlate":
        const plateRegex = /^[A-Z0-9]{2,8}$/i
        const isValidPlate = plateRegex.test(value.replace(/\s+/g, ""))
        return {
          field,
          isValid: isValidPlate,
          confidence: isValidPlate ? 95 : 60,
          suggestion: isValidPlate ? undefined : value.toUpperCase().replace(/\s+/g, ""),
          explanation: isValidPlate
            ? "License plate format is valid"
            : "License plates should be 2-8 alphanumeric characters",
        }

      case "brand":
        const normalizedBrand = value.toLowerCase()
        const exactMatch = carBrands.find((brand) => brand.toLowerCase() === normalizedBrand)
        const similarMatch = carBrands.find(
          (brand) => brand.toLowerCase().includes(normalizedBrand) || normalizedBrand.includes(brand.toLowerCase()),
        )

        if (exactMatch) {
          return {
            field,
            isValid: true,
            confidence: 98,
            explanation: "Brand recognized and verified",
          }
        } else if (similarMatch) {
          return {
            field,
            isValid: false,
            confidence: 85,
            suggestion: similarMatch,
            explanation: `Did you mean "${similarMatch}"?`,
          }
        } else {
          return {
            field,
            isValid: false,
            confidence: 30,
            explanation: "Brand not recognized in our database",
          }
        }

      case "model":
        if (!formData.brand) {
          return {
            field,
            isValid: false,
            confidence: 0,
            explanation: "Please select a brand first",
          }
        }

        const brandModels = carModels[formData.brand] || []
        const modelMatch = brandModels.find((model) => model.toLowerCase() === value.toLowerCase())
        const similarModelMatch = brandModels.find(
          (model) =>
            model.toLowerCase().includes(value.toLowerCase()) || value.toLowerCase().includes(model.toLowerCase()),
        )

        if (modelMatch) {
          return {
            field,
            isValid: true,
            confidence: 95,
            explanation: "Model verified for this brand",
          }
        } else if (similarModelMatch) {
          return {
            field,
            isValid: false,
            confidence: 80,
            suggestion: similarModelMatch,
            explanation: `Did you mean "${similarModelMatch}"?`,
          }
        } else {
          return {
            field,
            isValid: value.length > 0,
            confidence: 60,
            explanation: "Model not in our database but may be valid",
          }
        }

      case "year":
        const currentYear = new Date().getFullYear()
        const yearNum = Number.parseInt(value)
        const isValidYear = yearNum >= 1900 && yearNum <= currentYear + 1

        return {
          field,
          isValid: isValidYear,
          confidence: isValidYear ? 99 : 20,
          suggestion: isValidYear ? undefined : currentYear.toString(),
          explanation: isValidYear
            ? "Year is within valid range"
            : `Year should be between 1900 and ${currentYear + 1}`,
        }

      default:
        return {
          field,
          isValid: true,
          confidence: 0,
          explanation: "No validation available",
        }
    }
  }

  const handleInputChange = (field: keyof VehicleData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))

    // Simulate validation delay
    setIsValidating(true)
    setTimeout(() => {
      const result = validateField(field, value)
      setValidationResults((prev) => {
        const filtered = prev.filter((r) => r.field !== field)
        return value ? [...filtered, result] : filtered
      })
      setIsValidating(false)
    }, 300)
  }

  const applySuggestion = (field: string, suggestion: string) => {
    setFormData((prev) => ({ ...prev, [field]: suggestion }))
    handleInputChange(field as keyof VehicleData, suggestion)
  }

  const getFieldIcon = (field: string) => {
    switch (field) {
      case "licensePlate":
        return <Hash className="h-4 w-4" />
      case "brand":
        return <Tag className="h-4 w-4" />
      case "model":
        return <Car className="h-4 w-4" />
      case "year":
        return <Calendar className="h-4 w-4" />
      default:
        return null
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return "text-green-600"
    if (confidence >= 70) return "text-amber-600"
    return "text-red-600"
  }

  return (
    <Card className="border-border">
      <CardHeader>
        <CardTitle className="flex items-center text-xl">
          <Car className="h-6 w-6 text-primary mr-2" />
          Vehicle Information
        </CardTitle>
        <CardDescription>
          Enter your vehicle details below. We'll validate and suggest corrections in real-time.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="licensePlate" className="flex items-center">
              <Hash className="h-4 w-4 mr-1" />
              License Plate
            </Label>
            <Input
              id="licensePlate"
              placeholder="ABC123"
              value={formData.licensePlate}
              onChange={(e) => handleInputChange("licensePlate", e.target.value)}
              className="transition-all duration-200"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="year" className="flex items-center">
              <Calendar className="h-4 w-4 mr-1" />
              Year
            </Label>
            <Input
              id="year"
              type="number"
              placeholder="2023"
              value={formData.year}
              onChange={(e) => handleInputChange("year", e.target.value)}
              className="transition-all duration-200"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="brand" className="flex items-center">
              <Tag className="h-4 w-4 mr-1" />
              Brand
            </Label>
            <Input
              id="brand"
              placeholder="Toyota"
              value={formData.brand}
              onChange={(e) => handleInputChange("brand", e.target.value)}
              className="transition-all duration-200"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="model" className="flex items-center">
              <Car className="h-4 w-4 mr-1" />
              Model
            </Label>
            <Input
              id="model"
              placeholder="Camry"
              value={formData.model}
              onChange={(e) => handleInputChange("model", e.target.value)}
              className="transition-all duration-200"
            />
          </div>
        </div>

        {/* Validation Results */}
        {validationResults.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Validation Results</h3>
            <div className="space-y-3">
              {validationResults.map((result) => (
                <Alert
                  key={result.field}
                  className={`border-l-4 ${result.isValid ? "border-l-green-500" : "border-l-amber-500"}`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-2">
                      {result.isValid ? (
                        <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
                      ) : (
                        <AlertTriangle className="h-5 w-5 text-amber-500 mt-0.5" />
                      )}
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          {getFieldIcon(result.field)}
                          <span className="font-medium capitalize">{result.field}</span>
                          <Badge variant="outline" className={getConfidenceColor(result.confidence)}>
                            {result.confidence}% confidence
                          </Badge>
                        </div>
                        <AlertDescription className="text-sm">{result.explanation}</AlertDescription>
                        {result.suggestion && (
                          <div className="mt-2 flex items-center space-x-2">
                            <Lightbulb className="h-4 w-4 text-amber-500" />
                            <span className="text-sm text-muted-foreground">Suggestion:</span>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => applySuggestion(result.field, result.suggestion!)}
                              className="h-6 px-2 text-xs"
                            >
                              Apply "{result.suggestion}"
                            </Button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </Alert>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-end space-x-3">
          <Button
            variant="outline"
            onClick={() => {
              setFormData({ licensePlate: "", brand: "", model: "", year: "" })
              setValidationResults([])
            }}
          >
            Clear Form
          </Button>
          <Button
            disabled={validationResults.some((r) => !r.isValid) || validationResults.length === 0}
            className="bg-primary hover:bg-primary/90"
          >
            Validate Vehicle
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
