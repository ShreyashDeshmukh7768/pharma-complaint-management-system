export interface ComplaintData {
  complaintSource: string;
  customerName: string;
  email: string;
  productName: string;
  productStrength: string;
  batchNumber: string;
  manufacturingDate: string;
  expiryDate: string;
  quantityAffected: string;
  complaintType: string;
  complaintDate: string;
  complaintDescription: string;
  severity: string;
  priority: string;
}

export interface AIInsight {
  summary: string;
  category: string;
  riskLevel: string;
  confidenceScore: number;
  recommendedActions: string[];
}