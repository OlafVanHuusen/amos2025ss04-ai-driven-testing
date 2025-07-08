import React from 'react';
import { Paper, Typography, Stack, CircularProgress, Box, Divider } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  responseTime?: number;
  coverage_data?: {
    overall_coverage: number;
    line_coverage: number;
    branch_coverage: number;
    covered_lines: number;
    total_lines: number;
    uncovered_lines: number[];
    details: string;
  };
}

interface ChatHistoryProps {
  messages: ChatMessage[];
  loading?: boolean;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, loading = false }) => (
  <Stack spacing={2} sx={{ flexGrow: 1, mb: 1, pb: 25 }}>
    {messages.length === 0 ? (
      <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.paper' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="subtitle2" fontWeight="bold">Assistant</Typography>
        </Box>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>Wie kann ich Ihnen heute helfen?</ReactMarkdown>
      </Paper>
    ) : (
      messages.map((msg, idx) => (
        <Paper
          key={idx}
          variant="outlined"
          sx={{ p: 2, bgcolor: msg.role === 'user' ? '#f5faff' : 'background.paper' }}
        >
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
            <Typography variant="subtitle2" fontWeight="bold">
              {msg.role === 'user' ? 'Du' : 'Assistant'}
            </Typography>

            {msg.role === 'assistant' && typeof msg.responseTime === 'number' && (
              <Typography variant="subtitle2" color="text.secondary" whiteSpace="nowrap">
                {msg.responseTime.toFixed(1)} s
              </Typography>
            )}
          </Box>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
          
          {/* Display coverage data if available */}
          {msg.coverage_data && (
            <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="subtitle2" fontWeight="bold" sx={{ mb: 1 }}>
                Code Coverage Analysis
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Overall Coverage:</strong> {msg.coverage_data.overall_coverage.toFixed(1)}%
                  </Typography>
                </Box>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Line Coverage:</strong> {msg.coverage_data.line_coverage.toFixed(1)}%
                  </Typography>
                </Box>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Covered Lines:</strong> {msg.coverage_data.covered_lines}
                  </Typography>
                </Box>
                <Box sx={{ minWidth: '150px' }}>
                  <Typography variant="body2">
                    <strong>Total Lines:</strong> {msg.coverage_data.total_lines}
                  </Typography>
                </Box>
              </Box>
              {msg.coverage_data.uncovered_lines.length > 0 && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  <strong>Uncovered Lines:</strong> {msg.coverage_data.uncovered_lines.join(', ')}
                </Typography>
              )}
              <Divider sx={{ my: 1 }} />
              <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                {msg.coverage_data.details}
              </Typography>
            </Box>
          )}
        </Paper>
      ))
    )}

    {loading && (
      <Stack direction="row" alignItems="center" spacing={2} sx={{ px: 1 }}>
        <CircularProgress size={24} />
        <Typography variant="body2" color="text.secondary">
          Antwort wird geladen…
        </Typography>
      </Stack>
    )}
  </Stack>
);

export default ChatHistory; 