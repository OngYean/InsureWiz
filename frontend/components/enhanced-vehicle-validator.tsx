"use client"

import { useState, useEffect, useCallback, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CheckCircle, AlertTriangle, Lightbulb, Car, Calendar, Tag, Hash, User, Palette } from "lucide-react"

interface SuggestionResponse {
  primary: string | null
  suggestions: string[]
  completion: string
}

interface YearData {
  year: number
  brands: string[]
  models: Record<string, string[]>
  colors: Record<string, Record<string, string[]>>
}

interface ValidationResult {
  field: string
  isValid: boolean
  confidence: number
  suggestion?: string
  explanation: string
}

interface VehicleFormData {
  year: string
  ownerIc: string
  plateNumber: string
  brand: string
  model: string
  color: string
}

interface AutoCompleteInputProps {
  label: string
  value: string
  onChange: (value: string) => void
  onTabComplete?: () => void
  placeholder: string
  suggestions: string[]
  primarySuggestion: string | null
  completion: string
  icon: React.ReactNode
  disabled?: boolean
  error?: string
}

const AutoCompleteInput: React.FC<AutoCompleteInputProps> = ({
  label,
  value,
  onChange,
  onTabComplete,
  placeholder,
  suggestions,
  primarySuggestion,
  completion,
  icon,
  disabled = false,
  error
}) => {
  const [showDropdown, setShowDropdown] = useState(false)
  const [focusedIndex, setFocusedIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab' && completion && primarySuggestion) {
      e.preventDefault()
      onChange(primarySuggestion)
      onTabComplete?.()
      setShowDropdown(false)
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      setFocusedIndex(prev => Math.min(prev + 1, suggestions.length - 1))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setFocusedIndex(prev => Math.max(prev - 1, -1))
    } else if (e.key === 'Enter' && focusedIndex >= 0) {
      e.preventDefault()
      onChange(suggestions[focusedIndex])
      setShowDropdown(false)
    } else if (e.key === 'Escape') {
      setShowDropdown(false)
    }
  }

  const handleFocus = () => {
    if (suggestions.length > 0) {
      setShowDropdown(true)
    }
  }

  const handleBlur = () => {
    // Delay hiding dropdown to allow clicking on suggestions
    setTimeout(() => setShowDropdown(false), 150)
  }

  const handleSuggestionClick = (suggestion: string) => {
    onChange(suggestion)
    setShowDropdown(false)
    inputRef.current?.focus()
  }

  // Calculate the width of the typed text for positioning
  const getTextWidth = (text: string, font: string) => {
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    if (context) {
      context.font = font
      return context.measureText(text).width
    }
    return 0
  }

  return (
    <div className="space-y-2 relative">
      <Label className="flex items-center gap-2">
        {icon}
        {label}
      </Label>
      <div className="relative">
        {/* Background completion text */}
        {completion && value && (
          <div className="absolute inset-0 px-3 py-2 pointer-events-none z-0 flex items-center font-mono text-sm">
            <span className="invisible select-none">{value}</span>
            <span className="text-muted-foreground/30 select-none">{completion}</span>
          </div>
        )}
        
        {/* Main input */}
        <Input
          ref={inputRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={`relative z-10 bg-background/50 backdrop-blur-sm font-mono text-sm ${
            error ? 'border-destructive focus-visible:ring-destructive' : ''
          }`}
        />
        
        {/* Dropdown suggestions */}
        {showDropdown && suggestions.length > 0 && (
          <div className="absolute z-20 w-full mt-1 bg-popover border border-border rounded-md shadow-lg max-h-60 overflow-auto">
            {suggestions.map((suggestion, index) => (
              <div
                key={index}
                className={`px-3 py-2 cursor-pointer transition-colors duration-150 text-sm ${
                  index === focusedIndex 
                    ? 'bg-accent text-accent-foreground' 
                    : 'hover:bg-accent/50 text-popover-foreground'
                } ${suggestion === primarySuggestion ? 'font-semibold border-l-2 border-l-primary' : ''}`}
                onClick={() => handleSuggestionClick(suggestion)}
              >
                <div className="flex items-center justify-between">
                  <span>{suggestion}</span>
                  {suggestion === primarySuggestion && (
                    <span className="text-xs text-muted-foreground bg-muted px-1.5 py-0.5 rounded">
                      Tab
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {error && (
        <p className="text-sm text-destructive flex items-center gap-1">
          <AlertTriangle className="h-3 w-3" />
          {error}
        </p>
      )}
    </div>
  )
}

interface EnhancedVehicleValidatorProps {
  onVehicleInfoChange?: (vehicleInfo: any, isLoading: boolean) => void
}

export default function EnhancedVehicleValidatorForm({ onVehicleInfoChange }: EnhancedVehicleValidatorProps) {
  const [formData, setFormData] = useState<VehicleFormData>({
    year: "",
    ownerIc: "",
    plateNumber: "",
    brand: "",
    model: "",
    color: ""
  })

  const [availableYears, setAvailableYears] = useState<number[]>([])
  const [yearDataCache, setYearDataCache] = useState<Record<number, YearData>>({})
  const [currentYearData, setCurrentYearData] = useState<YearData | null>(null)
  const [isLoadingYearData, setIsLoadingYearData] = useState(false)
  const [brandSuggestions, setBrandSuggestions] = useState<SuggestionResponse>({
    primary: null,
    suggestions: [],
    completion: ""
  })
  const [modelSuggestions, setModelSuggestions] = useState<SuggestionResponse>({
    primary: null,
    suggestions: [],
    completion: ""
  })

  const [colorSuggestions, setColorSuggestions] = useState<SuggestionResponse>({
    primary: null,
    suggestions: [],
    completion: ""
  })

  const [validationResults, setValidationResults] = useState<ValidationResult[]>([])
  const [isValidating, setIsValidating] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [vehicleInfo, setVehicleInfo] = useState<any>(null)

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  // Client-side filtering functions
  const getFilteredSuggestions = useCallback((query: string, items: string[], maxResults: number = 5) => {
    if (!query || !items) {
      return {
        primary: null,
        suggestions: items.slice(0, maxResults),
        completion: ""
      }
    }

    const queryLower = query.toLowerCase()
    const matches: Array<{text: string, score: number, completion: string}> = []

    for (const item of items) {
      const itemLower = item.toLowerCase()
      
      // Exact prefix match gets highest priority
      if (itemLower.startsWith(queryLower)) {
        matches.push({
          text: item,
          score: 1.0,
          completion: item.slice(query.length)
        })
      }
      // Contains match gets medium priority
      else if (itemLower.includes(queryLower)) {
        matches.push({
          text: item,
          score: 0.8,
          completion: ""
        })
      }
    }

    // Sort by score (descending) and return top results
    matches.sort((a, b) => b.score - a.score)
    const topMatches = matches.slice(0, maxResults)

    return {
      primary: topMatches[0]?.text || null,
      suggestions: topMatches.map(m => m.text),
      completion: topMatches[0]?.completion || ""
    }
  }, [])

  // Load year data with caching
  const loadYearData = useCallback(async (year: number) => {
    // Check cache first
    if (yearDataCache[year]) {
      setCurrentYearData(yearDataCache[year])
      return yearDataCache[year]
    }

    // Check localStorage
    const cacheKey = `yearData_${year}`
    const cached = localStorage.getItem(cacheKey)
    if (cached) {
      try {
        const cachedData = JSON.parse(cached)
        // Check if cached data is less than 24 hours old
        const cacheTime = localStorage.getItem(`${cacheKey}_time`)
        if (cacheTime && Date.now() - parseInt(cacheTime) < 24 * 60 * 60 * 1000) {
          setYearDataCache(prev => ({ ...prev, [year]: cachedData }))
          setCurrentYearData(cachedData)
          return cachedData
        }
      } catch (e) {
        console.warn('Failed to parse cached year data:', e)
      }
    }

    // Fetch from API
    setIsLoadingYearData(true)
    try {
      const response = await fetch(`${API_BASE}/api/validator/year-data/${year}`)
      if (response.ok) {
        const yearData = await response.json()
        
        // Cache in memory and localStorage
        setYearDataCache(prev => ({ ...prev, [year]: yearData }))
        setCurrentYearData(yearData)
        localStorage.setItem(cacheKey, JSON.stringify(yearData))
        localStorage.setItem(`${cacheKey}_time`, Date.now().toString())
        
        return yearData
      } else {
        throw new Error(`Failed to load year data: ${response.statusText}`)
      }
    } catch (error) {
      console.error('Error loading year data:', error)
      return null
    } finally {
      setIsLoadingYearData(false)
    }
  }, [API_BASE, yearDataCache])

  // Load available years on component mount
  useEffect(() => {
    const loadYears = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/validator/years`)
        if (response.ok) {
          const years = await response.json()
          setAvailableYears(years)
        }
      } catch (error) {
        console.error('Error loading years:', error)
      }
    }
    loadYears()
  }, [API_BASE])

  // Show available models when brand is selected
  useEffect(() => {
    if (formData.brand && currentYearData) {
      // Find the exact brand match (case-insensitive)
      const exactBrand = currentYearData.brands.find(b => b.toLowerCase() === formData.brand.toLowerCase()) || formData.brand
      const models = currentYearData.models[exactBrand] || []
      
      if (models.length > 0) {
        setModelSuggestions({
          primary: null,
          suggestions: models.slice(0, 5),
          completion: ""
        })
      }
    } else {
      setModelSuggestions({ primary: null, suggestions: [], completion: "" })
    }
  }, [formData.brand, currentYearData])

  // Show available colors when model is selected
  useEffect(() => {
    if (formData.brand && formData.model && currentYearData) {
      // Find the exact brand and model matches (case-insensitive)
      const exactBrand = currentYearData.brands.find(b => b.toLowerCase() === formData.brand.toLowerCase()) || formData.brand
      const brandModels = currentYearData.models[exactBrand] || []
      const exactModel = brandModels.find(m => m.toLowerCase() === formData.model.toLowerCase()) || formData.model
      
      const colors = currentYearData.colors[exactBrand]?.[exactModel] || []
      
      if (colors.length > 0) {
        setColorSuggestions({
          primary: null,
          suggestions: colors.slice(0, 5),
          completion: ""
        })
      }
    } else {
      setColorSuggestions({ primary: null, suggestions: [], completion: "" })
    }
  }, [formData.brand, formData.model, currentYearData])

  // Immediate brand suggestions (client-side)
  const getBrandSuggestions = useCallback((query: string) => {
    if (!currentYearData) {
      setBrandSuggestions({ primary: null, suggestions: [], completion: "" })
      return
    }

    const suggestions = getFilteredSuggestions(query, currentYearData.brands)
    setBrandSuggestions(suggestions)
  }, [currentYearData, getFilteredSuggestions])

  // Immediate model suggestions (client-side)
  const getModelSuggestions = useCallback((brand: string, query: string) => {
    if (!currentYearData || !brand) {
      setModelSuggestions({ primary: null, suggestions: [], completion: "" })
      return
    }

    // Find the exact brand match (case-insensitive)
    const exactBrand = currentYearData.brands.find(b => b.toLowerCase() === brand.toLowerCase()) || brand
    const models = currentYearData.models[exactBrand] || []
    const suggestions = getFilteredSuggestions(query, models)
    setModelSuggestions(suggestions)
  }, [currentYearData, getFilteredSuggestions])

  // Immediate color suggestions (client-side)
  const getColorSuggestions = useCallback((brand: string, model: string, query: string) => {
    if (!currentYearData || !brand || !model) {
      setColorSuggestions({ primary: null, suggestions: [], completion: "" })
      return
    }

    // Find the exact brand and model matches (case-insensitive)
    const exactBrand = currentYearData.brands.find(b => b.toLowerCase() === brand.toLowerCase()) || brand
    const brandModels = currentYearData.models[exactBrand] || []
    const exactModel = brandModels.find(m => m.toLowerCase() === model.toLowerCase()) || model
    
    const colors = currentYearData.colors[exactBrand]?.[exactModel] || []
    const suggestions = getFilteredSuggestions(query, colors)
    setColorSuggestions(suggestions)
  }, [currentYearData, getFilteredSuggestions])

  // Validate formats
  const validateFormats = async (ic?: string, plateNumber?: string) => {
    try {
      const response = await fetch(`${API_BASE}/api/validator/validate-formats`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ic: ic || undefined,
          plate_number: plateNumber || undefined
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        const results: ValidationResult[] = []
        
        if (data.ic) {
          results.push({
            field: 'ownerIc',
            isValid: data.ic.valid,
            confidence: data.ic.valid ? 99 : 20,
            explanation: data.ic.error || 'Valid IC format'
          })
        }
        
        if (data.plate_number) {
          results.push({
            field: 'plateNumber',
            isValid: data.plate_number.valid,
            confidence: data.plate_number.valid ? 99 : 20,
            explanation: data.plate_number.error || 'Valid plate number format'
          })
        }
        
        setValidationResults(prev => {
          const filtered = prev.filter(r => 
            !results.some(nr => nr.field === r.field)
          )
          return [...filtered, ...results]
        })
      }
    } catch (error) {
      console.error('Error validating formats:', error)
    }
  }

  // Handle form changes
  const handleYearChange = async (year: string) => {
    setFormData(prev => ({ ...prev, year, brand: "", model: "", color: "" }))
    
    // Load year data for client-side filtering
    if (year) {
      const yearData = await loadYearData(parseInt(year))
      // Show all available brands immediately after year data is loaded
      if (yearData) {
        setBrandSuggestions({
          primary: null,
          suggestions: yearData.brands.slice(0, 5),
          completion: ""
        })
      }
    } else {
      setCurrentYearData(null)
      setBrandSuggestions({ primary: null, suggestions: [], completion: "" })
    }
    
    // Clear other suggestions
    setModelSuggestions({ primary: null, suggestions: [], completion: "" })
    setColorSuggestions({ primary: null, suggestions: [], completion: "" })
  }

  const handleBrandChange = (brand: string) => {
    setFormData(prev => ({ ...prev, brand, model: "", color: "" }))
    setColorSuggestions({ primary: null, suggestions: [], completion: "" })
    
    // Always get brand suggestions immediately
    getBrandSuggestions(brand)
    
    // Show available models for selected brand
    if (brand && currentYearData) {
      const models = currentYearData.models[brand] || []
      setModelSuggestions({
        primary: null,
        suggestions: models.slice(0, 5),
        completion: ""
      })
    } else {
      setModelSuggestions({ primary: null, suggestions: [], completion: "" })
    }
  }

  const handleModelChange = (model: string) => {
    setFormData(prev => ({ ...prev, model, color: "" }))
    
    // Always get model suggestions immediately
    if (formData.brand) {
      getModelSuggestions(formData.brand, model)
    }
  }

  const handleColorChange = (color: string) => {
    setFormData(prev => ({ ...prev, color }))
    
    // Always get color suggestions immediately
    if (formData.brand && formData.model) {
      getColorSuggestions(formData.brand, formData.model, color)
    }
  }

  const handleIcChange = (ic: string) => {
    setFormData(prev => ({ ...prev, ownerIc: ic }))
    if (ic.length >= 12) {
      validateFormats(ic, undefined)
    }
  }

  const handlePlateChange = (plate: string) => {
    setFormData(prev => ({ ...prev, plateNumber: plate }))
    if (plate.length >= 3) {
      validateFormats(undefined, plate)
    }
  }

  const handleValidateVehicle = async () => {
    setIsLoading(true)
    onVehicleInfoChange?.(null, true)
    
    try {
      const response = await fetch(`${API_BASE}/api/validator/validate-vehicle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          year: parseInt(formData.year),
          brand: formData.brand,
          model: formData.model,
          color: formData.color,
          owner_ic: formData.ownerIc,
          plate_number: formData.plateNumber
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        setVehicleInfo(data)
        onVehicleInfoChange?.(data, false)
      } else {
        const error = await response.json()
        alert(`Validation failed: ${error.detail}`)
        onVehicleInfoChange?.(null, false)
      }
    } catch (error) {
      console.error('Error validating vehicle:', error)
      alert('Error validating vehicle. Please try again.')
      onVehicleInfoChange?.(null, false)
    } finally {
      setIsLoading(false)
    }
  }

  const getValidationResult = (field: string) => {
    return validationResults.find(r => r.field === field)
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Car className="h-6 w-6" />
            Smart Vehicle Validator
          </CardTitle>
          <CardDescription>
            Enter vehicle details with AI-powered real-time suggestions and validation
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Year Selection */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Registration Year
            </Label>
            <Select value={formData.year} onValueChange={handleYearChange}>
              <SelectTrigger>
                <SelectValue placeholder="Select registration year" />
              </SelectTrigger>
              <SelectContent>
                {availableYears.map(year => (
                  <SelectItem key={year} value={year.toString()}>
                    {year}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {isLoadingYearData && (
              <div className="text-sm text-muted-foreground flex items-center gap-2">
                <div className="animate-spin h-3 w-3 border border-current border-t-transparent rounded-full"></div>
                Loading vehicle data for {formData.year}...
              </div>
            )}
          </div>

          {/* Owner IC */}
          <AutoCompleteInput
            label="Owner IC Number"
            value={formData.ownerIc}
            onChange={handleIcChange}
            placeholder="Enter IC number (e.g., 850101-01-1234)"
            suggestions={[]}
            primarySuggestion={null}
            completion=""
            icon={<User className="h-4 w-4" />}
            error={getValidationResult('ownerIc')?.isValid === false ? 
              getValidationResult('ownerIc')?.explanation : undefined}
          />

          {/* Plate Number */}
          <AutoCompleteInput
            label="Plate Number"
            value={formData.plateNumber}
            onChange={handlePlateChange}
            placeholder="Enter plate number (e.g., ABC 1234)"
            suggestions={[]}
            primarySuggestion={null}
            completion=""
            icon={<Hash className="h-4 w-4" />}
            error={getValidationResult('plateNumber')?.isValid === false ? 
              getValidationResult('plateNumber')?.explanation : undefined}
          />

          {/* Brand */}
          <AutoCompleteInput
            label="Vehicle Brand"
            value={formData.brand}
            onChange={handleBrandChange}
            placeholder={isLoadingYearData ? "Loading..." : "Start typing brand name..."}
            suggestions={brandSuggestions.suggestions}
            primarySuggestion={brandSuggestions.primary}
            completion={brandSuggestions.completion}
            icon={<Tag className="h-4 w-4" />}
            disabled={!formData.year || isLoadingYearData}
          />

          {/* Model */}
          <AutoCompleteInput
            label="Vehicle Model"
            value={formData.model}
            onChange={handleModelChange}
            placeholder={isLoadingYearData ? "Loading..." : "Start typing model name..."}
            suggestions={modelSuggestions.suggestions}
            primarySuggestion={modelSuggestions.primary}
            completion={modelSuggestions.completion}
            icon={<Car className="h-4 w-4" />}
            disabled={!formData.brand || isLoadingYearData}
          />

          {/* Color */}
          <AutoCompleteInput
            label="Vehicle Color"
            value={formData.color}
            onChange={handleColorChange}
            placeholder={isLoadingYearData ? "Loading..." : "Start typing color name..."}
            suggestions={colorSuggestions.suggestions}
            primarySuggestion={colorSuggestions.primary}
            completion={colorSuggestions.completion}
            icon={<Palette className="h-4 w-4" />}
            disabled={!formData.model || isLoadingYearData}
          />

          {/* Real-time Field Validation */}
          {validationResults.length > 0 && (
            <div className="space-y-2">
              <h4 className="font-medium text-sm">Real-time Field Validation</h4>
              {validationResults.map((result, index) => (
                <Alert key={index} className={result.isValid ? "border-green-500/50 bg-green-50 dark:bg-green-950/10" : "border-destructive/50 bg-destructive/5"}>
                  <div className="flex items-center gap-2">
                    {result.isValid ? (
                      <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    ) : (
                      <AlertTriangle className="h-4 w-4 text-destructive" />
                    )}
                    <AlertDescription className={result.isValid ? "text-green-800 dark:text-green-300" : "text-destructive"}>
                      {result.explanation}
                    </AlertDescription>
                  </div>
                </Alert>
              ))}
            </div>
          )}

          {/* Validate Button */}
          <Button 
            onClick={handleValidateVehicle}
            disabled={!formData.year || !formData.brand || !formData.model || !formData.color || isLoading}
            className="w-full"
          >
            {isLoading ? "Validating..." : "Validate Vehicle Details"}
          </Button>

          {/* Instructions */}
          <Alert className="border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950/20">
            <Lightbulb className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            <AlertDescription className="text-blue-800 dark:text-blue-300">
              <strong>Tips:</strong> Press Tab to auto-complete suggestions. Use arrow keys to navigate dropdown options.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    </div>
  )
}
