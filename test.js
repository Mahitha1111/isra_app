import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ChevronLeft, ChevronRight, Upload } from 'lucide-react';

const DynamicPDFViewer = () => {
  // Initial form fields structure
  const formFields = [
    { id: 'formDate', label: 'Form Date', type: 'text' },
    { id: 'teamMember', label: 'Team Member', type: 'text' },
    { id: 'beneficiaryName', label: 'Beneficiary Name', type: 'text' },
    { id: 'gender', label: 'Gender', type: 'text' },
    { id: 'dob', label: 'DOB', type: 'text' },
    { id: 'area', label: 'Area', type: 'text' },
    { id: 'mobile', label: 'Mobile', type: 'text' },
    { id: 'religion', label: 'Religion', type: 'text' },
    { id: 'caste', label: 'Caste', type: 'text' },
    { id: 'occupation', label: 'Occupation', type: 'text' },
    { id: 'cardsApply', label: 'Cards Apply', type: 'text' },
    { id: 'schemeApply', label: 'Scheme Apply', type: 'text' },
    { id: 'familyIncome', label: 'Family Income', type: 'text' },
    { id: 'differentlyAbled', label: 'Differently Abled', type: 'text' },
    { id: 'proofOfEvidence', label: 'Proof of Evidence', type: 'text' }
  ];

  const [pdfData, setPdfData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    // Mock data extraction - replace with actual PDF parsing logic
    const extractedData = files.map((file, index) => {
      const dataObject = {};
      formFields.forEach(field => {
        dataObject[field.id] = ''; // Initialize with empty values
      });
      return dataObject;
    });
    
    setPdfData(extractedData);
    setCurrentIndex(0);
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < pdfData.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handleSave = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const updatedData = { ...pdfData[currentIndex] };
    
    formFields.forEach(field => {
      updatedData[field.id] = formData.get(field.id);
    });

    const newPdfData = [...pdfData];
    newPdfData[currentIndex] = updatedData;
    setPdfData(newPdfData);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>PDF Data Viewer</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <label className="block mb-2">
              <span className="sr-only">Choose PDFs</span>
              <div className="flex items-center gap-2 border rounded p-2 cursor-pointer hover:bg-gray-50">
                <Upload className="h-5 w-5" />
                <span>Upload PDFs</span>
                <Input
                  type="file"
                  accept=".pdf"
                  multiple
                  className="hidden"
                  onChange={handleFileUpload}
                />
              </div>
            </label>
          </div>

          {pdfData.length > 0 && (
            <div>
              <form onSubmit={handleSave} className="space-y-4">
                {formFields.map(field => (
                  <div key={field.id}>
                    <label className="block text-sm font-medium mb-1">
                      {field.label}
                    </label>
                    <Input
                      name={field.id}
                      type={field.type}
                      defaultValue={pdfData[currentIndex][field.id]}
                    />
                  </div>
                ))}
                
                <div className="flex justify-between items-center pt-4">
                  <Button 
                    type="button"
                    onClick={handlePrevious}
                    disabled={currentIndex === 0}
                    variant="outline"
                  >
                    <ChevronLeft className="h-4 w-4 mr-2" />
                    Previous
                  </Button>
                  
                  <span className="text-sm text-gray-500">
                    {currentIndex + 1} of {pdfData.length}
                  </span>
                  
                  <Button 
                    type="button"
                    onClick={handleNext}
                    disabled={currentIndex === pdfData.length - 1}
                    variant="outline"
                  >
                    Next
                    <ChevronRight className="h-4 w-4 ml-2" />
                  </Button>
                </div>
                
                <Button type="submit" className="w-full">
                  Save Changes
                </Button>
              </form>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default DynamicPDFViewer;
