import api from './axios';
import type { ComplaintData } from '../types/complaint';

export const saveComplaint = async (payload: ComplaintData) => {
  return api.post('/complaints', payload);
};
