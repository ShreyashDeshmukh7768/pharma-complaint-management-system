import { useEffect, useRef, useState } from 'react';
import type { ChangeEvent, DragEvent } from 'react';
import {
  Box,
  Button,
  Card,
  Chip,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadComplaint } from '../api/uploadApi';
import type { AIInsight } from '../types/complaint';

interface UploadPanelProps {
  onUpload?: (response: any) => void;
  insights?: AIInsight;
}

interface ChatMessage {
  sender: 'AI' | 'User';
  message: string;
  timestamp: string;
}

interface SummaryCardData {
  customer: string;
  product: string;
  category: string;
  risk: string;
  confidence: string;
}

const UploadPanel = ({ onUpload }: UploadPanelProps) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [draft, setDraft] = useState('');
  const [summary, setSummary] = useState<SummaryCardData | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: 'AI',
      message: 'Upload a complaint PDF or add context. I will extract and structure the key details for review.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const appendMessage = (message: string, sender: 'AI' | 'User' = 'AI') => {
    setMessages((prev) => [
      ...prev,
      {
        sender,
        message,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  };

  const processFile = async (file?: File | null) => {
    if (!file) {
      return;
    }

    try {
      setLoading(true);
      setError('');
      appendMessage('Document uploaded successfully.');
      appendMessage('Extracting complaint information...');

      const response = await uploadComplaint(file);
      onUpload?.(response);

      const extracted = response?.extracted_fields ?? {};
      const risk = response?.risk_assessment ?? {};
      const details: string[] = [];

      const nextSummary: SummaryCardData = {
        customer: extracted.customer_name || 'Not available',
        product: extracted.product_name || 'Not available',
        category: extracted.complaint_category || 'Pending',
        risk: String(risk.risk_level || 'Pending').toUpperCase(),
        confidence: risk.confidence_score ? `${risk.confidence_score}%` : 'N/A',
      };
      setSummary(nextSummary);

      if (extracted.customer_name) {
        details.push(`Customer identified: ${extracted.customer_name}`);
      }

      if (extracted.product_name) {
        details.push(`Product: ${extracted.product_name}`);
      }

      if (risk.risk_level) {
        details.push(`Risk Level: ${String(risk.risk_level).toUpperCase()}`);
      }

      if (details.length > 0) {
        details.forEach((detail) => appendMessage(detail));
      } else {
        appendMessage('I could not extract additional details from the uploaded document.');
      }
    } catch (err) {
      console.error(err);
      setError('Failed to upload and process the complaint.');
      appendMessage('I could not process the uploaded file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    await processFile(file);
  };

  const handleDrop = async (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    await processFile(file);
  };

  const handleSendMessage = () => {
    const trimmed = draft.trim();

    if (!trimmed) {
      return;
    }

    appendMessage(trimmed, 'User');
    setDraft('');
    appendMessage('I can help summarize the complaint, outline follow-up actions, or prepare a review note.');
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Card
      elevation={0}
      sx={{
        p: { xs: 2, md: 2.75 },
        border: '1px solid #e5e7eb',
        borderRadius: 4,
        boxShadow: '0 24px 60px -30px rgba(15, 23, 42, 0.3)',
        background: '#ffffff',
        height: '100%',
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 1, mb: 2 }}>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 700, color: '#0f172a' }}>
            AI Complaint Assistant
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Live extraction and review guidance
          </Typography>
        </Box>
        <Chip label="Live" size="small" color="primary" variant="outlined" sx={{ borderRadius: 999 }} />
      </Box>

      <Paper
        variant="outlined"
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
        sx={{
          p: { xs: 2.25, md: 2.75 },
          textAlign: 'center',
          borderStyle: 'dashed',
          borderColor: 'primary.main',
          backgroundColor: '#f8fbff',
          mb: 2.25,
          borderRadius: 3,
        }}
      >
        <CloudUploadIcon sx={{ fontSize: 42, color: 'primary.main', mb: 1 }} />
        <Typography variant="subtitle1" sx={{ mb: 0.75, fontWeight: 600 }}>
          Drag and drop a complaint PDF here
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Secure PDF intake for rapid extraction and review
        </Typography>
        <Button variant="contained" component="label" sx={{ borderRadius: 2.2 }}>
          Upload PDF
          <input hidden type="file" accept="application/pdf" onChange={handleFileChange} />
        </Button>
      </Paper>

      {summary && (
        <Card
          variant="outlined"
          sx={{
            mb: 1.5,
            borderRadius: 3,
            borderColor: '#dbeafe',
            background: 'linear-gradient(180deg, #ffffff 0%, #f8fbff 100%)',
          }}
        >
          <Box sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1.5 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#0f172a' }}>
                ✓ Complaint processed
              </Typography>
              <Chip
                label={summary.risk}
                color={summary.risk === 'HIGH' || summary.risk === 'CRITICAL' ? 'error' : summary.risk === 'MEDIUM' ? 'warning' : 'success'}
                size="small"
                sx={{ fontWeight: 700, borderRadius: 999 }}
              />
            </Box>

            <Stack spacing={1}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
                <Typography variant="body2" color="text.secondary">Customer</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, textAlign: 'right' }}>{summary.customer}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
                <Typography variant="body2" color="text.secondary">Product</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, textAlign: 'right' }}>{summary.product}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
                <Typography variant="body2" color="text.secondary">Category</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, textAlign: 'right' }}>{summary.category}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
                <Typography variant="body2" color="text.secondary">Risk</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, textAlign: 'right' }}>{summary.risk}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
                <Typography variant="body2" color="text.secondary">Confidence Score</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, textAlign: 'right' }}>{summary.confidence}</Typography>
              </Box>
            </Stack>
          </Box>
        </Card>
      )}

      <Box
        sx={{
          height: 240,
          overflowY: 'auto',
          border: '1px solid #e8edf5',
          borderRadius: 3,
          background: '#fcfdff',
          p: 2,
          mb: 1.5,
        }}
      >
        <Stack spacing={1.5}>
          {messages.map((message, index) => {
            const isUser = message.sender === 'User';

            return (
              <Box key={`${message.sender}-${index}`} sx={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start' }}>
                <Box
                  sx={{
                    maxWidth: '85%',
                    p: 1.5,
                    borderRadius: 2.2,
                    background: isUser ? '#2563eb' : '#ffffff',
                    color: isUser ? '#ffffff' : '#0f172a',
                    border: isUser ? '1px solid #2563eb' : '1px solid #e5e7eb',
                    boxShadow: '0 8px 20px -12px rgba(15, 23, 42, 0.28)',
                  }}
                >
                  <Typography variant="body2" sx={{ mb: 0.5, opacity: 0.8, fontSize: '0.75rem' }}>
                    {message.sender} • {message.timestamp}
                  </Typography>
                  <Typography variant="body2">{message.message}</Typography>
                </Box>
              </Box>
            );
          })}

          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start' }}>
              <Box sx={{ maxWidth: '85%', p: 1.5, borderRadius: 2.2, background: '#eef4ff', border: '1px solid #dbeafe' }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  AI • {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </Typography>
                <Typography variant="body2">Reviewing the uploaded complaint…</Typography>
              </Box>
            </Box>
          )}

          <div ref={messagesEndRef} />
        </Stack>
      </Box>

      <Paper
        variant="outlined"
        sx={{
          p: 1.25,
          borderRadius: 3,
          borderColor: '#dbeafe',
          backgroundColor: '#f8fbff',
          display: 'flex',
          alignItems: 'flex-end',
          gap: 1,
        }}
      >
        <TextField
          multiline
          minRows={2}
          maxRows={4}
          fullWidth
          placeholder="Ask the assistant..."
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          variant="outlined"
          size="small"
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 2.2,
              backgroundColor: '#ffffff',
            },
          }}
        />
        <Button variant="contained" onClick={handleSendMessage} sx={{ borderRadius: 2.2, px: 2.5, py: 1.2 }}>
          Send
        </Button>
      </Paper>

      {error && (
        <Typography color="error" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}
    </Card>
  );
};

export default UploadPanel;