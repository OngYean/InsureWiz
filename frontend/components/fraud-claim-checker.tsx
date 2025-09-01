"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Upload,
  FileText,
  Scan,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Calendar,
  DollarSign,
  MapPin,
  User,
  Car,
  Clock,
} from "lucide-react"

interface ClaimData {
  claimId: string
  claimantName: string
  incidentDate: string
  location: string
  claimAmount: string
  vehicleInfo: string
  description: string
  uploadedFiles: File[]
}

interface FraudResult {
  status: "valid" | "suspicious" | "fraud"
  confidence: number
  riskScore: number
  flags: string[]
  recommendations: string[]
}

export function FraudClaimChecker() {
  const [claimData, setClaimData] = useState<ClaimData>({
    claimId: "",
    claimantName: "",
    incidentDate: "",
    location: "",
    claimAmount: "",
    vehicleInfo: "",
    description: "",
    uploadedFiles: [],
  })

  const [isScanning, setIsScanning] = useState(false)
  const [scanProgress, setScanProgress] = useState(0)
  const [result, setResult] = useState<FraudResult | null>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    setClaimData((prev) => ({ ...prev, uploadedFiles: [...prev.uploadedFiles, ...files] }))
  }

  const removeFile = (index: number) => {
    setClaimData((prev) => ({
      ...prev,
      uploadedFiles: prev.uploadedFiles.filter((_, i) => i !== index),
    }))
  }

  const analyzeClaim = (): FraudResult => {
    const flags: string[] = []
    let riskScore = 0

    // Simulate fraud detection logic
    const claimAmount = Number.parseFloat(claimData.claimAmount)

    // Check for high claim amounts
    if (claimAmount > 50000) {
      flags.push("Unusually high claim amount")
      riskScore += 30
    }

    // Check for recent incident dates (potential rush claims)
    const incidentDate = new Date(claimData.incidentDate)
    const daysSinceIncident = Math.floor((Date.now() - incidentDate.getTime()) / (1000 * 60 * 60 * 24))
    if (daysSinceIncident < 1) {
      flags.push("Claim filed very soon after incident")
      riskScore += 25
    }

    // Check for suspicious keywords in description
    const suspiciousKeywords = ["total loss", "stolen", "fire", "flood"]
    const description = claimData.description.toLowerCase()
    const foundKeywords = suspiciousKeywords.filter((keyword) => description.includes(keyword))
    if (foundKeywords.length > 1) {
      flags.push("Multiple high-risk incident types mentioned")
      riskScore += 20
    }

    // Check for missing information
    const requiredFields = [claimData.claimantName, claimData.location, claimData.vehicleInfo, claimData.description]
    const missingFields = requiredFields.filter((field) => !field.trim()).length
    if (missingFields > 0) {
      flags.push("Incomplete claim information")
      riskScore += 15
    }

    // Simulate duplicate detection
    if (claimData.claimId.includes("DUP") || claimData.description.includes("duplicate")) {
      flags.push("Potential duplicate claim detected")
      riskScore += 40
    }

    // Determine status based on risk score
    let status: "valid" | "suspicious" | "fraud"
    let confidence: number

    if (riskScore >= 60) {
      status = "fraud"
      confidence = Math.min(95, 70 + riskScore * 0.3)
    } else if (riskScore >= 30) {
      status = "suspicious"
      confidence = Math.min(85, 60 + riskScore * 0.4)
    } else {
      status = "valid"
      confidence = Math.max(80, 95 - riskScore * 0.5)
    }

    const recommendations: string[] = []
    if (status === "fraud") {
      recommendations.push("Recommend immediate investigation")
      recommendations.push("Flag for manual review")
      recommendations.push("Consider claim denial pending investigation")
    } else if (status === "suspicious") {
      recommendations.push("Request additional documentation")
      recommendations.push("Schedule adjuster inspection")
      recommendations.push("Verify claimant identity")
    } else {
      recommendations.push("Proceed with standard claim processing")
      recommendations.push("No additional verification required")
    }

    return {
      status,
      confidence: Math.round(confidence),
      riskScore,
      flags,
      recommendations,
    }
  }

  const handleScanClaim = async () => {
    setIsScanning(true)
    setScanProgress(0)
    setResult(null)

    // Simulate scanning progress
    const progressSteps = [
      { progress: 20, message: "Analyzing claim data..." },
      { progress: 40, message: "Checking for duplicates..." },
      { progress: 60, message: "Pattern recognition..." },
      { progress: 80, message: "Risk assessment..." },
      { progress: 100, message: "Generating report..." },
    ]

    for (const step of progressSteps) {
      await new Promise((resolve) => setTimeout(resolve, 800))
      setScanProgress(step.progress)
    }

    // Generate result
    const analysisResult = analyzeClaim()
    setResult(analysisResult)
    setIsScanning(false)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "valid":
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case "suspicious":
        return <AlertTriangle className="h-5 w-5 text-amber-500" />
      case "fraud":
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return null
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "valid":
        return "text-green-600 bg-green-50 border-green-200"
      case "suspicious":
        return "text-amber-600 bg-amber-50 border-amber-200"
      case "fraud":
        return "text-red-600 bg-red-50 border-red-200"
      default:
        return ""
    }
  }

  return (
    <div className="space-y-6">
      {/* Claim Input Form */}
      <Card className="border-border">
        <CardHeader>
          <CardTitle className="flex items-center text-xl">
            <FileText className="h-6 w-6 text-primary mr-2" />
            Claim Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="claimId" className="flex items-center">
                <FileText className="h-4 w-4 mr-1" />
                Claim ID
              </Label>
              <Input
                id="claimId"
                placeholder="CLM-2024-001"
                value={claimData.claimId}
                onChange={(e) => setClaimData({ ...claimData, claimId: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="claimantName" className="flex items-center">
                <User className="h-4 w-4 mr-1" />
                Claimant Name
              </Label>
              <Input
                id="claimantName"
                placeholder="John Doe"
                value={claimData.claimantName}
                onChange={(e) => setClaimData({ ...claimData, claimantName: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="incidentDate" className="flex items-center">
                <Calendar className="h-4 w-4 mr-1" />
                Incident Date
              </Label>
              <Input
                id="incidentDate"
                type="date"
                value={claimData.incidentDate}
                onChange={(e) => setClaimData({ ...claimData, incidentDate: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="claimAmount" className="flex items-center">
                <DollarSign className="h-4 w-4 mr-1" />
                Claim Amount
              </Label>
              <Input
                id="claimAmount"
                type="number"
                placeholder="15000"
                value={claimData.claimAmount}
                onChange={(e) => setClaimData({ ...claimData, claimAmount: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="location" className="flex items-center">
                <MapPin className="h-4 w-4 mr-1" />
                Incident Location
              </Label>
              <Input
                id="location"
                placeholder="123 Main St, City, State"
                value={claimData.location}
                onChange={(e) => setClaimData({ ...claimData, location: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="vehicleInfo" className="flex items-center">
                <Car className="h-4 w-4 mr-1" />
                Vehicle Information
              </Label>
              <Input
                id="vehicleInfo"
                placeholder="2020 Toyota Camry, License: ABC123"
                value={claimData.vehicleInfo}
                onChange={(e) => setClaimData({ ...claimData, vehicleInfo: e.target.value })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Incident Description</Label>
            <Textarea
              id="description"
              placeholder="Describe the incident in detail..."
              rows={4}
              value={claimData.description}
              onChange={(e) => setClaimData({ ...claimData, description: e.target.value })}
            />
          </div>

          {/* File Upload */}
          <div className="space-y-4">
            <Label className="flex items-center">
              <Upload className="h-4 w-4 mr-1" />
              Supporting Documents
            </Label>
            <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
              <Upload className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
              <p className="text-sm text-muted-foreground mb-2">
                Upload photos, police reports, or other supporting documents
              </p>
              <Input
                type="file"
                multiple
                accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <Button variant="outline" asChild>
                <label htmlFor="file-upload" className="cursor-pointer">
                  Choose Files
                </label>
              </Button>
            </div>

            {claimData.uploadedFiles.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium">Uploaded Files:</p>
                {claimData.uploadedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-2 bg-muted rounded">
                    <span className="text-sm">{file.name}</span>
                    <Button size="sm" variant="ghost" onClick={() => removeFile(index)}>
                      Remove
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <Button
            onClick={handleScanClaim}
            disabled={isScanning || !claimData.claimId || !claimData.claimantName}
            className="w-full"
            size="lg"
          >
            {isScanning ? (
              <>
                <Clock className="h-4 w-4 mr-2 animate-spin" />
                Scanning Claim...
              </>
            ) : (
              <>
                <Scan className="h-4 w-4 mr-2" />
                Analyze for Fraud
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Scanning Progress */}
      {isScanning && (
        <Card className="border-border">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Analyzing Claim</span>
                <span className="text-sm text-muted-foreground">{scanProgress}%</span>
              </div>
              <Progress value={scanProgress} className="w-full" />
              <div className="flex items-center justify-center space-x-2">
                <Scan className="h-4 w-4 text-primary animate-pulse" />
                <span className="text-sm text-muted-foreground">
                  {scanProgress < 40
                    ? "Analyzing claim data..."
                    : scanProgress < 60
                      ? "Checking for duplicates..."
                      : scanProgress < 80
                        ? "Pattern recognition..."
                        : "Generating report..."}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {result && (
        <Card className="border-border">
          <CardHeader>
            <CardTitle className="flex items-center text-xl">
              <Scan className="h-6 w-6 text-primary mr-2" />
              Fraud Analysis Results
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Status Badge */}
            <div className="flex items-center justify-center">
              <Badge className={`text-lg px-4 py-2 ${getStatusColor(result.status)}`}>
                {getStatusIcon(result.status)}
                <span className="ml-2 capitalize">{result.status}</span>
              </Badge>
            </div>

            {/* Confidence and Risk Score */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="text-center p-4 bg-muted/50 rounded-lg">
                <div className="text-2xl font-bold text-foreground">{result.confidence}%</div>
                <div className="text-sm text-muted-foreground">Confidence Level</div>
              </div>
              <div className="text-center p-4 bg-muted/50 rounded-lg">
                <div className="text-2xl font-bold text-foreground">{result.riskScore}</div>
                <div className="text-sm text-muted-foreground">Risk Score</div>
              </div>
            </div>

            {/* Flags */}
            {result.flags.length > 0 && (
              <div>
                <h4 className="font-medium text-sm mb-3">Detected Issues</h4>
                <div className="space-y-2">
                  {result.flags.map((flag, index) => (
                    <Alert key={index} className="border-l-4 border-l-amber-500">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertDescription>{flag}</AlertDescription>
                    </Alert>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            <div>
              <h4 className="font-medium text-sm mb-3">Recommendations</h4>
              <div className="space-y-2">
                {result.recommendations.map((recommendation, index) => (
                  <div key={index} className="flex items-start space-x-2 p-3 bg-muted/30 rounded-lg">
                    <CheckCircle className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{recommendation}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-center space-x-3">
              <Button variant="outline" onClick={() => setResult(null)}>
                Clear Results
              </Button>
              <Button>Generate Report</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
