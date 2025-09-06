"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import EnhancedVehicleValidatorForm from "@/components/enhanced-vehicle-validator"
import VehicleInfoDisplay from "@/components/vehicle-info-display"
import { Car } from "lucide-react"

export default function ValidatorPage() {
  const [vehicleInfo, setVehicleInfo] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleVehicleInfoChange = (info: any, loading: boolean) => {
    setVehicleInfo(info)
    setIsLoading(loading)
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Car className="h-10 w-10 text-primary mr-3" />
            <h1 className="text-3xl font-bold text-foreground">Vehicle Data Validator</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Enter your vehicle information and get real-time validation with intelligent auto-correction suggestions.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2">
            <EnhancedVehicleValidatorForm onVehicleInfoChange={handleVehicleInfoChange} />
          </div>

          {/* Vehicle Info Panel */}
          <div className="space-y-6">
            <VehicleInfoDisplay vehicleInfo={vehicleInfo} isLoading={isLoading} />
          </div>
        </div>
      </main>
    </div>
  )
}
