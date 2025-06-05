/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*` : 'http://localhost:5001/api/:path*',
      },
    ];
  },
  // Configuración para Vercel
  distDir: '.next',
  // Asegurarse de que las imágenes funcionen correctamente
  images: {
    domains: ['localhost'],
    unoptimized: true
  }
}

module.exports = nextConfig
