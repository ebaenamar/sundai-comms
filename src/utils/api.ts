import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: '/api',
});

// Subscribers API
export const getSubscribers = async (activeOnly = true) => {
  const response = await api.get(`/subscribers?active_only=${activeOnly}`);
  return response.data;
};

export const unsubscribe = async (email: string) => {
  const response = await api.post('/subscribers/unsubscribe', { email });
  return response.data;
};

// Newsletter API
export const sendNewsletter = async (subject: string, content: string) => {
  const response = await api.post('/newsletter/send', { subject, content });
  return response.data;
};

// Types
export interface Subscriber {
  _id: string;
  email: string;
  name?: string;
  subscribed_at: string;
  updated_at: string;
  active: boolean;
  data?: Record<string, any>;
}

export interface FormSubmission {
  _id: string;
  form_id: string;
  submission_data: any;
  received_at: string;
}
