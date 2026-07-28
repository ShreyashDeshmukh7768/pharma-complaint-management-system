import {
  Box,
  Button,
  Card,
  Divider,
  Grid,
  MenuItem,
  TextField,
  Typography,
} from '@mui/material';
import type { ChangeEvent, ReactNode } from 'react';
import type { ComplaintData } from '../types/complaint';

interface ComplaintFormProps {
  complaintData: ComplaintData;
  onFieldChange: (field: keyof ComplaintData, value: string) => void;
  onSave: () => void;
  highlightedFields?: Partial<Record<keyof ComplaintData, boolean>>;
}

const ComplaintForm = ({ complaintData, onFieldChange, onSave, highlightedFields = {} }: ComplaintFormProps) => {
  const renderField = (field: keyof ComplaintData, label: string, options?: { type?: string; select?: boolean; multiline?: boolean; minRows?: number; helperText?: string; }) => {
    const isHighlighted = Boolean(highlightedFields[field]);
    const commonProps = {
      fullWidth: true,
      label,
      value: complaintData[field],
      onChange: (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => onFieldChange(field, event.target.value),
      helperText: options?.helperText,
      sx: {
        '& .MuiOutlinedInput-root': {
          backgroundColor: isHighlighted ? '#f8fbff' : 'transparent',
          borderRadius: 2.2,
        },
      },
    };

    if (options?.select) {
      return (
        <TextField
          {...commonProps}
          select
          value={complaintData[field]}
          onChange={(event) => onFieldChange(field, event.target.value)}
        >
          {options?.helperText ? null : null}
        </TextField>
      );
    }

    return (
      <TextField
        {...commonProps}
        type={options?.type}
        multiline={options?.multiline}
        minRows={options?.minRows}
        slotProps={options?.type === 'date' ? { inputLabel: { shrink: true } } : undefined}
      />
    );
  };

  const renderSection = (title: string, children: ReactNode) => (
    <Box
      sx={{
        mb: 2.5,
        p: { xs: 2, md: 2.5 },
        border: '1px solid #e2e8f0',
        borderRadius: 3.25,
        background: 'linear-gradient(180deg, #ffffff 0%, #fcfdff 100%)',
        boxShadow: '0 14px 36px -24px rgba(15, 23, 42, 0.24)',
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#0f172a' }}>
          {title}
        </Typography>
        <Box sx={{ flexGrow: 1, height: 1, borderBottom: '1px solid #e5e7eb' }} />
      </Box>
      <Grid container spacing={2.25}>
        {children}
      </Grid>
    </Box>
  );

  return (
    <Card
      elevation={0}
      sx={{
        p: { xs: 2, md: 3.25 },
        border: '1px solid #e5e7eb',
        borderRadius: 4,
        boxShadow: '0 24px 60px -30px rgba(15, 23, 42, 0.3)',
        background: '#ffffff',
      }}
    >
      <Typography variant="h4" sx={{ mb: 0.75, fontWeight: 700, color: '#0f172a' }}>
        Complaint Intake
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2.25, maxWidth: 720 }}>
        Capture and triage pharmaceutical complaints with a focused, AI-ready workflow that keeps the review process clear and professional.
      </Typography>

      <Divider sx={{ mb: 2.75, borderColor: '#e5e7eb' }} />

      {renderSection('1. Customer Information', (
        <>
          <Grid size={{ xs: 12, md: 6 }}>
            {renderField('customerName', 'Customer Name', { helperText: highlightedFields.customerName ? 'AI extracted. Please verify.' : undefined })}
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            {renderField('email', 'Email', { type: 'email', helperText: highlightedFields.email ? 'AI extracted. Please verify.' : undefined })}
          </Grid>
        </>
      ))}

      {renderSection('2. Product Information', (
        <>
          <Grid size={{ xs: 12, md: 6 }}>
            {renderField('productName', 'Product Name', { helperText: highlightedFields.productName ? 'AI extracted. Please verify.' : undefined })}
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            {renderField('batchNumber', 'Batch Number', { helperText: highlightedFields.batchNumber ? 'AI extracted. Please verify.' : undefined })}
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            {renderField('manufacturingDate', 'Manufacturing Date', { type: 'date', helperText: highlightedFields.manufacturingDate ? 'AI extracted. Please verify.' : undefined })}
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            {renderField('expiryDate', 'Expiry Date', { type: 'date', helperText: highlightedFields.expiryDate ? 'AI extracted. Please verify.' : undefined })}
          </Grid>
        </>
      ))}

      {renderSection('3. Complaint Details', (
        <>
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              select
              label="Complaint Category"
              value={complaintData.complaintType}
              onChange={(event) => onFieldChange('complaintType', event.target.value)}
              helperText={highlightedFields.complaintType ? 'AI extracted. Please verify.' : undefined}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: highlightedFields.complaintType ? '#f8fbff' : 'transparent',
                  borderRadius: 2.2,
                },
              }}
            >
              <MenuItem value="Product Quality">Product Quality</MenuItem>
              <MenuItem value="Packaging">Packaging</MenuItem>
              <MenuItem value="Delivery">Delivery</MenuItem>
              <MenuItem value="Labeling">Labeling</MenuItem>
            </TextField>
          </Grid>
          <Grid size={{ xs: 12 }}>
            {renderField('complaintDescription', 'Complaint Description', {
              multiline: true,
              minRows: 4,
              helperText: highlightedFields.complaintDescription ? 'AI extracted. Please verify.' : undefined,
            })}
          </Grid>
        </>
      ))}

      {renderSection('4. Review & Priority', (
        <>
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              select
              label="Risk Level"
              value={complaintData.severity}
              onChange={(event) => onFieldChange('severity', event.target.value)}
              helperText={highlightedFields.severity ? 'AI extracted. Please verify.' : undefined}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: highlightedFields.severity ? '#f8fbff' : 'transparent',
                  borderRadius: 2.2,
                },
              }}
            >
              <MenuItem value="Low">Low</MenuItem>
              <MenuItem value="Medium">Medium</MenuItem>
              <MenuItem value="High">High</MenuItem>
              <MenuItem value="Critical">Critical</MenuItem>
            </TextField>
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              select
              label="Priority"
              value={complaintData.priority}
              onChange={(event) => onFieldChange('priority', event.target.value)}
              helperText={highlightedFields.priority ? 'AI extracted. Please verify.' : undefined}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: highlightedFields.priority ? '#f8fbff' : 'transparent',
                  borderRadius: 2.2,
                },
              }}
            >
              <MenuItem value="Low">Low</MenuItem>
              <MenuItem value="Medium">Medium</MenuItem>
              <MenuItem value="High">High</MenuItem>
              <MenuItem value="Urgent">Urgent</MenuItem>
            </TextField>
          </Grid>
        </>
      ))}

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2.25 }}>
        <Button variant="contained" size="large" onClick={onSave} sx={{ px: 3, py: 1.2, borderRadius: 2.2 }}>
          Save Complaint
        </Button>
      </Box>
    </Card>
  );
};

export default ComplaintForm;
