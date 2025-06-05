import axios from 'axios';

// URL base de la API - Usar la URL directa con HTTPS para evitar problemas de CORS
const API_BASE_URL = 'https://tally-subscriber-api.onrender.com';

// Configuración común para todas las solicitudes
const axiosConfig = {
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000, // 30 segundos de timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Forwarded-Proto': 'https' // Forzar HTTPS
  },
  withCredentials: false,
  maxRedirects: 0, // No seguir redirecciones automáticamente
  httpsAgent: new (require('https').Agent)({ 
    rejectUnauthorized: false, // Solo para desarrollo
    keepAlive: true
  }),
  validateStatus: (status) => status >= 200 && status < 500 // Considerar códigos de estado 2xx y 3xx como exitosos
};

// Crear instancia de axios con configuración
const api = axios.create(axiosConfig);

// Interceptor para manejar redirecciones manualmente
api.interceptors.request.use(config => {
  // Asegurarse de que la URL use HTTPS
  if (config.url && config.url.startsWith('http://')) {
    config.url = config.url.replace('http://', 'https://');
  }
  
  // Asegurarse de que la URL base use HTTPS
  if (config.baseURL && config.baseURL.startsWith('http://')) {
    config.baseURL = config.baseURL.replace('http://', 'https://');
  }
  
  // Asegurarse de que la URL no termine con una barra para evitar redirecciones
  if (config.url && config.url.endsWith('/')) {
    config.url = config.url.slice(0, -1);
  }
  
  // Agregar parámetros de caché solo para solicitudes GET
  if (config.method === 'get' || !config.method) {
    config.params = {
      ...config.params,
      _t: Date.now() // Evitar caché del navegador
    };
  }
  
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => {
    // Manejar respuesta exitosa
    return response;
  },
  (error) => {
    // Manejar errores
    if (error.response) {
      // La petición se realizó y el servidor respondió con un código de estado
      // que está fuera del rango 2xx
      console.error('Error de respuesta:', error.response.status, error.response.data);
    } else if (error.request) {
      // La petición se realizó pero no se recibió respuesta
      console.error('No se recibió respuesta del servidor:', error.request);
    } else {
      // Algo sucedió en la configuración de la petición que generó un error
      console.error('Error al realizar la petición:', error.message);
    }
    return Promise.reject(error);
  }
);

// Subscribers API
export const getSubscribers = async (activeOnly = true) => {
  // Asegurarse de que no haya barras adicionales en la URL
  const url = `/subscribers?active_only=${activeOnly}`.replace(/\/+$/, '');
  try {
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    console.error('Error en getSubscribers:', error);
    throw error;
  }
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
