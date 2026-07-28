import { useState } from "react";
import { Box, Container, Grid, Paper, Typography } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";

import Header from "./components/Header";
import ComplaintForm from "./components/ComplaintForm";
import UploadPanel from "./components/UploadPanel";
import AIInsights from "./components/AIInsights";

import { saveComplaint } from "./api/complaintApi";

import type { ComplaintData, AIInsight } from "./types/complaint";

const initialComplaintData: ComplaintData = {
  complaintSource: "Email",
  customerName: "",
  email: "",
  productName: "",
  productStrength: "",
  batchNumber: "",
  manufacturingDate: "",
  expiryDate: "",
  quantityAffected: "",
  complaintType: "Product Quality",
  complaintDate: "",
  complaintDescription: "",
  severity: "Medium",
  priority: "Medium",
};

const initialInsights: AIInsight = {
  summary: "Awaiting PDF analysis",
  category: "Pending",
  riskLevel: "Pending",
  confidenceScore: 0,
  recommendedActions: [],
};

const theme = createTheme({
  palette: {
    primary: {
      main: "#2563eb",
    },
    secondary: {
      main: "#0f172a",
    },
  },
  shape: {
    borderRadius: 16,
  },
  typography: {
    fontFamily: "Inter, Roboto, Arial, sans-serif",
  },
});

const categoryMap: Record<string, string> = {
  PRODUCT_QUALITY: "Product Quality",
  PACKAGING: "Packaging",
  LABELING: "Labeling",
  CONTAMINATION: "Contamination",
  STABILITY: "Stability",
  ADVERSE_EVENT: "Adverse Event",
  OTHER: "Other",
};

const App = () => {
  const [complaintData, setComplaintData] =
    useState<ComplaintData>(initialComplaintData);

  const [insights, setInsights] =
    useState<AIInsight>(initialInsights);

  const [highlightedFields, setHighlightedFields] =
    useState<Partial<Record<keyof ComplaintData, boolean>>>({});

  const handleFieldChange = (
    field: keyof ComplaintData,
    value: string
  ) => {
    setComplaintData((prev) => ({
      ...prev,
      [field]: value,
    }));

    setHighlightedFields((prev) => ({
      ...prev,
      [field]: false,
    }));
  };

  const handleUpload = (response: any) => {
    if (!response?.extracted_fields) return;

    const extracted = response.extracted_fields;
    const analysis = response.analysis;

    setComplaintData((prev) => ({
      ...prev,
      customerName: extracted.customer_name ?? "",
      email: extracted.customer_email ?? "",
      productName: extracted.product_name ?? "",
      batchNumber: extracted.batch_number ?? "",
      manufacturingDate: extracted.manufacturing_date ?? "",
      expiryDate: extracted.expiry_date ?? "",
      complaintDescription:
        extracted.complaint_description ?? "",
      complaintDate: extracted.received_date ?? "",
      complaintType:
        categoryMap[extracted.complaint_category] ??
        "Product Quality",
    }));

    setHighlightedFields({
      customerName: Boolean(extracted.customer_name),
      email: Boolean(extracted.customer_email),
      productName: Boolean(extracted.product_name),
      batchNumber: Boolean(extracted.batch_number),
      manufacturingDate: Boolean(
        extracted.manufacturing_date
      ),
      expiryDate: Boolean(extracted.expiry_date),
      complaintDescription: Boolean(
        extracted.complaint_description
      ),
      complaintDate: Boolean(extracted.received_date),
      complaintType: Boolean(
        extracted.complaint_category
      ),
    });

    if (analysis) {
      setInsights({
        summary: analysis.summary ?? "",
        category: extracted.complaint_category ?? "Unknown",
        riskLevel: analysis.risk_level ?? "Pending",
        confidenceScore:
          analysis.confidence_score ?? 0,
        recommendedActions:
          analysis.recommended_actions ?? [],
      });
    }
  };

  const handleSaveComplaint = async () => {
    try {
      await saveComplaint(complaintData);

      setInsights({
        summary: "Complaint saved successfully.",
        category: complaintData.complaintType,
        riskLevel: complaintData.severity,
        confidenceScore: 1,
        recommendedActions: [],
      });
    } catch (error) {
      console.error(error);

      setInsights({
        summary: "Unable to save complaint.",
        category: "Error",
        riskLevel: "Unknown",
        confidenceScore: 0,
        recommendedActions: [],
      });
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          minHeight: "100vh",
          bgcolor: "#f4f7fb",
        }}
      >
        <Header />

        <Container
          maxWidth="xl"
          sx={{ py: 4 }}
        >
          <Paper
            elevation={0}
            sx={{
              p: 3,
              mb: 3,
              borderRadius: 4,
              border: "1px solid #e2e8f0",
            }}
          >
            <Typography
              variant="overline"
              color="primary"
            >
              Enterprise Pharmaceutical QMS
            </Typography>

            <Typography
              variant="h4"
              sx={{ mb: 1, fontWeight: 700 }}
            >
              AI Complaint Management System
            </Typography>

            <Typography color="text.secondary">
              Upload a pharmaceutical complaint and let AI
              automatically extract information, assess
              risk, and populate the complaint form.
            </Typography>
          </Paper>

          <Grid container spacing={3}>
            <Grid size={{ xs: 12, lg: 8 }}>
              <ComplaintForm
                complaintData={complaintData}
                onFieldChange={handleFieldChange}
                onSave={handleSaveComplaint}
                highlightedFields={highlightedFields}
              />
            </Grid>

            <Grid size={{ xs: 12, lg: 4 }}>
              <UploadPanel
                onUpload={handleUpload}
                insights={insights}
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3 }}>
            <AIInsights insights={insights} />
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default App;