/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    images: {
        domains: [
            'images.pexels.com',
            'videos.pexels.com',
            'commondatastorage.googleapis.com',
            'grainy-gradients.vercel.app'
        ],
    },
}

module.exports = nextConfig
