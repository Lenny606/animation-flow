import { QueryClient } from '@tanstack/react-query';

/**
 * Standard configuration for TanStack Query Client.
 * 
 * Recommended settings for premium apps:
 * - defaultOptions.queries.staleTime: 5 minutes to reduce redundant requests
 * - defaultOptions.queries.retry: 1 (reduce retry noise)
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
