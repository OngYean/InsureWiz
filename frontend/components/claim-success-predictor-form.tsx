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
  Loader2,
  Sparkles,
} from "lucide-react";
import Speedometer from "./speedometer";

interface PredictionResult {
  prediction: number;
  confidence: number;
  key_factors: string[];
  ai_insights: string;
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
    timeOfDay: "",
    roadConditions: "",
    weatherConditions: "",
    injuries: "no",

    // Vehicle & Documentation
    thirdPartyVehicle: "no",
    witnesses: "no",
    policeReport: "no",
    policeReportFiledWithin24h: 0,
    trafficViolation: 0,
    previousClaims: 0,
    description: "",
  });

  const totalSteps = 5;

  const updateFormData = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleFilesChange = (files: File[]) => {
    setUploadedFiles(files);
  };

  const handlePolicyDocChange = (files: File[]) => {
    setPolicyDocument(files);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault(); // Prevent default form submission
    setIsLoading(true);
    setPrediction(null);

    const submissionData = new FormData();

    // Append policy document if it exists
    if (policyDocument.length > 0) {
      submissionData.append("policy_document", policyDocument[0]);
    } else {
      // Add a placeholder if no file is selected, to prevent backend errors
      submissionData.append("policy_document", new Blob(), "placeholder.pdf");
    }

    // Append evidence files
    if (uploadedFiles.length > 0) {
      uploadedFiles.forEach((file) => {
        submissionData.append("evidence_files", file);
      });
    } else {
      // Add a placeholder if no files are selected
      submissionData.append("evidence_files", new Blob(), "placeholder.png");
    }

    // Convert form data values to match model expectations
    const processedFormData = {
      ...formData,
      policeReportFiledWithin24h:
        formData.policeReport === "yes" && formData.policeReportFiledWithin24h
          ? 1
          : 0,
      trafficViolation: formData.trafficViolation,
    };

    submissionData.append("form_data_json", JSON.stringify(processedFormData));

    try {
      const response = await fetch("http://localhost:8000/advanced/claim", {
        method: "POST",
        body: submissionData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setPrediction(result);
    } catch (error) {
      console.error("Error submitting form:", error);
      // Display an error message to the user
      setPrediction({
        prediction: 0,
        confidence: 0,
        key_factors: [
          "An error occurred while fetching the prediction. Please try again.",
        ],
        ai_insights: "Could not generate AI insights due to an error.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
    // The form will be submitted via the button's onClick, not here.
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
      timeOfDay: "",
      roadConditions: "",
      weatherConditions: "",
      injuries: "no",
      thirdPartyVehicle: "no",
      witnesses: "no",
      policeReport: "no",
      policeReportFiledWithin24h: 0,
      trafficViolation: 0,
      previousClaims: 0,
      description: "",
    });
  };

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
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
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
                      <SelectItem value="Collision">
                        Vehicle Collision
                      </SelectItem>
                      <SelectItem value="Theft">Theft/Burglary</SelectItem>
                      <SelectItem value="Vandalism">Vandalism</SelectItem>
                      <SelectItem value="Natural Disaster">
                        Natural Disaster
                      </SelectItem>
                      <SelectItem value="Fire">Fire</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="timeOfDay">Time of Day</Label>
                  <Select
                    value={formData.timeOfDay}
                    onValueChange={(value) =>
                      updateFormData("timeOfDay", value)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select time" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Morning">Morning</SelectItem>
                      <SelectItem value="Afternoon">Afternoon</SelectItem>
                      <SelectItem value="Evening">Evening</SelectItem>
                      <SelectItem value="Night">Night</SelectItem>
                    </SelectContent>
                  </Select>
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
                      <SelectItem value="Clear">Clear</SelectItem>
                      <SelectItem value="Rain">Rain</SelectItem>
                      <SelectItem value="Heavy Rain">Heavy Rain</SelectItem>
                      <SelectItem value="Fog">Fog</SelectItem>
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
                      <SelectItem value="Dry">Dry</SelectItem>
                      <SelectItem value="Wet">Wet</SelectItem>
                      <SelectItem value="Construction Zone">
                        Construction Zone
                      </SelectItem>
                      <SelectItem value="Poor Visibility">
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
                <h3 className="text-lg font-semibold">Policy and Vehicle</h3>
              </div>

              <div className="space-y-2">
                <Label htmlFor="policyDocument">
                  Upload your Policy Document (Optional)
                </Label>
                <FileUploader
                  onFilesChange={handlePolicyDocChange}
                  initialFiles={policyDocument}
                  multiple={false}
                  accept="application/pdf"
                />
              </div>

              <div className="space-y-2">
                <Label>Any Injuries?</Label>
                <RadioGroup
                  value={formData.injuries}
                  onValueChange={(value) => updateFormData("injuries", value)}
                  className="grid grid-cols-2 gap-4"
                >
                  <div>
                    <RadioGroupItem
                      value="yes"
                      id="injuries-yes"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="injuries-yes"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      Yes
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem
                      value="no"
                      id="injuries-no"
                      className="peer sr-only"
                    />
                    <Label
                      htmlFor="injuries-no"
                      className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                    >
                      No
                    </Label>
                  </div>
                </RadioGroup>
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-6">
              <div className="flex items-center mb-4">
                <Users className="h-5 w-5 text-primary mr-2" />
                <h3 className="text-lg font-semibold">Parties Involved</h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Third-party vehicle involved?</Label>
                  <RadioGroup
                    value={formData.thirdPartyVehicle}
                    onValueChange={(value) =>
                      updateFormData("thirdPartyVehicle", value)
                    }
                    className="grid grid-cols-2 gap-4"
                  >
                    <div>
                      <RadioGroupItem
                        value="yes"
                        id="tp-yes"
                        className="peer sr-only"
                      />
                      <Label
                        htmlFor="tp-yes"
                        className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                      >
                        Yes
                      </Label>
                    </div>
                    <div>
                      <RadioGroupItem
                        value="no"
                        id="tp-no"
                        className="peer sr-only"
                      />
                      <Label
                        htmlFor="tp-no"
                        className="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-primary/10 hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                      >
                        No
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                <div className="space-y-2">
                  <Label>Are there witnesses?</Label>
                  <RadioGroup
                    value={formData.witnesses}
                    onValueChange={(value) =>
                      updateFormData("witnesses", value)
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
                <Camera className="h-5 w-5 text-primary mr-2" />
                <h3 className="text-lg font-semibold">
                  Documentation & Evidence
                </h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Police Report Filed?</Label>
                  <RadioGroup
                    value={formData.policeReport}
                    onValueChange={(value) =>
                      updateFormData("policeReport", value)
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

                {formData.policeReport === "yes" && (
                  <div className="space-y-2">
                    <Label>When was police report filed?</Label>
                    <RadioGroup
                      value={
                        formData.policeReportFiledWithin24h === 1 ? "yes" : "no"
                      }
                      onValueChange={(value) =>
                        updateFormData(
                          "policeReportFiledWithin24h",
                          value === "yes" ? 1 : 0
                        )
                      }
                      className="grid grid-cols-2 gap-4"
                    >
                      <div>
                        <RadioGroupItem
                          value="yes"
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
                          value="no"
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
              </div>

              <div className="p-4 border-l-4 border-amber-500 bg-amber-50 rounded-r-lg">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <AlertCircle className="h-5 w-5 text-amber-600" />
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-amber-800">
                      <strong>Privacy Notice:</strong> Do not upload documents
                      containing sensitive personal information. Photos of your
                      car damage are sufficient.
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
                <h3 className="text-lg font-semibold">Circumstances</h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="trafficViolation">
                    Any traffic violation involved?
                  </Label>
                  <RadioGroup
                    value={formData.trafficViolation === 1 ? "yes" : "no"}
                    onValueChange={(value) =>
                      updateFormData(
                        "trafficViolation",
                        value === "yes" ? 1 : 0
                      )
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
                  <Label htmlFor="previousClaims">
                    Previous Claims (last 3 years)
                  </Label>
                  <Select
                    value={String(formData.previousClaims)}
                    onValueChange={(value) =>
                      updateFormData("previousClaims", parseInt(value))
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select number" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">0 claims</SelectItem>
                      <SelectItem value="1">1 claim</SelectItem>
                      <SelectItem value="2">2 claims</SelectItem>
                      <SelectItem value="3">3+ claims</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">
                  Brief Description of Incident
                </Label>
                <Textarea
                  id="description"
                  placeholder="Provide a brief description of what happened..."
                  value={formData.description}
                  onChange={(e) =>
                    updateFormData("description", e.target.value)
                  }
                  className="min-h-[100px]"
                />
              </div>
            </div>
          )}

          {/* Navigation and Submission */}
          <div className="flex justify-between pt-6">
            <Button
              type="button"
              onClick={prevStep}
              variant="outline"
              disabled={currentStep === 1 || isLoading}
            >
              Previous
            </Button>

            {currentStep < totalSteps ? (
              <Button type="button" onClick={nextStep}>
                Next
              </Button>
            ) : (
              <Button type="submit" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  "Get Prediction"
                )}
              </Button>
            )}
          </div>
        </form>

        {/* Prediction Result Section */}
        {isLoading && !prediction && (
          <div className="text-center p-8">
            <Loader2 className="mx-auto h-12 w-12 animate-spin text-primary" />
            <p className="mt-4 text-muted-foreground">
              Analyzing your claim details...
            </p>
          </div>
        )}

        {prediction && !isLoading && (
          <div className="pt-8 space-y-6">
            <div className="flex flex-col items-center justify-center">
              <Speedometer value={prediction.prediction} />
            </div>

            {prediction.ai_insights && (
              <div className="space-y-2 p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                <h4 className="font-semibold text-purple-800 flex items-center">
                  <Sparkles className="h-5 w-5 mr-2" />
                  AI-Powered Insights
                </h4>
                <p className="text-sm text-purple-700">
                  {prediction.ai_insights}
                </p>
              </div>
            )}

            <div className="space-y-2">
              <h4 className="font-semibold text-blue-700 flex items-center">
                <TrendingUp className="h-4 w-4 mr-2" />
                Key Factors
              </h4>
              {prediction.key_factors.map((factor, index) => (
                <div
                  key={index}
                  className="text-sm p-2 bg-blue-50 rounded border-l-4 border-blue-500"
                >
                  {factor}
                </div>
              ))}
            </div>

            <div className="flex gap-4 pt-4">
              <Button onClick={resetForm} variant="outline" className="flex-1">
                Check Another Claim
              </Button>
            </div>
          </div>
        )}
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
