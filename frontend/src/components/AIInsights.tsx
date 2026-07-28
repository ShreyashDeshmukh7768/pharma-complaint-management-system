import {
  Box,
  Card,
  Chip,
  Divider,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Stack,
  Typography,
} from "@mui/material";

import type { AIInsight } from "../types/complaint";

interface AIInsightsProps {
  insights: AIInsight;
}

const getRiskColor = (
  risk: string
): "success" | "warning" | "error" | "default" => {
  switch (risk.toUpperCase()) {
    case "LOW":
      return "success";

    case "MEDIUM":
      return "warning";

    case "HIGH":
    case "CRITICAL":
      return "error";

    default:
      return "default";
  }
};

const AIInsights = ({ insights }: AIInsightsProps) => {
  return (
    <Card
      elevation={0}
      sx={{
        p: 3,
        border: "1px solid #e5e7eb",
        borderRadius: 3,
      }}
    >
      <Typography
        variant="h6"
        sx={{
          fontWeight: 700,
          mb: 3,
        }}
      >
        AI Analysis
      </Typography>

      <Stack spacing={3}>
        <Box>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 1 }}
          >
            Complaint Summary
          </Typography>

          <Typography variant="body1">
            {insights.summary}
          </Typography>
        </Box>

        <Divider />

        <Box>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 1 }}
          >
            Complaint Category
          </Typography>

          <Chip
            label={insights.category}
            color="primary"
            variant="outlined"
          />
        </Box>

        <Divider />

        <Box>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 1 }}
          >
            Risk Level
          </Typography>

          <Chip
            label={insights.riskLevel}
            color={getRiskColor(insights.riskLevel)}
          />
        </Box>

        <Divider />

        <Box>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 1 }}
          >
            AI Confidence
          </Typography>

          <LinearProgress
            variant="determinate"
            value={insights.confidenceScore * 100}
            sx={{
              height: 10,
              borderRadius: 5,
              mb: 1,
            }}
          />

          <Typography variant="body2">
            {(insights.confidenceScore * 100).toFixed(0)}%
          </Typography>
        </Box>

        <Divider />

        <Box>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 1 }}
          >
            Recommended Actions
          </Typography>

          <List dense>
            {insights.recommendedActions.length > 0 ? (
              insights.recommendedActions.map((action, index) => (
                <ListItem key={index} disablePadding>
                  <ListItemText primary={`• ${action}`} />
                </ListItem>
              ))
            ) : (
              <Typography variant="body2">
                Awaiting AI analysis...
              </Typography>
            )}
          </List>
        </Box>
      </Stack>
    </Card>
  );
};

export default AIInsights;