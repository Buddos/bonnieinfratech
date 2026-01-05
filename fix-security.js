const fs = require('fs');
const path = require('path');

// Add security headers to all HTML files
function addSecurityHeaders(filePath) {
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Add security meta tags
        const securityTags = `
<meta http-equiv="Content-Security-Policy" content="default-src 'self' https://cdnjs.cloudflare.com; script-src 'self' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; font-src 'self' https://cdnjs.cloudflare.com; img-src 'self' data: https:">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
`;
        
        // Insert after <head>
        content = content.replace('<head>', `<head>${securityTags}`);
        
        // Fix empty href attributes
        content = content.replace(/href="#"/g, 'href="javascript:void(0)"');
        
        fs.writeFileSync(filePath, content);
        console.log(`Updated: ${filePath}`);
    }
}

// Update all HTML files
const htmlFiles = ['index.html', 'login.html', 'registration.html', 'privacy.html', 'terms.html', 'cookies.html', 'sitemap.html'];

htmlFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
        addSecurityHeaders(filePath);
    } else {
        console.log(`Creating: ${file}`);
        // Create basic HTML file
        const basicHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'">
    <title>${file.replace('.html', '')} - BonnieInfratech</title>
    <style>body{font-family:Arial,sans-serif;padding:20px;max-width:800px;margin:0 auto}</style>
</head>
<body>
    <h1>${file.replace('.html', '').charAt(0).toUpperCase() + file.replace('.html', '').slice(1)}</h1>
    <p>BonnieInfratech Solutions - IT & Networking Services</p>
    <a href="index.html">Back to Home</a>
</body>
</html>`;
        fs.writeFileSync(filePath, basicHTML);
    }
});

console.log('Security updates completed!');