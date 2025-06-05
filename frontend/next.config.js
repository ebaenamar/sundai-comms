/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Configuración de redirecciones de API
  async rewrites() {
    // En desarrollo, redirigir las solicitudes de API al backend
    if (process.env.NODE_ENV === 'development') {
      const backendUrl = 'https://tally-subscriber-api.onrender.com';
      return [
        {
          source: '/api/:path*',
          destination: `${backendUrl}/api/:path*`,
        },
      ];
    }
    
    // En producción, no es necesario redirigir si están en el mismo dominio
    return [];
  },
  
  // Configuración para Vercel
  distDir: '.next',
  
  // Configuración de imágenes
  images: {
    domains: ['localhost', 'tally-subscriber-api.onrender.com'],
    unoptimized: true,
    minimumCacheTTL: 60, // 1 minuto de caché para las imágenes
  },
  
  // Configuración de cabeceras para CORS
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE, OPTIONS, PATCH' },
          { key: 'Access-Control-Allow-Headers', value: 'X-Requested-With, Content-Type, Authorization' },
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Max-Age', value: '86400' },
        ],
      },
    ];
  },
  
  // Configuración de Webpack
  webpack: (config, { isServer }) => {
    // Configuraciones adicionales de Webpack si son necesarias
    return config;
  },
  
  // Desactivar la verificación de tipos en tiempo de compilación
  typescript: {
    ignoreBuildErrors: true,
  },
  
  // Desactivar la verificación de ESLint en tiempo de compilación
  eslint: {
    ignoreDuringBuilds: true,
  },
}

module.exports = nextConfig
