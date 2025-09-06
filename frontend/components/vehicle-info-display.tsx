"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  Car, 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  Gauge, 
  Palette, 
  MapPin, 
  Calendar,
  Fuel,
  Users,
  AlertCircle,
  Image as ImageIcon,
  Search,
  Brain,
  Shield
} from "lucide-react"

interface VehicleInfo {
  status: string
  confidence: number
  message: string
  vehicle_info?: {
    brand: string
    model: string
    year: number
    type: string
    fuel_type: string
    available_colors: string[]
    common_states: string[]
    total_registrations: number
  }
  vehicle_images?: string[]
  local_validation?: {
    brand_found: boolean
    model_found: boolean
    color_found: boolean
    total_records: number
    available_colors: string[]
  }
  agent_analysis?: string
  recommendations?: string[]
  typo_detection?: {
    brand_has_typo: boolean
    corrected_brand?: string
    model_has_typo: boolean
    corrected_model?: string
    year_has_error: boolean
    corrected_year?: number
    color_has_typo: boolean
    corrected_color?: string
  }
  insurance_risk?: {
    policy_risk_level: string
    pricing_impact: string
    coverage_validity: string
    fraud_indicators: string[]
  }
  pydantic_data?: {
    validation_status: string
    confidence_score: number
    color_validation?: {
      color_found_locally: boolean
      color_available_for_model: boolean
      alternative_colors: string[]
      color_verification_source: string
      insurance_color_category: string
    }
    vehicle_info?: {
      brand: string
      model: string
      year: string
      market_availability: string
      assembly_type: string
      insurance_category: string
      common_insurance_model: boolean
    }
    search_performed: boolean
    image_urls: string[]
    validation_notes: string
    recommendations: string[]
  }
}

interface VehicleInfoDisplayProps {
  vehicleInfo: VehicleInfo | null
  isLoading: boolean
}

export default function VehicleInfoDisplay({ vehicleInfo, isLoading }: VehicleInfoDisplayProps) {
  if (isLoading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Car className="h-5 w-5 animate-pulse" />
              Validating Vehicle...
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-muted rounded animate-pulse" />
                <div className="h-4 bg-muted rounded flex-1 animate-pulse" />
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-muted rounded animate-pulse" />
                <div className="h-4 bg-muted rounded flex-1 animate-pulse" />
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-muted rounded animate-pulse" />
                <div className="h-4 bg-muted rounded flex-1 animate-pulse" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!vehicleInfo) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="h-5 w-5" />
            Vehicle Information
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-muted-foreground py-8">
            <Car className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>Complete the form and click "Validate Vehicle Details" to see detailed information about your vehicle.</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'valid':
        return <CheckCircle className="h-5 w-5 text-green-600" />
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />
      case 'invalid':
        return <AlertCircle className="h-5 w-5 text-red-600" />
      default:
        return <Info className="h-5 w-5 text-blue-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'valid':
        return 'green'
      case 'warning':
        return 'yellow'
      case 'invalid':
        return 'red'
      default:
        return 'blue'
    }
  }

  return (
    <div className="space-y-6">
      {/* Validation Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {getStatusIcon(vehicleInfo.status)}
            Validation Result
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Confidence Score</span>
            <Badge variant={vehicleInfo.confidence > 80 ? "default" : vehicleInfo.confidence > 60 ? "secondary" : "outline"}>
              {vehicleInfo.confidence}%
            </Badge>
          </div>
          
          <Progress value={vehicleInfo.confidence} className="w-full" />
          
          <Alert className={`border-${getStatusColor(vehicleInfo.status)}-200 bg-${getStatusColor(vehicleInfo.status)}-50 dark:bg-${getStatusColor(vehicleInfo.status)}-950/20`}>
            <AlertDescription className={`text-${getStatusColor(vehicleInfo.status)}-800 dark:text-${getStatusColor(vehicleInfo.status)}-300`}>
              {vehicleInfo.message}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Vehicle Images */}
      {vehicleInfo.vehicle_images && vehicleInfo.vehicle_images.length > 0 ? (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImageIcon className="h-5 w-5" />
              Vehicle Images
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-4">
              {vehicleInfo.vehicle_images.slice(0, 3).map((imageUrl, index) => (
                <div key={index} className="relative overflow-hidden rounded-lg border bg-muted">
                  <img
                    src={imageUrl}
                    alt={`${vehicleInfo.vehicle_info?.brand} ${vehicleInfo.vehicle_info?.model} ${vehicleInfo.vehicle_info?.year}`}
                    className="w-full h-48 object-cover hover:scale-105 transition-transform duration-300"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      const parent = target.parentElement;
                      if (parent) {
                        parent.innerHTML = `
                          <div class="w-full h-48 flex items-center justify-center bg-muted">
                            <div class="text-center text-muted-foreground">
                              <svg class="h-8 w-8 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                              </svg>
                              <p class="text-xs">Image unavailable</p>
                            </div>
                          </div>
                        `;
                      }
                    }}
                    loading="lazy"
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-black/70 text-white p-2 text-xs">
                    {vehicleInfo.vehicle_info?.brand} {vehicleInfo.vehicle_info?.model} ({vehicleInfo.vehicle_info?.year})
                  </div>
                </div>
              ))}
            </div>
            {vehicleInfo.vehicle_images.length > 3 && (
              <p className="text-xs text-muted-foreground mt-2 text-center">
                +{vehicleInfo.vehicle_images.length - 3} more images found
              </p>
            )}
          </CardContent>
        </Card>
      ) : vehicleInfo.vehicle_info && vehicleInfo.status === 'valid' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImageIcon className="h-5 w-5" />
              Vehicle Images
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Car className="h-16 w-16 text-muted-foreground/30 mb-4" />
              <p className="text-sm text-muted-foreground">
                No images found for this vehicle model
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                {vehicleInfo.vehicle_info.brand} {vehicleInfo.vehicle_info.model} ({vehicleInfo.vehicle_info.year})
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* AI Agent Validation Analysis - MOVED BELOW IMAGES */}
      {vehicleInfo.pydantic_data && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-purple-600" />
              AI Agent Validation Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Validation Status from Agent */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Shield className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Agent Status</span>
                </div>
                <Badge 
                  variant={
                    vehicleInfo.pydantic_data.validation_status === 'valid' ? 'default' :
                    vehicleInfo.pydantic_data.validation_status === 'warning' ? 'secondary' :
                    vehicleInfo.pydantic_data.validation_status === 'invalid' ? 'destructive' :
                    'outline'
                  }
                  className="text-xs"
                >
                  {vehicleInfo.pydantic_data.validation_status?.toUpperCase() || 'UNKNOWN'}
                </Badge>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Search className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">External Search</span>
                </div>
                <Badge 
                  variant={vehicleInfo.pydantic_data.search_performed ? 'default' : 'outline'}
                  className="text-xs"
                >
                  {vehicleInfo.pydantic_data.search_performed ? 'PERFORMED' : 'NOT PERFORMED'}
                </Badge>
              </div>
            </div>

            {/* Agent Analysis Notes */}
            {vehicleInfo.pydantic_data.validation_notes && (
              <Alert className="border-blue-200 bg-blue-50 dark:bg-blue-950/20">
                <Brain className="h-4 w-4 text-blue-600" />
                <AlertDescription className="text-blue-800 dark:text-blue-300">
                  <strong>AI Analysis:</strong> {vehicleInfo.pydantic_data.validation_notes}
                </AlertDescription>
              </Alert>
            )}

            {/* Color Validation Details */}
            {vehicleInfo.pydantic_data.color_validation && (
              <div className="space-y-3">
                <h4 className="font-medium text-sm">Color Validation Details</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center justify-between">
                    <span>Found Locally:</span>
                    {vehicleInfo.pydantic_data.color_validation.color_found_locally ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-red-600" />
                    )}
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span>Available for Model:</span>
                    {vehicleInfo.pydantic_data.color_validation.color_available_for_model ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-red-600" />
                    )}
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span>Verification Source:</span>
                    <Badge variant="outline" className="text-xs">
                      {vehicleInfo.pydantic_data.color_validation.color_verification_source}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span>Insurance Category:</span>
                    <Badge 
                      variant={
                        vehicleInfo.pydantic_data.color_validation.insurance_color_category === 'premium' ? 'default' :
                        vehicleInfo.pydantic_data.color_validation.insurance_color_category === 'rare' ? 'destructive' :
                        'outline'
                      }
                      className="text-xs"
                    >
                      {vehicleInfo.pydantic_data.color_validation.insurance_color_category?.toUpperCase()}
                    </Badge>
                  </div>
                </div>

                {/* Alternative Colors */}
                {vehicleInfo.pydantic_data.color_validation.alternative_colors && 
                 vehicleInfo.pydantic_data.color_validation.alternative_colors.length > 0 && (
                  <div className="space-y-2">
                    <span className="text-sm font-medium">Alternative Colors:</span>
                    <div className="flex flex-wrap gap-1">
                      {vehicleInfo.pydantic_data.color_validation.alternative_colors.map((color, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {color}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Vehicle Market Information */}
            {vehicleInfo.pydantic_data.vehicle_info && (
              <div className="space-y-3">
                <h4 className="font-medium text-sm">Market Information</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center justify-between">
                    <span>Market Availability:</span>
                    <Badge 
                      variant={
                        vehicleInfo.pydantic_data.vehicle_info.market_availability === 'available' ? 'default' :
                        vehicleInfo.pydantic_data.vehicle_info.market_availability === 'unavailable' ? 'destructive' :
                        'outline'
                      }
                      className="text-xs"
                    >
                      {vehicleInfo.pydantic_data.vehicle_info.market_availability?.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span>Assembly Type:</span>
                    <Badge variant="outline" className="text-xs">
                      {vehicleInfo.pydantic_data.vehicle_info.assembly_type?.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span>Insurance Category:</span>
                    <Badge 
                      variant={
                        vehicleInfo.pydantic_data.vehicle_info.insurance_category === 'luxury' ? 'default' :
                        vehicleInfo.pydantic_data.vehicle_info.insurance_category === 'sports' ? 'destructive' :
                        'outline'
                      }
                      className="text-xs"
                    >
                      {vehicleInfo.pydantic_data.vehicle_info.insurance_category?.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span>Common Model:</span>
                    {vehicleInfo.pydantic_data.vehicle_info.common_insurance_model ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <AlertTriangle className="h-4 w-4 text-amber-600" />
                    )}
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Vehicle Specifications */}
      {vehicleInfo.vehicle_info && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Car className="h-5 w-5" />
              Vehicle Specifications
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Year</span>
                </div>
                <p className="text-sm text-muted-foreground pl-6">{vehicleInfo.vehicle_info.year}</p>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Gauge className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Type</span>
                </div>
                <p className="text-sm text-muted-foreground pl-6">{vehicleInfo.vehicle_info.type}</p>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Fuel className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Fuel Type</span>
                </div>
                <p className="text-sm text-muted-foreground pl-6">{vehicleInfo.vehicle_info.fuel_type}</p>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Registrations</span>
                </div>
                <p className="text-sm text-muted-foreground pl-6">{vehicleInfo.vehicle_info.total_registrations.toLocaleString()}</p>
              </div>
            </div>

            {/* Available Colors */}
            {vehicleInfo.vehicle_info.available_colors.length > 0 && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Palette className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Available Colors</span>
                </div>
                <div className="flex flex-wrap gap-1 pl-6">
                  {vehicleInfo.vehicle_info.available_colors.slice(0, 6).map((color, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {color}
                    </Badge>
                  ))}
                  {vehicleInfo.vehicle_info.available_colors.length > 6 && (
                    <Badge variant="outline" className="text-xs">
                      +{vehicleInfo.vehicle_info.available_colors.length - 6} more
                    </Badge>
                  )}
                </div>
              </div>
            )}

            {/* Common States */}
            {vehicleInfo.vehicle_info.common_states.length > 0 && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Common Registration States</span>
                </div>
                <div className="flex flex-wrap gap-1 pl-6">
                  {vehicleInfo.vehicle_info.common_states.map((state, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {state}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Typo Detection & Corrections */}
      {vehicleInfo.typo_detection && (
        vehicleInfo.typo_detection?.brand_has_typo || 
        vehicleInfo.typo_detection?.model_has_typo || 
        vehicleInfo.typo_detection?.year_has_error || 
        vehicleInfo.typo_detection?.color_has_typo
      ) && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-600" />
              Smart Error Detection
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {vehicleInfo.typo_detection?.brand_has_typo && (
              <Alert className="border-amber-200 bg-amber-50 dark:bg-amber-950/20">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <AlertDescription className="text-amber-800 dark:text-amber-300">
                  <strong>Brand Typo Detected:</strong> "{vehicleInfo.typo_detection?.corrected_brand}" suggested instead of the entered brand name
                </AlertDescription>
              </Alert>
            )}
            
            {vehicleInfo.typo_detection?.model_has_typo && (
              <Alert className="border-amber-200 bg-amber-50 dark:bg-amber-950/20">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <AlertDescription className="text-amber-800 dark:text-amber-300">
                  <strong>Model Typo Detected:</strong> "{vehicleInfo.typo_detection?.corrected_model}" suggested instead of the entered model name
                </AlertDescription>
              </Alert>
            )}
            
            {vehicleInfo.typo_detection?.year_has_error && (
              <Alert className="border-amber-200 bg-amber-50 dark:bg-amber-950/20">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <AlertDescription className="text-amber-800 dark:text-amber-300">
                  <strong>Year Error Detected:</strong> "{vehicleInfo.typo_detection?.corrected_year}" suggested instead of the entered year
                </AlertDescription>
              </Alert>
            )}
            
            {vehicleInfo.typo_detection?.color_has_typo && (
              <Alert className="border-amber-200 bg-amber-50 dark:bg-amber-950/20">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <AlertDescription className="text-amber-800 dark:text-amber-300">
                  <strong>Color Typo Detected:</strong> "{vehicleInfo.typo_detection?.corrected_color}" suggested instead of the entered color
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>
      )}

      {/* Insurance Risk Assessment */}
      {vehicleInfo.insurance_risk && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-blue-600" />
              Insurance Risk Assessment
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Policy Risk Level</span>
                </div>
                <Badge 
                  variant={
                    vehicleInfo.insurance_risk?.policy_risk_level === 'low' ? 'default' :
                    vehicleInfo.insurance_risk?.policy_risk_level === 'medium' ? 'secondary' :
                    vehicleInfo.insurance_risk?.policy_risk_level === 'high' ? 'destructive' :
                    'outline'
                  }
                  className="text-xs"
                >
                  {vehicleInfo.insurance_risk?.policy_risk_level?.toUpperCase() || 'UNKNOWN'}
                </Badge>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Pricing Impact</span>
                </div>
                <Badge 
                  variant={
                    vehicleInfo.insurance_risk?.pricing_impact === 'none' ? 'default' :
                    vehicleInfo.insurance_risk?.pricing_impact === 'minor' ? 'secondary' :
                    'destructive'
                  }
                  className="text-xs"
                >
                  {vehicleInfo.insurance_risk?.pricing_impact?.toUpperCase() || 'UNKNOWN'}
                </Badge>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">Coverage Validity</span>
                </div>
                <Badge 
                  variant={
                    vehicleInfo.insurance_risk?.coverage_validity === 'valid' ? 'default' :
                    vehicleInfo.insurance_risk?.coverage_validity === 'questionable' ? 'secondary' :
                    'destructive'
                  }
                  className="text-xs"
                >
                  {vehicleInfo.insurance_risk?.coverage_validity?.toUpperCase() || 'UNKNOWN'}
                </Badge>
              </div>
            </div>
            
            {/* Fraud Indicators */}
            {vehicleInfo.insurance_risk?.fraud_indicators && vehicleInfo.insurance_risk.fraud_indicators.length > 0 && (
              <Alert className="border-red-200 bg-red-50 dark:bg-red-950/20">
                <AlertCircle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800 dark:text-red-300">
                  <strong>Fraud Alert:</strong> {vehicleInfo.insurance_risk?.fraud_indicators?.join(', ')}
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>
      )}

      {/* Enhanced Recommendations */}
      {vehicleInfo.recommendations && vehicleInfo.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="h-5 w-5" />
              Insurance Application Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {vehicleInfo.recommendations.map((rec, index) => {
                const isError = rec.includes('TYPO DETECTED') || rec.includes('ERROR') || rec.includes('CRITICAL');
                const isWarning = rec.includes('WARNING') || rec.includes('RISK') || rec.includes('⚠️');
                const isSuccess = rec.includes('✅') || rec.includes('READY') || rec.includes('APPROVED');
                const isFraud = rec.includes('FRAUD') || rec.includes('🚨');
                
                let alertClass = "";
                let iconColor = "text-blue-600";
                
                if (isError || isFraud) {
                  alertClass = "border-red-200 bg-red-50 dark:bg-red-950/20";
                  iconColor = "text-red-600";
                } else if (isWarning) {
                  alertClass = "border-amber-200 bg-amber-50 dark:bg-amber-950/20";
                  iconColor = "text-amber-600";
                } else if (isSuccess) {
                  alertClass = "border-green-200 bg-green-50 dark:bg-green-950/20";
                  iconColor = "text-green-600";
                }
                
                return (
                  <Alert key={index} className={alertClass}>
                    <Info className={`h-4 w-4 ${iconColor}`} />
                    <AlertDescription className={
                      isError || isFraud ? "text-red-800 dark:text-red-300" :
                      isWarning ? "text-amber-800 dark:text-amber-300" :
                      isSuccess ? "text-green-800 dark:text-green-300" :
                      ""
                    }>
                      {rec}
                    </AlertDescription>
                  </Alert>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Database Analysis */}
      {vehicleInfo.local_validation && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5" />
              Database Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Brand Found</span>
              {vehicleInfo.local_validation?.brand_found ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-red-600" />
              )}
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm">Model Found</span>
              {vehicleInfo.local_validation?.model_found ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-red-600" />
              )}
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm">Color Found</span>
              {vehicleInfo.local_validation?.color_found ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-red-600" />
              )}
            </div>
            
            <div className="pt-2 border-t">
              <span className="text-sm text-muted-foreground">
                Database Records: {vehicleInfo.local_validation?.total_records?.toLocaleString() || 0}
              </span>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
