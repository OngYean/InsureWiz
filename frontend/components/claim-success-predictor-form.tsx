"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  AlertCircle,
  CheckCircle,
  Clock,
  FileImage,
  MapPin,
  Target,
  TrendingUp,
  Upload,
  Car,
  Camera,
  FileText,
  Calendar,
  Users,
  X,
} from "lucide-react";

interface PredictionResult {
  successProbability: number;
  factors: {
    positive: string[];
    negative: string[];
    neutral: string[];
  };
  recommendations: string[];
  expectedTimeline: string;
  riskLevel: "low" | "medium" | "high";
}

export function ClaimSuccessPredictorForm() {
  const [currentStep, setCurrentStep] = useState(1);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [policyDocument, setPolicyDocument] = useState<File[]>([]);

  const [formData, setFormData] = useState({
    // Incident Details
    incidentType: "",
    incidentDate: "",
    incidentTime: "",
    weatherConditions: "",
    roadConditions: "",

    // Vehicle & Coverage
    vehicleAge: "",
    coverageType: "",
    hasNCD: "",

    // Evidence & Documentation
    policeReportFiled: "",
    policeReportTime: "",
    hasPhotos: "",
    hasWitnesses: "",
    witnessCount: "",

    // Damage Assessment
    damageExtent: "",
    estimatedCost: "",

    // Fault & Circumstances
    atFault: "",
    trafficViolation: "",
    previousClaims: "",

    // Description
    incidentDescription: "",
  });

  const totalSteps = 5;

  const updateFormData = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleFilesChange = (files: File[]) => {
    setUploadedFiles(files);
    if (files.length > 0) {
      updateFormData("hasPhotos", "yes");
    } else {
      updateFormData("hasPhotos", "no");
    }
  };

  const handlePolicyDocChange = (files: File[]) => {
    setPolicyDocument(files);
  };

  const handleSubmit = async () => {
    setIsLoading(true);

    const submissionData = new FormData();

    // Append policy document if it exists
    if (policyDocument.length > 0) {
      submissionData.append("policy_document", policyDocument[0]);
    }

    // Append evidence files
    uploadedFiles.forEach((file) => {
      submissionData.append("evidence_files", file);
    });

    // Append form data as a JSON string
    submissionData.append("form_data_json", JSON.stringify(formData));

    try {
      const response = await fetch("http://localhost:8000/advanced/claim", {
        method: "POST",
        body: submissionData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      // Mocking the transformation to the frontend's PredictionResult structure
      const transformedPrediction: PredictionResult = {
        successProbability: result.prediction,
        factors: {
          positive: result.key_factors.filter(
            (f: string) =>
              !f.toLowerCase().includes("loss") &&
              !f.toLowerCase().includes("injuries")
          ),
          negative: result.key_factors.filter(
            (f: string) =>
              f.toLowerCase().includes("loss") ||
              f.toLowerCase().includes("injuries")
          ),
          neutral: [],
        },
        recommendations: [
          "Submit claim as soon as possible.",
          "Ensure all details are accurate before final submission.",
        ],
        expectedTimeline: result.prediction > 70 ? "7-14 days" : "14-30 days",
        riskLevel:
          result.prediction > 80
            ? "low"
            : result.prediction > 60
            ? "medium"
            : "high",
      };

      setPrediction(transformedPrediction);
    } catch (error) {
      console.error("Error submitting form:", error);
      // Optionally, handle the error in the UI
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    } else {
      handleSubmit();
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const resetForm = () => {
    setCurrentStep(1);
    setPrediction(null);
    setUploadedFiles([]);
    setPolicyDocument([]);
    setFormData({
      incidentType: "",
      incidentDate: "",
      incidentTime: "",
      weatherConditions: "",
      roadConditions: "",
      vehicleAge: "",
      coverageType: "",
      hasNCD: "",
      policeReportFiled: "",
      policeReportTime: "",
      hasPhotos: "",
      hasWitnesses: "",
      witnessCount: "",
      damageExtent: "",
      estimatedCost: "",
      atFault: "",
      trafficViolation: "",
      previousClaims: "",
      incidentDescription: "",
    });
  };

  if (prediction) {
    return (
      <Card className="w-full">
        <CardHeader className="text-center">
          <CardTitle className="flex items-center justify-center text-2xl">
            <Target className="h-6 w-6 text-primary mr-2" />
            Claim Success Prediction
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Success Probability */}
          <div className="text-center">
            <div className="text-4xl font-bold mb-2">
              {prediction.successProbability}%
            </div>
            <div className="text-lg text-muted-foreground mb-4">
              Success Probability
            </div>
            <Progress value={prediction.successProbability} className="h-3" />
            <div className="mt-2">
              <Badge
                variant={
                  prediction.riskLevel === "low"
                    ? "default"
                    : prediction.riskLevel === "medium"
                    ? "secondary"
                    : "destructive"
                }
              >
                {prediction.riskLevel.toUpperCase()} RISK
              </Badge>
            </div>
          </div>

          {/* Expected Timeline */}
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <Clock className="h-6 w-6 text-blue-500 mx-auto mb-2" />
            <div className="font-medium">Expected Processing Time</div>
            <div className="text-lg text-blue-700">
              {prediction.expectedTimeline}
            </div>
          </div>

          {/* Factors Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Positive Factors */}
            {prediction.factors.positive.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-semibold text-green-700 flex items-center">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Positive Factors
                </h4>
                {prediction.factors.positive.map((factor, index) => (
                  <div
                    key={index}
                    className="text-sm p-2 bg-green-50 rounded border-l-4 border-green-500"
                  >
                    {factor}
                  </div>
                ))}
              </div>
            )}

            {/* Negative Factors */}
            {prediction.factors.negative.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-semibold text-red-700 flex items-center">
                  <AlertCircle className="h-4 w-4 mr-2" />
                  Risk Factors
                </h4>
                {prediction.factors.negative.map((factor, index) => (
                  <div
                    key={index}
                    className="text-sm p-2 bg-red-50 rounded border-l-4 border-red-500"
                  >
                    {factor}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recommendations */}
          <div className="space-y-2">
            <h4 className="font-semibold text-blue-700 flex items-center">
              <TrendingUp className="h-4 w-4 mr-2" />
              Recommendations
            </h4>
            {prediction.recommendations.map((rec, index) => (
              <div
                key={index}
                className="text-sm p-2 bg-blue-50 rounded border-l-4 border-blue-500"
              >
                {rec}
              </div>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 pt-4">
            <Button onClick={resetForm} variant="outline" className="flex-1">
              Check Another Claim
            </Button>
            <Button className="flex-1">Proceed to File Claim</Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Claim Success Predictor</span>
          <Badge variant="outline">
            Step {currentStep} of {totalSteps}
          </Badge>
        </CardTitle>
        <Progress value={(currentStep / totalSteps) * 100} className="mt-2" />
      </CardHeader>
      <CardContent className="space-y-6">
        {currentStep === 1 && (
          <div className="space-y-6">
            <div className="flex items-center mb-4">
              <Car className="h-5 w-5 text-primary mr-2" />
              <h3 className="text-lg font-semibold">Incident Details</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="incidentType">Type of Incident</Label>
                <Select
                  value={formData.incidentType}
                  onValueChange={(value) =>
                    updateFormData("incidentType", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select incident type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="collision">Vehicle Collision</SelectItem>
                    <SelectItem value="theft">Theft/Burglary</SelectItem>
                    <SelectItem value="vandalism">Vandalism</SelectItem>
                    <SelectItem value="natural-disaster">
                      Natural Disaster
                    </SelectItem>
                    <SelectItem value="fire">Fire</SelectItem>
                    <SelectItem value="windscreen">
                      Windscreen Damage
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="incidentDate">Incident Date</Label>
                <Input
                  id="incidentDate"
                  type="date"
                  value={formData.incidentDate}
                  onChange={(e) =>
                    updateFormData("incidentDate", e.target.value)
                  }
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="weatherConditions">Weather Conditions</Label>
                <Select
                  value={formData.weatherConditions}
                  onValueChange={(value) =>
                    updateFormData("weatherConditions", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select weather" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="clear">Clear</SelectItem>
                    <SelectItem value="rain">Rain</SelectItem>
                    <SelectItem value="heavy-rain">Heavy Rain</SelectItem>
                    <SelectItem value="fog">Fog</SelectItem>
                    <SelectItem value="night">Night Time</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="roadConditions">Road Conditions</Label>
                <Select
                  value={formData.roadConditions}
                  onValueChange={(value) =>
                    updateFormData("roadConditions", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select road condition" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dry">Dry</SelectItem>
                    <SelectItem value="wet">Wet</SelectItem>
                    <SelectItem value="construction">
                      Construction Zone
                    </SelectItem>
                    <SelectItem value="poor-visibility">
                      Poor Visibility
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        )}

        {currentStep === 2 && (
          <div className="space-y-6">
            <div className="flex items-center mb-4">
              <FileText className="h-5 w-5 text-primary mr-2" />
              <h3 className="text-lg font-semibold">
                Coverage & Vehicle Details
              </h3>
            </div>

            <div className="space-y-2">
              <Label htmlFor="policyDocument">
                Upload your Policy Document to be referenced by our AI:
              </Label>
              <FileUploader
                onFilesChange={handlePolicyDocChange}
                initialFiles={policyDocument}
                multiple={false}
                accept="application/pdf"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Insurance Coverage Type</Label>
                <RadioGroup
                  value={formData.coverageType}
                  onValueChange={(value) =>
                    updateFormData("coverageType", value)
                  }
                  className="grid grid-cols-2 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="comprehensive"
                      id="comprehensive"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="comprehensive"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Comprehensive
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="third-party"
                      id="third-party"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="third-party"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Third Party
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label htmlFor="vehicleAge">Vehicle Age</Label>
                <Select
                  value={formData.vehicleAge}
                  onValueChange={(value) => updateFormData("vehicleAge", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select vehicle age" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0-3">0-3 years</SelectItem>
                    <SelectItem value="4-7">4-7 years</SelectItem>
                    <SelectItem value="8-12">8-12 years</SelectItem>
                    <SelectItem value="13+">13+ years</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Do you have No Claims Discount (NCD)?</Label>
                <RadioGroup
                  value={formData.hasNCD}
                  onValueChange={(value) => updateFormData("hasNCD", value)}
                  className="grid grid-cols-2 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="yes"
                      id="ncd-yes"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="ncd-yes"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Yes
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="no"
                      id="ncd-no"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="ncd-no"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      No
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label htmlFor="previousClaims">
                  Previous Claims (last 3 years)
                </Label>
                <Select
                  value={formData.previousClaims}
                  onValueChange={(value) =>
                    updateFormData("previousClaims", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select number" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0">0 claims</SelectItem>
                    <SelectItem value="1">1 claim</SelectItem>
                    <SelectItem value="2">2 claims</SelectItem>
                    <SelectItem value="3+">3+ claims</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        )}

        {currentStep === 3 && (
          <div className="space-y-6">
            <div className="flex items-center mb-4">
              <Camera className="h-5 w-5 text-primary mr-2" />
              <h3 className="text-lg font-semibold">
                Documentation & Evidence
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Police Report Filed?</Label>
                <RadioGroup
                  value={formData.policeReportFiled}
                  onValueChange={(value) =>
                    updateFormData("policeReportFiled", value)
                  }
                  className="grid grid-cols-2 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="yes"
                      id="police-yes"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="police-yes"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Yes
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="no"
                      id="police-no"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="police-no"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      No
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              {formData.policeReportFiled === "yes" && (
                <div className="space-y-2">
                  <Label>When was police report filed?</Label>
                  <RadioGroup
                    value={formData.policeReportTime}
                    onValueChange={(value) =>
                      updateFormData("policeReportTime", value)
                    }
                    className="grid grid-cols-2 gap-4"
                  >
                    <div>
                      <RadioGroupItem
                        value="within-24h"
                        id="within-24h"
                        className="peer sr-only"
                      />
                      <Label
                        htmlFor="within-24h"
                        className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                      >
                        Within 24 hours
                      </Label>
                    </div>
                    <div>
                      <RadioGroupItem
                        value="after-24h"
                        id="after-24h"
                        className="peer sr-only"
                      />
                      <Label
                        htmlFor="after-24h"
                        className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                      >
                        After 24 hours
                      </Label>
                    </div>
                  </RadioGroup>
                </div>
              )}

              <div className="space-y-2">
                <Label>Are there witnesses?</Label>
                <RadioGroup
                  value={formData.hasWitnesses}
                  onValueChange={(value) =>
                    updateFormData("hasWitnesses", value)
                  }
                  className="grid grid-cols-2 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="yes"
                      id="witnesses-yes"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="witnesses-yes"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Yes
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="no"
                      id="witnesses-no"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="witnesses-no"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      No
                    </Label>
                  </div>
                </RadioGroup>
              </div>
            </div>
          </div>
        )}

        {currentStep === 4 && (
          <div className="space-y-6">
            <div className="flex items-center mb-4">
              <Upload className="h-5 w-5 text-primary mr-2" />
              <h3 className="text-lg font-semibold">Upload Evidence</h3>
            </div>

            <div className="p-4 border-l-4 border-amber-500 bg-amber-50 rounded-r-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <AlertCircle className="h-5 w-5 text-amber-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-amber-800">
                    <strong>Privacy Notice:</strong> Do not upload documents
                    containing sensitive personal information like your full
                    NRIC or home address. Photos of your car (including plate
                    number) and damage are acceptable.
                  </p>
                </div>
              </div>
            </div>

            <FileUploader
              onFilesChange={handleFilesChange}
              initialFiles={uploadedFiles}
            />
          </div>
        )}

        {currentStep === 5 && (
          <div className="space-y-6">
            <div className="flex items-center mb-4">
              <AlertCircle className="h-5 w-5 text-primary mr-2" />
              <h3 className="text-lg font-semibold">
                Fault & Damage Assessment
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Are you at fault?</Label>
                <RadioGroup
                  value={formData.atFault}
                  onValueChange={(value) => updateFormData("atFault", value)}
                  className="grid grid-cols-3 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="yes"
                      id="fault-yes"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="fault-yes"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Yes
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="no"
                      id="fault-no"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="fault-no"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      No
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="partial"
                      id="fault-partial"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="fault-partial"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Partially
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label>Any traffic violation involved?</Label>
                <RadioGroup
                  value={formData.trafficViolation}
                  onValueChange={(value) =>
                    updateFormData("trafficViolation", value)
                  }
                  className="grid grid-cols-2 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="yes"
                      id="violation-yes"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="violation-yes"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Yes
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="no"
                      id="violation-no"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="violation-no"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      No
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label htmlFor="damageExtent">Extent of Damage</Label>
                <Select
                  value={formData.damageExtent}
                  onValueChange={(value) =>
                    updateFormData("damageExtent", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select damage extent" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="minor">
                      Minor (scratches, dents)
                    </SelectItem>
                    <SelectItem value="moderate">
                      Moderate (body damage)
                    </SelectItem>
                    <SelectItem value="major">
                      Major (structural damage)
                    </SelectItem>
                    <SelectItem value="total-loss">Total Loss</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="estimatedCost">
                  Estimated Repair Cost (RM)
                </Label>
                <Select
                  value={formData.estimatedCost}
                  onValueChange={(value) =>
                    updateFormData("estimatedCost", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select cost range" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="under-1000">Under RM 1,000</SelectItem>
                    <SelectItem value="1000-5000">RM 1,000 - 5,000</SelectItem>
                    <SelectItem value="5000-15000">
                      RM 5,000 - 15,000
                    </SelectItem>
                    <SelectItem value="15000-30000">
                      RM 15,000 - 30,000
                    </SelectItem>
                    <SelectItem value="over-30000">Over RM 30,000</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="incidentDescription">
                Brief Description of Incident (Optional)
              </Label>
              <Textarea
                id="incidentDescription"
                placeholder="Provide a brief description of what happened..."
                value={formData.incidentDescription}
                onChange={(e) =>
                  updateFormData("incidentDescription", e.target.value)
                }
                className="min-h-[100px]"
              />
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between pt-6">
          <Button
            onClick={prevStep}
            variant="outline"
            disabled={currentStep === 1}
          >
            Previous
          </Button>

          <Button onClick={nextStep} disabled={isLoading}>
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Analyzing...
              </>
            ) : currentStep === totalSteps ? (
              "Get Prediction"
            ) : (
              "Next"
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

const FileUploader = ({
  onFilesChange,
  initialFiles,
  multiple = true,
  accept = "image/jpeg,image/png,application/pdf",
}: {
  onFilesChange: (files: File[]) => void;
  initialFiles: File[];
  multiple?: boolean;
  accept?: string;
}) => {
  const [files, setFiles] = useState<File[]>(initialFiles || []);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const newFiles = Array.from(event.target.files);
      const updatedFiles = multiple ? [...files, ...newFiles] : newFiles;
      setFiles(updatedFiles);
      onFilesChange(updatedFiles);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const newFiles = Array.from(event.dataTransfer.files);
    const updatedFiles = multiple
      ? [...files, ...newFiles]
      : newFiles.slice(0, 1);
    setFiles(updatedFiles);
    onFilesChange(updatedFiles);
  };

  const removeFile = (index: number) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    setFiles(updatedFiles);
    onFilesChange(updatedFiles);
  };

  return (
    <div className="space-y-4">
      <div
        className="border-2 border-dashed border-muted-foreground rounded-lg p-6 text-center cursor-pointer hover:border-primary transition-colors"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <Upload className="mx-auto h-10 w-10 text-muted-foreground" />
        <p className="mt-2 text-sm text-muted-foreground">
          Drag & drop files here, or click to select files
        </p>
        <p className="mt-1 text-xs text-muted-foreground">
          Supported formats: JPG, PNG, PDF. Max 5MB each.
        </p>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
          multiple={multiple}
          accept={accept}
        />
      </div>
      {files.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-medium">Uploaded Files:</h4>
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-2 bg-muted rounded-lg text-sm"
            >
              <div className="flex items-center space-x-2 overflow-hidden">
                <FileImage className="h-5 w-5 flex-shrink-0" />
                <span className="truncate">{file.name}</span>
                <span className="text-muted-foreground text-xs">
                  ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </span>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={() => removeFile(index)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
