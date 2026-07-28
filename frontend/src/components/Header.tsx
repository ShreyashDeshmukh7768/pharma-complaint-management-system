import { AppBar, Box, Chip, Toolbar, Typography } from '@mui/material';

const Header = () => {
  return (
    <AppBar
      position="static"
      color="transparent"
      elevation={0}
      sx={{
        borderBottom: '1px solid #e2e8f0',
        background: 'rgba(248, 250, 252, 0.86)',
        backdropFilter: 'blur(16px)',
      }}
    >
      <Toolbar sx={{ px: { xs: 2, md: 4 }, py: { xs: 1.25, md: 1.6 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', gap: 2 }}>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 700, color: '#0f172a', lineHeight: 1.2 }}>
              Complaint Intake Console
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.25 }}>
              AI-powered pharmaceutical complaint intake and triage
            </Typography>
          </Box>
          <Chip label="Live review" color="primary" variant="outlined" sx={{ borderRadius: 999 }} />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
