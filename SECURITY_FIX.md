# Security Fix: Credentials Setup

## What happened?
Your git sync was failing because GitHub detected Google Cloud Service Account credentials in your repository. For security reasons, GitHub blocks pushes that contain sensitive credentials.

## What was fixed?
1. **Removed credentials file**: The `app/book-scanner-ocr-466206-2737ae18ea9d.json` file has been removed from the repository
2. **Updated .gitignore**: Added patterns to exclude credential files from future commits
3. **Secure setup**: Your app already supports environment variables for credentials

## How to set up credentials securely

### Option 1: Environment Variable (Recommended)
Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your credentials file:

**macOS/Linux:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

**Windows:**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\credentials.json
```

### Option 2: Store in a secure location
1. Move your credentials file to a secure location outside the repository:
   ```bash
   mkdir -p ~/.config/book-scanner
   mv /path/to/book-scanner-ocr-466206-2737ae18ea9d.json ~/.config/book-scanner/
   ```

2. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/book-scanner/book-scanner-ocr-466206-2737ae18ea9d.json"
   ```

### Option 3: Add to shell profile (persistent)
Add the export command to your shell profile so it's always available:

**For zsh (default on macOS):**
```bash
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/book-scanner/book-scanner-ocr-466206-2737ae18ea9d.json"' >> ~/.zshrc
source ~/.zshrc
```

## Verify setup
After setting up credentials, you can verify they work by running your book scanner app. The app will warn you if credentials are not properly configured.

## Important Security Notes
- **Never commit credentials** to version control
- **Keep credentials files outside** your project repository
- **Use environment variables** or secure credential management services
- **Regularly rotate** your API keys and service account credentials

## Files affected
- ✅ **Fixed**: Git sync now works
- ✅ **Secure**: Credentials removed from repository
- ✅ **Protected**: .gitignore updated to prevent future credential commits
